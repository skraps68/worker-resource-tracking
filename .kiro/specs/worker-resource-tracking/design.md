# Design Document: Worker Resource Tracking System

## Overview

The Worker Resource Tracking System is a web-based application that implements a bi-temporal data model for tracking worker assignments over time. The system maintains two independent time dimensions: business time (when events actually occurred) and processing time (when the system recorded the events). This design enables historical tracking, corrections to past data, and accurate point-in-time queries.

The application consists of a backend API for data management and a frontend web interface with three main panels: creation, viewing, and querying. The system ensures data integrity through referential constraints, unique identifiers, and bi-temporal versioning.

## Architecture

### System Components

1. **Database Layer**: Relational database storing worker and resource tables with bi-temporal support
2. **Backend API**: RESTful service handling CRUD operations, versioning logic, and query execution
3. **Frontend Application**: Web-based UI with three panels for creation, viewing, and querying
4. **Validation Layer**: Business logic ensuring data integrity and bi-temporal consistency

### Technology Stack

- **Database**: PostgreSQL with support for date and timestamp types
- **Backend**: Python with Flask
- **Frontend**: React with a component-based architecture
- **API Protocol**: REST with JSON payloads

### Architectural Patterns

- **Repository Pattern**: Separate data access logic from business logic
- **Service Layer**: Encapsulate business rules for worker/resource management
- **MVC Pattern**: Separate concerns between data models, business logic, and presentation

## Components and Interfaces

### Database Schema

#### Worker Table
```sql
CREATE TABLE worker (
  WID INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  org TEXT NOT NULL,
  type TEXT NOT NULL
);
```

#### Resource Table
```sql
CREATE TABLE resource (
  RID INTEGER NOT NULL,
  version INTEGER NOT NULL,
  WID INTEGER NOT NULL,
  res_start DATE NOT NULL,
  res_end DATE NOT NULL,
  proc_start DATETIME NOT NULL,
  proc_end DATETIME NOT NULL,
  PRIMARY KEY (RID, version),
  FOREIGN KEY (WID) REFERENCES worker(WID)
);
```

### Backend API Endpoints

#### POST /api/workers
Create a new worker and associated resource record.

**Request Body:**
```json
{
  "name": "string",
  "org": "string",
  "type": "string",
  "res_start": "YYYY-MM-DD"
}
```

**Response:**
```json
{
  "WID": "integer",
  "RID": "integer",
  "version": 1
}
```

#### PUT /api/resources/:rid
Update the business time range of a resource, creating a new version.

**Request Body:**
```json
{
  "res_start": "YYYY-MM-DD",  // optional
  "res_end": "YYYY-MM-DD"     // optional
}
```

Note: At least one of res_start or res_end must be provided. If only one is provided, the other date is copied from the current version.

**Response:**
```json
{
  "RID": "integer",
  "version": "integer"
}
```

#### GET /api/resources/active
Retrieve all currently active resources (proc_end = infinity).

**Response:**
```json
[
  {
    "RID": "integer",
    "version": "integer",
    "WID": "integer",
    "name": "string",
    "org": "string",
    "type": "string",
    "res_start": "YYYY-MM-DD",
    "res_end": "YYYY-MM-DD",
    "proc_start": "YYYY-MM-DD HH:MM:SS",
    "proc_end": "YYYY-MM-DD HH:MM:SS"
  }
]
```

#### GET /api/resources/as-of
Execute a bi-temporal as-of query.

**Query Parameters:**
- `business_date`: YYYY-MM-DD (required)
- `processing_datetime`: YYYY-MM-DD HH:MM:SS (optional, defaults to current datetime)

**Response:** Same format as /api/resources/active

### Frontend Components

#### CreationPanel Component
- Input fields for name, org, type, res_start
- Submit button to create worker and resource
- Input fields to select existing resource and update res_start/res_end
- Form validation and error display

#### ViewingPanel Component
- Table displaying all active resources
- Columns: RID, version, WID, name, org, type, res_start, res_end, proc_start, proc_end
- Auto-refresh capability

#### QueryPanel Component
- Input field for business date (required)
- Input field for processing datetime (optional, defaults to now)
- Submit button to execute as-of query
- Results table with same columns as ViewingPanel

