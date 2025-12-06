"""Repository classes for data access."""
from typing import Optional, List
from app.database import get_db
from app.models import Worker, Resource, INFINITY_DATETIME
from app.validation import (
    validate_required_field,
    validate_business_time_range,
    validate_processing_time_range
)


class WorkerRepository:
    """Repository for worker data access."""
    
    @staticmethod
    def create(name: str, org: str, type_: str) -> int:
        """
        Create a new worker and return the auto-generated WID.
        
        Args:
            name: Worker name
            org: Worker organization
            type_: Worker type
            
        Returns:
            The auto-generated WID
        """
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO worker (name, org, type) VALUES (%s, %s, %s) RETURNING WID",
                (name, org, type_)
            )
            result = cursor.fetchone()
            return result['wid']
    
    @staticmethod
    def get_by_wid(wid: int) -> Optional[Worker]:
        """
        Get a worker by WID.
        
        Args:
            wid: Worker ID
            
        Returns:
            Worker object or None if not found
        """
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT WID, name, org, type FROM worker WHERE WID = %s",
                (wid,)
            )
            result = cursor.fetchone()
            if result:
                return Worker(
                    WID=result['wid'],
                    name=result['name'],
                    org=result['org'],
                    type=result['type']
                )
            return None
    
    @staticmethod
    def get_all() -> List[Worker]:
        """
        Get all workers.
        
        Returns:
            List of Worker objects
        """
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT WID, name, org, type FROM worker")
            results = cursor.fetchall()
            return [
                Worker(
                    WID=row['wid'],
                    name=row['name'],
                    org=row['org'],
                    type=row['type']
                )
                for row in results
            ]
    
    @staticmethod
    def exists(wid: int) -> bool:
        """
        Check if a worker with the given WID exists.
        
        Args:
            wid: Worker ID
            
        Returns:
            True if worker exists, False otherwise
        """
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM worker WHERE WID = %s",
                (wid,)
            )
            return cursor.fetchone() is not None


class ResourceRepository:
    """Repository for resource data access."""
    
    @staticmethod
    def _get_next_rid() -> int:
        """Get the next RID from the sequence."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nextval('resource_rid_seq') as rid")
            return cursor.fetchone()['rid']
    
    @staticmethod
    def create(wid: int, res_start, res_end, proc_start, proc_end) -> tuple:
        """
        Create a new resource with version 1.
        
        Args:
            wid: Worker ID
            res_start: Resource start date
            res_end: Resource end date
            proc_start: Processing start datetime
            proc_end: Processing end datetime
            
        Returns:
            Tuple of (RID, version)
        """
        # Validate required fields
        validate_required_field(wid, "wid")
        validate_required_field(res_start, "res_start")
        validate_required_field(res_end, "res_end")
        validate_required_field(proc_start, "proc_start")
        validate_required_field(proc_end, "proc_end")
        
        # Validate time ranges
        validate_business_time_range(res_start, res_end)
        validate_processing_time_range(proc_start, proc_end)
        
        rid = ResourceRepository._get_next_rid()
        version = 1
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO resource 
                   (RID, version, WID, res_start, res_end, proc_start, proc_end)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (rid, version, wid, res_start, res_end, proc_start, proc_end)
            )
        
        return rid, version
    
    @staticmethod
    def get_by_rid_version(rid: int, version: int) -> Optional[Resource]:
        """
        Get a specific version of a resource.
        
        Args:
            rid: Resource ID
            version: Version number
            
        Returns:
            Resource object or None if not found
        """
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT RID, version, WID, res_start, res_end, proc_start, proc_end
                   FROM resource WHERE RID = %s AND version = %s""",
                (rid, version)
            )
            result = cursor.fetchone()
            if result:
                return Resource(
                    RID=result['rid'],
                    version=result['version'],
                    WID=result['wid'],
                    res_start=result['res_start'],
                    res_end=result['res_end'],
                    proc_start=result['proc_start'],
                    proc_end=result['proc_end']
                )
            return None
    
    @staticmethod
    def get_current_version(rid: int) -> Optional[Resource]:
        """
        Get the current (active) version of a resource.
        
        Args:
            rid: Resource ID
            
        Returns:
            Resource object or None if not found
        """
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT RID, version, WID, res_start, res_end, proc_start, proc_end
                   FROM resource WHERE RID = %s AND proc_end = %s""",
                (rid, INFINITY_DATETIME)
            )
            result = cursor.fetchone()
            if result:
                return Resource(
                    RID=result['rid'],
                    version=result['version'],
                    WID=result['wid'],
                    res_start=result['res_start'],
                    res_end=result['res_end'],
                    proc_start=result['proc_start'],
                    proc_end=result['proc_end']
                )
            return None
    
    @staticmethod
    def get_all_versions(rid: int) -> List[Resource]:
        """
        Get all versions of a resource.
        
        Args:
            rid: Resource ID
            
        Returns:
            List of Resource objects ordered by version
        """
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT RID, version, WID, res_start, res_end, proc_start, proc_end
                   FROM resource WHERE RID = %s ORDER BY version""",
                (rid,)
            )
            results = cursor.fetchall()
            return [
                Resource(
                    RID=row['rid'],
                    version=row['version'],
                    WID=row['wid'],
                    res_start=row['res_start'],
                    res_end=row['res_end'],
                    proc_start=row['proc_start'],
                    proc_end=row['proc_end']
                )
                for row in results
            ]
    
    @staticmethod
    def update_proc_end(rid: int, version: int, proc_end) -> None:
        """
        Update the proc_end of a specific resource version.
        
        Args:
            rid: Resource ID
            version: Version number
            proc_end: New processing end datetime
        """
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE resource SET proc_end = %s WHERE RID = %s AND version = %s",
                (proc_end, rid, version)
            )
    
    @staticmethod
    def get_all() -> List[Resource]:
        """
        Get all resources.
        
        Returns:
            List of Resource objects
        """
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT RID, version, WID, res_start, res_end, proc_start, proc_end
                   FROM resource ORDER BY RID, version"""
            )
            results = cursor.fetchall()
            return [
                Resource(
                    RID=row['rid'],
                    version=row['version'],
                    WID=row['wid'],
                    res_start=row['res_start'],
                    res_end=row['res_end'],
                    proc_start=row['proc_start'],
                    proc_end=row['proc_end']
                )
                for row in results
            ]
