# Implementation Plan

- [x] 1. Set up project structure and database
  - Create Python Flask project structure with separate modules for models, services, routes, and tests
  - Set up PostgreSQL database connection and configuration
  - Create database schema with worker and resource tables
  - Set up Flask application factory pattern
  - Configure environment variables for database connection
  - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 4.1, 4.2, 4.3_

- [x] 2. Implement data models and database layer
- [x] 2.1 Create Worker and Resource model classes
  - Define Worker model with WID, name, org, type fields
  - Define Resource model with RID, version, WID, res_start, res_end, proc_start, proc_end fields
  - Implement infinity constants for dates and datetimes
  - _Requirements: 1.1, 1.3, 1.5, 1.7_

- [x] 2.2 Implement database repository for workers
  - Create WorkerRepository with methods to create and query workers
  - Implement WID auto-generation with uniqueness guarantee
  - _Requirements: 1.1, 1.2, 4.2_

- [x] 2.3 Write property test for WID uniqueness
  - **Property 1: WID uniqueness**
  - **Validates: Requirements 1.1, 1.2, 4.2**

- [x] 2.4 Implement database repository for resources
  - Create ResourceRepository with methods to create, update, and query resources
  - Implement RID auto-generation with uniqueness guarantee
  - Implement version management logic
  - _Requirements: 1.3, 2.1, 2.2, 4.1_

- [x] 2.5 Write property test for RID uniqueness
  - **Property 2: RID uniqueness**
  - **Validates: Requirements 1.3, 4.1**

- [x] 2.6 Write property test for initial version
  - **Property 3: Initial version is 1**
  - **Validates: Requirements 1.3**

- [-] 3. Implement resource creation logic
- [x] 3.1 Create service layer for worker and resource creation
  - Implement create_worker_and_resource service method
  - Ensure worker is created before resource (referential integrity)
  - Set default values for res_end, proc_start, proc_end
  - _Requirements: 1.1, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8_

- [x] 3.2 Write property test for res_start preservation
  - **Property 4: res_start preservation on creation**
  - **Validates: Requirements 1.4**

- [x] 3.3 Write property test for res_end default
  - **Property 5: res_end defaults to infinity on creation**
  - **Validates: Requirements 1.5**

- [x] 3.4 Write property test for proc_start timing
  - **Property 6: proc_start set to current time on creation**
  - **Validates: Requirements 1.6**

- [x] 3.5 Write property test for proc_end default
  - **Property 7: proc_end defaults to infinity on creation**
  - **Validates: Requirements 1.7**

- [x] 3.6 Write property test for referential integrity
  - **Property 8: Referential integrity on creation**
  - **Validates: Requirements 1.8, 4.3**

- [x] 4. Implement resource update logic
- [x] 4.1 Create service layer for resource updates
  - Implement update_resource service method
  - Close current version by setting proc_end to current datetime
  - Create new version with incremented version number
  - Copy RID and WID from previous version
  - Set proc_start to match previous proc_end
  - Apply user-provided res_start and/or res_end, copy unprovided values
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7_

- [x] 4.2 Write property test for old version closure
  - **Property 9: Old version closed on update**
  - **Validates: Requirements 2.1**

- [x] 4.3 Write property test for version increment
  - **Property 10: Version increment on update**
  - **Validates: Requirements 2.2**

- [x] 4.4 Write property test for RID/WID preservation
  - **Property 11: RID and WID preservation across versions**
  - **Validates: Requirements 2.3**

- [x] 4.5 Write property test for temporal continuity
  - **Property 12: Temporal continuity across versions**
  - **Validates: Requirements 2.4**

- [x] 4.6 Write property test for new version proc_end
  - **Property 13: New version proc_end defaults to infinity**
  - **Validates: Requirements 2.5**

- [x] 4.7 Write property test for partial update
  - **Property 14: User input applied on update**
  - **Validates: Requirements 2.6**

- [x] 4.8 Write property test for historical preservation
  - **Property 15: Historical preservation**
  - **Validates: Requirements 2.7**

- [x] 5. Implement query logic for active resources
- [x] 5.1 Create service layer for active resources query
  - Implement get_active_resources service method
  - Filter resources where proc_end equals infinity
  - Join with worker table on WID
  - Return all required fields
  - _Requirements: 3.1, 3.2, 3.3_

- [x] 5.2 Write property test for active resources filter
  - **Property 16: Active resources filter**
  - **Validates: Requirements 3.1**

- [x] 5.3 Write property test for display completeness
  - **Property 17: Active resources display completeness**
  - **Validates: Requirements 3.2, 6.4**