## Data Models

### Worker Model
```typescript
interface Worker {
  WID: number;
  name: string;
  org: string;
  type: string;
}
```

### Resource Model
```typescript
interface Resource {
  RID: number;
  version: number;
  WID: number;
  res_start: Date;  // Date only, no time component
  res_end: Date;    // Date only, no time component
  proc_start: Date; // Full datetime
  proc_end: Date;   // Full datetime
}
```

### ResourceWithWorker Model (for display)
```typescript
interface ResourceWithWorker extends Resource {
  name: string;
  org: string;
  type: string;
}
```

### Constants
```typescript
const INFINITY_DATE = new Date('9999-12-31');
const INFINITY_DATETIME = new Date('9999-12-31T23:59:00');
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

After analyzing the acceptance criteria, several properties were identified as redundant and have been consolidated. The following properties represent the unique, testable behaviors of the system:

### Property 1: WID uniqueness
*For any* set of worker records created by the system, all WIDs SHALL be unique.
**Validates: Requirements 1.1, 1.2, 4.2**

### Property 2: RID uniqueness
*For any* set of resource records created by the system, all RIDs SHALL be unique.
**Validates: Requirements 1.3, 4.1**

### Property 3: Initial version is 1
*For any* newly created resource (first version), the version number SHALL equal 1.
**Validates: Requirements 1.3**

### Property 4: res_start preservation on creation
*For any* resource creation with user-provided res_start date D, the created resource SHALL have res_start equal to D.
**Validates: Requirements 1.4**

### Property 5: res_end defaults to infinity on creation
*For any* newly created resource, res_end SHALL equal the infinity date constant (9999-12-31).
**Validates: Requirements 1.5**

### Property 6: proc_start set to current time on creation
*For any* newly created resource, proc_start SHALL be within a reasonable time window (e.g., 1 second) of the current system datetime.
**Validates: Requirements 1.6**

### Property 7: proc_end defaults to infinity on creation
*For any* newly created resource, proc_end SHALL equal the infinity datetime constant (9999-12-31 23:59:00).
**Validates: Requirements 1.7**

### Property 8: Referential integrity on creation
*For any* resource record created, the WID SHALL exist in the worker table.
**Validates: Requirements 1.8, 4.3**

### Property 9: Old version closed on update
*For any* resource update operation, the previous version's proc_end SHALL be set to the current system datetime (within a reasonable time window).
**Validates: Requirements 2.1**

### Property 10: Version increment on update
*For any* resource update operation, the new version number SHALL equal the previous version number plus 1.
**Validates: Requirements 2.2**

### Property 11: RID and WID preservation across versions
*For any* resource update operation, the new version SHALL have the same RID and WID as the previous version.
**Validates: Requirements 2.3**

### Property 12: Temporal continuity across versions
*For any* resource update operation, the new version's proc_start SHALL equal the previous version's proc_end.
**Validates: Requirements 2.4**

### Property 13: New version proc_end defaults to infinity
*For any* resource update operation, the new version's proc_end SHALL equal the infinity datetime constant (9999-12-31 23:59:00).
**Validates: Requirements 2.5**

### Property 14: User input applied on update
*For any* resource update operation with user-provided res_start and/or res_end values, the new version SHALL have the provided values for those fields, and SHALL copy the unprovided values from the previous version.
**Validates: Requirements 2.6**

### Property 15: Historical preservation
*For any* resource with RID R that has been updated N times, there SHALL exist N+1 versions in the database with sequential version numbers from 1 to N+1.
**Validates: Requirements 2.7**

### Property 16: Active resources filter
*For any* query for active resources, all returned resources SHALL have proc_end equal to the infinity datetime constant.
**Validates: Requirements 3.1**

### Property 17: Active resources display completeness
*For any* active resource returned, the result SHALL include RID, version, WID, name, org, type, res_start, res_end, proc_start, and proc_end.
**Validates: Requirements 3.2, 6.4**

### Property 18: Worker-resource join correctness
*For any* resource returned (active or as-of query), the worker fields (name, org, type) SHALL match the worker record with the same WID.
**Validates: Requirements 3.3, 6.5**

### Property 19: As-of query default processing datetime
*For any* as-of query with only business date D specified, the processing datetime SHALL default to the current system datetime (within a reasonable time window).
**Validates: Requirements 6.2**

### Property 20: Bi-temporal query correctness
*For any* as-of query with business date D and processing datetime P, all returned resources SHALL satisfy: proc_start <= P AND proc_end > P AND res_start <= D AND res_end > D.
**Validates: Requirements 6.3**

### Property 21: Processing time validity
*For any* resource record (created or updated), proc_start SHALL be less than or equal to proc_end.
**Validates: Requirements 4.4**

### Property 22: Business time validity
*For any* resource record (created or updated), res_start SHALL be less than or equal to res_end.
**Validates: Requirements 4.5**

### Property 23: Single active version per resource
*For any* RID with multiple versions, exactly one version SHALL have proc_end equal to the infinity datetime constant.
**Validates: Requirements 4.6**

### Property 24: Sequential version numbering
*For any* RID with N versions, the version numbers SHALL be exactly {1, 2, 3, ..., N} with no gaps or duplicates.
**Validates: Requirements 4.7**

## Error Handling

### Validation Errors

The system SHALL validate all inputs and return appropriate error messages:

1. **Invalid WID on resource creation**: Return 400 Bad Request with message "Worker with WID {wid} does not exist"
2. **Invalid date ranges**: Return 400 Bad Request with message "Start date must be less than or equal to end date"
3. **Missing required fields**: Return 400 Bad Request with message "Required field {field} is missing"
4. **Invalid date format**: Return 400 Bad Request with message "Invalid date format for {field}"
5. **Resource not found on update**: Return 404 Not Found with message "Resource with RID {rid} not found"
6. **No dates provided on update**: Return 400 Bad Request with message "At least one of res_start or res_end must be provided"

### Database Errors

1. **Unique constraint violation**: Return 500 Internal Server Error with message "Database constraint violation"
2. **Foreign key violation**: Return 500 Internal Server Error with message "Referential integrity violation"
3. **Connection errors**: Return 503 Service Unavailable with message "Database temporarily unavailable"

### Concurrency Handling

The system SHALL handle concurrent updates to the same resource:
- Use optimistic locking by checking the current version before updating
- If the version has changed, return 409 Conflict with message "Resource has been modified by another user"

## Testing Strategy

### Unit Testing

Unit tests will verify specific examples and integration points:

1. **Worker creation**: Test creating workers with various valid inputs
2. **Resource creation**: Test creating resources with various valid res_start dates
3. **Resource update**: Test updating resources with various date combinations
4. **Active resources query**: Test querying with and without active resources
5. **As-of query**: Test with specific known dates and expected results
6. **Error cases**: Test all validation error scenarios
7. **Edge cases**: Test with infinity dates, boundary dates, concurrent updates

### Property-Based Testing

Property-based tests will verify universal properties across all inputs using the `hypothesis` library for Python.

Each property-based test SHALL:
- Run a minimum of 100 iterations with randomly generated inputs
- Be tagged with a comment referencing the specific correctness property from this design document
- Use the format: `# Feature: worker-resource-tracking, Property {number}: {property_text}`

**Test Data Generators:**

1. **Worker generator**: Random name, org, type strings
2. **Date generator**: Random dates between 2000-01-01 and 2030-12-31
3. **Datetime generator**: Random datetimes with second precision
4. **Resource generator**: Random resources with valid temporal ranges
5. **Update sequence generator**: Random sequences of resource updates

**Property Test Coverage:**

Each of the 24 correctness properties listed above SHALL be implemented as a separate property-based test. The tests will generate random valid inputs and verify the properties hold across all executions.

### Integration Testing

Integration tests will verify end-to-end workflows:

1. **Complete worker lifecycle**: Create worker, create resource, update resource multiple times, query history
2. **Bi-temporal queries**: Create resources, update them, query at various points in time
3. **Multi-user scenarios**: Simulate concurrent operations from multiple users

### Test Environment

- Use PostgreSQL with a test database that is reset between tests
- Alternatively, use SQLite in-memory database for faster unit test execution
- Mock current datetime for deterministic testing of time-dependent properties
- Use Flask test client for API endpoint testing
