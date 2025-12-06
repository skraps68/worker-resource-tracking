# Worker Resource Tracking System

A bi-temporal worker resource tracking and forecasting application built with Flask and PostgreSQL.

## Project Structure

```
.
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── database.py          # Database connection and schema
│   ├── models.py            # Data models
│   ├── services.py          # Business logic services
│   ├── routes.py            # API endpoints
│   └── tests/               # Test modules
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL 12+

### Installation

1. Clone the repository and navigate to the project directory

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database:
```bash
createdb worker_resource_tracking
```

5. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

6. Run the application:
```bash
python run.py
```

The application will create the database schema automatically on startup.

## API Endpoints

### POST /api/workers
Create a new worker and associated resource record.

### PUT /api/resources/:rid
Update a resource by creating a new version.

### GET /api/resources/active
Get all currently active resources.

### GET /api/resources/as-of
Execute a bi-temporal as-of query.

## Testing

### Prerequisites for Testing

Tests require a PostgreSQL test database. Set up the test database:

```bash
createdb worker_resource_tracking_test
```

Or set a custom test database URL:
```bash
export TEST_DATABASE_URL="postgresql://username:password@localhost:5432/worker_resource_tracking_test"
```

### Running Tests

Run all tests with pytest:
```bash
pytest app/tests/
```

Run specific property tests:
```bash
pytest app/tests/test_properties.py -v
```

Property-based tests use the Hypothesis library and run 100 iterations by default to verify correctness properties across randomly generated inputs.

## Database Schema

### Worker Table
- WID (Primary Key, Auto-increment)
- name
- org
- type

### Resource Table
- RID (Primary Key, part 1)
- version (Primary Key, part 2)
- WID (Foreign Key)
- res_start (Date)
- res_end (Date)
- proc_start (Timestamp)
- proc_end (Timestamp)
