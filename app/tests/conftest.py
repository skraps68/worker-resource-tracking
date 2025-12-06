"""Test configuration and fixtures."""
import os
import pytest
import psycopg2
from dotenv import load_dotenv
from app import create_app
from app.database import get_db, create_schema

# Load environment variables
load_dotenv()


def _check_postgres_available():
    """Check if PostgreSQL is available."""
    try:
        test_url = os.getenv(
            'TEST_DATABASE_URL',
            'postgresql://localhost/worker_resource_tracking_test'
        )
        conn = psycopg2.connect(test_url)
        conn.close()
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    # Check if PostgreSQL is available
    if not _check_postgres_available():
        pytest.skip("PostgreSQL test database not available")
    
    # Use a test database
    test_config = {
        'DATABASE_URL': os.getenv(
            'TEST_DATABASE_URL',
            'postgresql://localhost/worker_resource_tracking_test'
        ),
        'TESTING': True
    }
    
    app = create_app(test_config)
    
    # Create schema
    with app.app_context():
        create_schema()
    
    yield app
    
    # Cleanup after all tests
    with app.app_context():
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS resource CASCADE")
            cursor.execute("DROP TABLE IF EXISTS worker CASCADE")
            cursor.execute("DROP SEQUENCE IF EXISTS resource_rid_seq CASCADE")


@pytest.fixture(scope='function')
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture(scope='function')
def clean_db(app):
    """Clean database before each test."""
    with app.app_context():
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE resource, worker RESTART IDENTITY CASCADE")
            cursor.execute("ALTER SEQUENCE resource_rid_seq RESTART WITH 1")
    yield
