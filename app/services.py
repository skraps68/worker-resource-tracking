"""Business logic services for worker and resource management."""
from datetime import datetime
from app.database import get_db
from app.models import INFINITY_DATE, INFINITY_DATETIME
from app.validation import (
    validate_required_field,
    validate_business_time_range,
    validate_processing_time_range
)


class WorkerService:
    """Service for worker operations."""
    
    @staticmethod
    def create_worker(name, org, type_):
        """Create a new worker and return the WID."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO worker (name, org, type) VALUES (%s, %s, %s) RETURNING WID",
                (name, org, type_)
            )
            result = cursor.fetchone()
            return result['wid']


class ResourceService:
    """Service for resource operations."""
    
    @staticmethod
    def create_worker_and_resource(name, org, type_, res_start):
        """Create a new worker and associated resource record."""
        # Validate required fields
        validate_required_field(name, "name")
        validate_required_field(org, "org")
        validate_required_field(type_, "type")
        validate_required_field(res_start, "res_start")
        
        # Validate business time range (res_start <= INFINITY_DATE)
        validate_business_time_range(res_start, INFINITY_DATE)
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Create worker
            cursor.execute(
                "INSERT INTO worker (name, org, type) VALUES (%s, %s, %s) RETURNING WID",
                (name, org, type_)
            )
            wid = cursor.fetchone()['wid']
            
            # Generate RID
            cursor.execute("SELECT nextval('resource_rid_seq') as rid")
            rid = cursor.fetchone()['rid']
            
            # Create resource
            proc_start = datetime.now()
            
            # Validate processing time range (proc_start <= INFINITY_DATETIME)
            validate_processing_time_range(proc_start, INFINITY_DATETIME)
            
            cursor.execute(
                """INSERT INTO resource 
                   (RID, version, WID, res_start, res_end, proc_start, proc_end)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (rid, 1, wid, res_start, INFINITY_DATE, proc_start, INFINITY_DATETIME)
            )
            
            return wid, rid, 1
    
    @staticmethod
    def update_resource(rid, res_start=None, res_end=None):
        """Update a resource by creating a new version."""
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Get current version
            cursor.execute(
                """SELECT * FROM resource 
                   WHERE RID = %s AND proc_end = %s""",
                (rid, INFINITY_DATETIME)
            )
            current = cursor.fetchone()
            
            if not current:
                raise ValueError(f"Resource with RID {rid} not found")
            
            # Close current version
            proc_end = datetime.now()
            
            # Create new version
            new_version = current['version'] + 1
            new_res_start = res_start if res_start is not None else current['res_start']
            new_res_end = res_end if res_end is not None else current['res_end']
            
            # Validate business time range
            validate_business_time_range(new_res_start, new_res_end)
            
            # Validate processing time range (proc_end <= INFINITY_DATETIME)
            validate_processing_time_range(proc_end, INFINITY_DATETIME)
            
            cursor.execute(
                "UPDATE resource SET proc_end = %s WHERE RID = %s AND version = %s",
                (proc_end, rid, current['version'])
            )
            
            cursor.execute(
                """INSERT INTO resource 
                   (RID, version, WID, res_start, res_end, proc_start, proc_end)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (rid, new_version, current['wid'], new_res_start, new_res_end, 
                 proc_end, INFINITY_DATETIME)
            )
            
            return rid, new_version
    
    @staticmethod
    def get_active_resources():
        """Get all active resources with worker information (business date constrained to today)."""
        from datetime import date
        today = date.today()
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT r.RID, r.version, r.WID, w.name, w.org, w.type,
                          r.res_start, r.res_end, r.proc_start, r.proc_end
                   FROM resource r
                   JOIN worker w ON r.WID = w.WID
                   WHERE r.proc_end = %s
                     AND r.res_start <= %s AND r.res_end > %s""",
                (INFINITY_DATETIME, today, today)
            )
            return cursor.fetchall()
    
    @staticmethod
    def get_open_resource_records():
        """Get all open resource records (proc_end = infinity) with worker information."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT r.RID, r.version, r.WID, w.name, w.org, w.type,
                          r.res_start, r.res_end, r.proc_start, r.proc_end
                   FROM resource r
                   JOIN worker w ON r.WID = w.WID
                   WHERE r.proc_end = %s""",
                (INFINITY_DATETIME,)
            )
            return cursor.fetchall()
    
    @staticmethod
    def as_of_query(business_date, processing_datetime=None):
        """Execute bi-temporal as-of query."""
        if processing_datetime is None:
            processing_datetime = datetime.now()
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT r.RID, r.version, r.WID, w.name, w.org, w.type,
                          r.res_start, r.res_end, r.proc_start, r.proc_end
                   FROM resource r
                   JOIN worker w ON r.WID = w.WID
                   WHERE r.proc_start <= %s AND r.proc_end > %s
                     AND r.res_start <= %s AND r.res_end > %s""",
                (processing_datetime, processing_datetime, business_date, business_date)
            )
            return cursor.fetchall()
    
    @staticmethod
    def get_orgs():
        """Get all organizations."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, parent FROM org ORDER BY name")
            rows = cursor.fetchall()
            return [{'name': row['name'], 'parent': row['parent']} for row in rows]
    
    @staticmethod
    def get_worker_types():
        """Get all worker types."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT type FROM worker_type ORDER BY type")
            rows = cursor.fetchall()
            return [row['type'] for row in rows]
