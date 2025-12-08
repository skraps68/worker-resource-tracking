"""Database connection and initialization."""
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager


_db_config = None


def init_db(app):
    """Initialize database configuration from Flask app."""
    global _db_config
    _db_config = app.config['DATABASE_URL']


def get_connection():
    """Get a database connection."""
    if _db_config is None:
        raise RuntimeError("Database not initialized. Call init_db first.")
    return psycopg2.connect(_db_config, cursor_factory=RealDictCursor)


@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def create_schema():
    """Create database schema with worker, resource, org, worker_type, and hc_series tables."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Create org table (must be created before worker due to potential FK)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS org (
                name TEXT PRIMARY KEY,
                parent TEXT,
                FOREIGN KEY (parent) REFERENCES org(name)
            )
        """)
        
        # Create worker_type table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS worker_type (
                type TEXT PRIMARY KEY
            )
        """)
        
        # Create hc_series table for budget and forecast time series
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hc_series (
                series_type CHAR(1) NOT NULL CHECK (series_type IN ('B', 'F')),
                org TEXT NOT NULL,
                date DATE NOT NULL,
                value INTEGER NOT NULL,
                PRIMARY KEY (series_type, org, date),
                FOREIGN KEY (org) REFERENCES org(name)
            )
        """)
        
        # Create worker table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS worker (
                WID SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                org TEXT NOT NULL,
                type TEXT NOT NULL
            )
        """)
        
        # Create resource table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resource (
                RID INTEGER NOT NULL,
                version INTEGER NOT NULL,
                WID INTEGER NOT NULL,
                res_start DATE NOT NULL,
                res_end DATE NOT NULL,
                proc_start TIMESTAMP NOT NULL,
                proc_end TIMESTAMP NOT NULL,
                PRIMARY KEY (RID, version),
                FOREIGN KEY (WID) REFERENCES worker(WID)
            )
        """)
        
        # Create sequence for RID generation
        cursor.execute("""
            CREATE SEQUENCE IF NOT EXISTS resource_rid_seq
        """)
        
        conn.commit()


def load_static_data():
    """Load static reference data into org and worker_type tables."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Load organization data (parent must be inserted before children)
        cursor.execute("""
            INSERT INTO org (name, parent) VALUES ('All', NULL)
            ON CONFLICT (name) DO NOTHING
        """)
        
        cursor.execute("""
            INSERT INTO org (name, parent) VALUES 
                ('Sales', 'All'),
                ('Marketing', 'All'),
                ('Technology', 'All'),
                ('Quality Assurance', 'All')
            ON CONFLICT (name) DO NOTHING
        """)
        
        # Load worker type data
        cursor.execute("""
            INSERT INTO worker_type (type) VALUES 
                ('Employee'),
                ('Consultant - Fixed'),
                ('Consultant - T&M')
            ON CONFLICT (type) DO NOTHING
        """)
        
        conn.commit()