- [x] 5.4 Write property test for join correctness
  - **Property 18: Worker-resource join correctness**
  - **Validates: Requirements 3.3, 6.5**

- [x] 6. Implement bi-temporal as-of query logic
- [x] 6.1 Create service layer for as-of queries
  - Implement as_of_query service method
  - Accept business_date and optional processing_datetime parameters
  - Default processing_datetime to current datetime if not provided
  - Filter resources using bi-temporal conditions
  - Join with worker table on WID
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 6.2 Write property test for default processing datetime
  - **Property 19: As-of query default processing datetime**
  - **Validates: Requirements 6.2**

- [x] 6.3 Write property test for bi-temporal query correctness
  - **Property 20: Bi-temporal query correctness**
  - **Validates: Requirements 6.3**

- [x] 7. Implement data validation
- [x] 7.1 Create validation utilities
  - Implement date range validation (start <= end)
  - Implement required field validation
  - Implement date format validation
  - _Requirements: 4.4, 4.5_

- [x] 7.2 Write property test for processing time validity
  - **Property 21: Processing time validity**
  - **Validates: Requirements 4.4**

- [x] 7.3 Write property test for business time validity
  - **Property 22: Business time validity**
  - **Validates: Requirements 4.5**

- [x] 7.4 Write property test for single active version
  - **Property 23: Single active version per resource**
  - **Validates: Requirements 4.6**

- [x] 7.5 Write property test for sequential versioning
  - **Property 24: Sequential version numbering**
  - **Validates: Requirements 4.7**

- [x] 8. Implement REST API endpoints
- [x] 8.1 Create POST /api/workers endpoint
  - Accept name, org, type, res_start in request body
  - Call create_worker_and_resource service
  - Return WID, RID, version in response
  - Handle validation errors
  - _Requirements: 1.1, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8_

- [x] 8.2 Create PUT /api/resources/:rid endpoint
  - Accept optional res_start and/or res_end in request body
  - Validate at least one date is provided
  - Call update_resource service
  - Return RID and new version in response
  - Handle validation and not-found errors
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7_

- [x] 8.3 Create GET /api/resources/active endpoint
  - Call get_active_resources service
  - Return list of active resources with worker information
  - _Requirements: 3.1, 3.2, 3.3_

- [x] 8.4 Create GET /api/resources/as-of endpoint
  - Accept business_date and optional processing_datetime query parameters
  - Call as_of_query service
  - Return list of resources matching bi-temporal criteria
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 8.5 Write unit tests for API endpoints
  - Test successful creation, update, and query operations
  - Test error responses for invalid inputs
  - Test edge cases (infinity dates, boundary conditions)
  - _Requirements: All_

- [ ] 9. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 10. Set up React frontend project
- [ ] 10.1 Create React application structure
  - Initialize React project with create-react-app or Vite
  - Set up component structure for CreationPanel, ViewingPanel, QueryPanel
  - Configure API client for backend communication
  - _Requirements: 5.1_

- [ ] 10.2 Implement CreationPanel component
  - Create form with input fields for name, org, type, res_start
  - Implement submit handler to call POST /api/workers
  - Display success/error feedback
  - Create form to select existing resource and update res_start/res_end
  - Implement update handler to call PUT /api/resources/:rid
  - _Requirements: 5.2, 5.3, 5.4, 5.7_

- [ ] 10.3 Implement ViewingPanel component
  - Create table to display active resources
  - Fetch data from GET /api/resources/active on component mount
  - Display all required columns
  - _Requirements: 5.5, 5.7_

- [ ] 10.4 Implement QueryPanel component
  - Create form with input fields for business_date and processing_datetime
  - Implement query handler to call GET /api/resources/as-of
  - Display results in table with same columns as ViewingPanel
  - _Requirements: 5.6, 6.1, 5.7_

- [ ] 10.5 Implement main App component
  - Create layout with tabs or panels for Creation, Viewing, and Query
  - Wire up all child components
  - Add basic styling
  - _Requirements: 5.1_

- [ ] 11. Final integration and testing
- [ ] 11.1 Test end-to-end workflows
  - Test creating worker and resource through UI
  - Test updating resource through UI
  - Test viewing active resources
  - Test executing as-of queries
  - _Requirements: All_

- [ ] 11.2 Write integration tests
  - Test complete worker lifecycle (create, update multiple times, query history)
  - Test bi-temporal queries at various points in time
  - Test concurrent update scenarios
  - _Requirements: All_

- [ ] 12. Final Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
