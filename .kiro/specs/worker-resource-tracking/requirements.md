# Requirements Document

## Introduction

This document specifies requirements for a bi-temporal worker resource tracking and forecasting application. The system manages workers and their associated resource records over time, supporting both business time (when events actually occurred) and processing time (when the system recorded the events). This bi-temporal model enables historical tracking, corrections, and accurate point-in-time queries across two independent time dimensions.

## Glossary

- **System**: The worker resource tracking application
- **Worker**: A person who performs work, represented as a static reference record
- **Resource**: A time-bound allocation of a worker, tracked bi-temporally with lifecycle management
- **WID**: Worker ID, a unique identifier for each worker record
- **RID**: Resource ID, a unique identifier for each resource record
- **version**: A sequential number tracking resource record changes over processing time
- **Business Time**: The time period when a resource was actually active in the real world (res_start to res_end), represented as dates without time components
- **Processing Time**: The time period when a resource record was current in the system (proc_start to proc_end), represented as full datetimes
- **Infinity**: A sentinel value representing an open-ended time range, represented as 9999-12-31 for dates and 9999-12-31 23:59:00 for datetimes
- **As-of Query**: A bi-temporal query that retrieves the state of resources as they were known at a specific processing datetime for a specific business date
- **name**: The name of a worker
- **org**: The organization a worker belongs to
- **type**: The classification or role type of a worker
- **Bi-temporal**: A data model supporting two independent time dimensions (business time and processing time)
- **Active Resource**: A resource record where proc_end is set to infinity (current version)
- **Historical Resource**: A resource record where proc_end is not infinity (superseded version)

## Requirements

### Requirement 1

**User Story:** As a resource manager, I want to create a new worker and associated resource record, so that I can track when workers begin their assignments.

#### Acceptance Criteria

1. WHEN a user submits worker information (name, org, type), THE System SHALL generate a unique WID and create a worker record
2. WHEN a worker record is created, THE System SHALL ensure the WID does not already exist in the worker table
3. WHEN a user creates a resource for a worker, THE System SHALL generate a unique RID and set the version to 1
4. WHEN a resource record is created, THE System SHALL set res_start to the user-provided business date
5. WHEN a resource record is created, THE System SHALL set res_end to infinity (9999-12-31)
6. WHEN a resource record is created, THE System SHALL set proc_start to the current system datetime
7. WHEN a resource record is created, THE System SHALL set proc_end to infinity (9999-12-31 23:59:00)
8. WHEN creating a new worker and resource, THE System SHALL create the worker record before the resource record to maintain referential integrity

### Requirement 2

**User Story:** As a resource manager, I want to update the business time range of a resource, so that I can correct or adjust when a worker's assignment actually started or ended.

#### Acceptance Criteria

1. WHEN a user updates res_start or res_end on a resource, THE System SHALL set proc_end on the current record to the current system datetime
2. WHEN a user updates res_start or res_end on a resource, THE System SHALL create a new resource record with version incremented by 1
3. WHEN creating a new version of a resource, THE System SHALL copy RID and WID from the previous version
4. WHEN creating a new version of a resource, THE System SHALL set proc_start to the exact datetime used for proc_end on the previous version
5. WHEN creating a new version of a resource, THE System SHALL set proc_end to infinity (9999-12-31 23:59:00)
6. WHEN creating a new version of a resource, THE System SHALL apply the user-provided res_start and/or res_end values
7. WHEN updating a resource, THE System SHALL preserve all historical versions in the database

### Requirement 3

**User Story:** As a resource manager, I want to view all currently active resources, so that I can see the current state of worker assignments.

#### Acceptance Criteria

1. WHEN a user views the active resources list without specifying query parameters, THE System SHALL display only resources where proc_end equals infinity
2. WHEN displaying active resources, THE System SHALL show RID, version, WID, worker name, org, type, res_start, res_end, proc_start, and proc_end
3. WHEN displaying active resources, THE System SHALL join resource records with worker records using WID

### Requirement 6

**User Story:** As a resource manager, I want to execute bi-temporal "as-of" queries, so that I can view the historical state of resources as they were known at specific points in time.

#### Acceptance Criteria

1. WHEN a user accesses the query panel, THE System SHALL provide input fields for business date and processing datetime
2. WHEN a user specifies only a business date, THE System SHALL default the processing datetime to the current system datetime
3. WHEN a user executes an as-of query with business date D and processing datetime P, THE System SHALL return resources where proc_start <= P and proc_end > P and res_start <= D and res_end > D
4. WHEN displaying as-of query results, THE System SHALL show the same columns as the active resources list
5. WHEN a user executes an as-of query, THE System SHALL join resource records with worker records using WID

### Requirement 4

**User Story:** As a system administrator, I want the system to maintain data integrity, so that the bi-temporal model remains consistent and queryable.

#### Acceptance Criteria

1. WHEN any resource record is created, THE System SHALL ensure RID uniqueness within the resource table
2. WHEN any worker record is created, THE System SHALL ensure WID uniqueness within the worker table
3. WHEN any resource record is created, THE System SHALL validate that the WID exists in the worker table
4. WHEN any resource record is created or updated, THE System SHALL ensure proc_start is less than or equal to proc_end
5. WHEN any resource record is created or updated, THE System SHALL ensure res_start is less than or equal to res_end
6. WHEN multiple versions of a resource exist with the same RID, THE System SHALL ensure only one version has proc_end set to infinity
7. WHEN multiple versions of a resource exist with the same RID, THE System SHALL ensure version numbers are sequential and unique

### Requirement 5

**User Story:** As a resource manager, I want a web-based interface for managing workers and resources, so that I can perform all operations through a simple GUI.

#### Acceptance Criteria

1. WHEN a user accesses the application, THE System SHALL display a web-based interface with distinct panels for creation and viewing
2. WHEN a user is in the creation panel, THE System SHALL provide input fields for name, org, type, and res_start
3. WHEN a user is in the creation panel, THE System SHALL provide a submit action that creates both worker and resource records
4. WHEN a user is in the creation panel, THE System SHALL provide input fields to update res_start and res_end for existing resources
5. WHEN a user is in the viewing panel, THE System SHALL display a list of all active resources with their associated worker information
6. WHEN a user is in the query panel, THE System SHALL provide input fields for business date and processing datetime to execute as-of queries
7. WHEN a user interacts with the interface, THE System SHALL provide clear feedback on successful operations and validation errors
