"""Property-based tests for worker resource tracking system."""
from datetime import datetime, date
from hypothesis import given, settings, strategies as st, HealthCheck
from app.repositories import WorkerRepository, ResourceRepository
from app.models import INFINITY_DATE, INFINITY_DATETIME


# Feature: worker-resource-tracking, Property 1: WID uniqueness
# Validates: Requirements 1.1, 1.2, 4.2
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    workers=st.lists(
        st.tuples(
            st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),  # name
            st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),  # org
            st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip())   # type
        ),
        min_size=1,
        max_size=10
    )
)
def test_wid_uniqueness(app, clean_db, workers):
    """
    Property 1: WID uniqueness
    For any set of worker records created by the system, all WIDs SHALL be unique.
    """
    with app.app_context():
        wids = []
        for name, org, type_ in workers:
            wid = WorkerRepository.create(name, org, type_)
            wids.append(wid)
        
        # All WIDs should be unique
        assert len(wids) == len(set(wids)), "WIDs are not unique"


# Feature: worker-resource-tracking, Property 2: RID uniqueness
# Validates: Requirements 1.3, 4.1
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    resources=st.lists(
        st.tuples(
            st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),  # worker name
            st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),  # worker org
            st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),  # worker type
            st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31))  # res_start
        ),
        min_size=1,
        max_size=10
    )
)
def test_rid_uniqueness(app, clean_db, resources):
    """
    Property 2: RID uniqueness
    For any set of resource records created by the system, all RIDs SHALL be unique.
    """
    with app.app_context():
        rids = []
        for name, org, type_, res_start in resources:
            # Create worker first
            wid = WorkerRepository.create(name, org, type_)
            
            # Create resource
            proc_start = datetime.now()
            rid, version = ResourceRepository.create(
                wid, res_start, INFINITY_DATE, proc_start, INFINITY_DATETIME
            )
            rids.append(rid)
        
        # All RIDs should be unique
        assert len(rids) == len(set(rids)), "RIDs are not unique"


# Feature: worker-resource-tracking, Property 3: Initial version is 1
# Validates: Requirements 1.3
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31))
)
def test_initial_version_is_one(app, clean_db, name, org, type_, res_start):
    """
    Property 3: Initial version is 1
    For any newly created resource (first version), the version number SHALL equal 1.
    """
    with app.app_context():
        # Create worker
        wid = WorkerRepository.create(name, org, type_)
        
        # Create resource
        proc_start = datetime.now()
        rid, version = ResourceRepository.create(
            wid, res_start, INFINITY_DATE, proc_start, INFINITY_DATETIME
        )
        
        # Version should be 1
        assert version == 1, f"Initial version is {version}, expected 1"


# Feature: worker-resource-tracking, Property 4: res_start preservation on creation
# Validates: Requirements 1.4
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31))
)
def test_res_start_preservation(app, clean_db, name, org, type_, res_start):
    """
    Property 4: res_start preservation on creation
    For any resource creation with user-provided res_start date D, 
    the created resource SHALL have res_start equal to D.
    """
    from app.services import ResourceService
    
    with app.app_context():
        # Create worker and resource using service
        wid, rid, version = ResourceService.create_worker_and_resource(
            name, org, type_, res_start
        )
        
        # Retrieve the created resource
        resource = ResourceRepository.get_by_rid_version(rid, version)
        
        # res_start should match the provided value
        assert resource.res_start == res_start, \
            f"res_start is {resource.res_start}, expected {res_start}"


# Feature: worker-resource-tracking, Property 5: res_end defaults to infinity on creation
# Validates: Requirements 1.5
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31))
)
def test_res_end_defaults_to_infinity(app, clean_db, name, org, type_, res_start):
    """
    Property 5: res_end defaults to infinity on creation
    For any newly created resource, res_end SHALL equal the infinity date constant (9999-12-31).
    """
    from app.services import ResourceService
    
    with app.app_context():
        # Create worker and resource using service
        wid, rid, version = ResourceService.create_worker_and_resource(
            name, org, type_, res_start
        )
        
        # Retrieve the created resource
        resource = ResourceRepository.get_by_rid_version(rid, version)
        
        # res_end should be infinity
        assert resource.res_end == INFINITY_DATE, \
            f"res_end is {resource.res_end}, expected {INFINITY_DATE}"


# Feature: worker-resource-tracking, Property 6: proc_start set to current time on creation
# Validates: Requirements 1.6
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31))
)
def test_proc_start_set_to_current_time(app, clean_db, name, org, type_, res_start):
    """
    Property 6: proc_start set to current time on creation
    For any newly created resource, proc_start SHALL be within a reasonable 
    time window (e.g., 1 second) of the current system datetime.
    """
    from app.services import ResourceService
    
    with app.app_context():
        # Capture time before creation
        before = datetime.now()
        
        # Create worker and resource using service
        wid, rid, version = ResourceService.create_worker_and_resource(
            name, org, type_, res_start
        )
        
        # Capture time after creation
        after = datetime.now()
        
        # Retrieve the created resource
        resource = ResourceRepository.get_by_rid_version(rid, version)
        
        # proc_start should be between before and after (within 1 second window)
        assert before <= resource.proc_start <= after, \
            f"proc_start {resource.proc_start} is not between {before} and {after}"
        
        # Additional check: should be within 1 second of current time
        time_diff = abs((resource.proc_start - before).total_seconds())
        assert time_diff <= 1.0, \
            f"proc_start is {time_diff} seconds from creation time, expected <= 1.0"


# Feature: worker-resource-tracking, Property 7: proc_end defaults to infinity on creation
# Validates: Requirements 1.7
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31))
)
def test_proc_end_defaults_to_infinity(app, clean_db, name, org, type_, res_start):
    """
    Property 7: proc_end defaults to infinity on creation
    For any newly created resource, proc_end SHALL equal the infinity 
    datetime constant (9999-12-31 23:59:00).
    """
    from app.services import ResourceService
    
    with app.app_context():
        # Create worker and resource using service
        wid, rid, version = ResourceService.create_worker_and_resource(
            name, org, type_, res_start
        )
        
        # Retrieve the created resource
        resource = ResourceRepository.get_by_rid_version(rid, version)
        
        # proc_end should be infinity
        assert resource.proc_end == INFINITY_DATETIME, \
            f"proc_end is {resource.proc_end}, expected {INFINITY_DATETIME}"


# Feature: worker-resource-tracking, Property 8: Referential integrity on creation
# Validates: Requirements 1.8, 4.3
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31))
)
def test_referential_integrity_on_creation(app, clean_db, name, org, type_, res_start):
    """
    Property 8: Referential integrity on creation
    For any resource record created, the WID SHALL exist in the worker table.
    """
    from app.services import ResourceService
    
    with app.app_context():
        # Create worker and resource using service
        wid, rid, version = ResourceService.create_worker_and_resource(
            name, org, type_, res_start
        )
        
        # Retrieve the created resource
        resource = ResourceRepository.get_by_rid_version(rid, version)
        
        # Verify the WID exists in the worker table
        worker = WorkerRepository.get_by_wid(resource.WID)
        assert worker is not None, \
            f"Worker with WID {resource.WID} does not exist"
        
        # Verify the WID matches
        assert worker.WID == wid, \
            f"Worker WID {worker.WID} does not match resource WID {wid}"


# Feature: worker-resource-tracking, Property 9: Old version closed on update
# Validates: Requirements 2.1
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31)),
    new_res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31))
)
def test_old_version_closed_on_update(app, clean_db, name, org, type_, res_start, new_res_start):
    """
    Property 9: Old version closed on update
    For any resource update operation, the previous version's proc_end SHALL be 
    set to the current system datetime (within a reasonable time window).
    """
    from app.services import ResourceService
    
    with app.app_context():
        # Create worker and resource
        wid, rid, version = ResourceService.create_worker_and_resource(
            name, org, type_, res_start
        )
        
        # Capture time before update
        before = datetime.now()
        
        # Update the resource
        ResourceService.update_resource(rid, res_start=new_res_start)
        
        # Capture time after update
        after = datetime.now()
        
        # Retrieve the old version
        old_version = ResourceRepository.get_by_rid_version(rid, 1)
        
        # Old version's proc_end should be between before and after
        assert before <= old_version.proc_end <= after, \
            f"Old version proc_end {old_version.proc_end} is not between {before} and {after}"
        
        # Old version's proc_end should NOT be infinity
        assert old_version.proc_end != INFINITY_DATETIME, \
            f"Old version proc_end is still infinity"


# Feature: worker-resource-tracking, Property 10: Version increment on update
# Validates: Requirements 2.2
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2020, 12, 31)),
    new_res_end=st.dates(min_value=date(2020, 1, 1), max_value=date(2030, 12, 31))
)
def test_version_increment_on_update(app, clean_db, name, org, type_, res_start, new_res_end):
    """
    Property 10: Version increment on update
    For any resource update operation, the new version number SHALL equal 
    the previous version number plus 1.
    """
    from app.services import ResourceService
    
    with app.app_context():
        # Create worker and resource
        wid, rid, version = ResourceService.create_worker_and_resource(
            name, org, type_, res_start
        )
        
        # Update the resource (new_res_end will be >= res_start due to date ranges)
        updated_rid, new_version = ResourceService.update_resource(rid, res_end=new_res_end)
        
        # New version should be old version + 1
        assert new_version == version + 1, \
            f"New version is {new_version}, expected {version + 1}"


# Feature: worker-resource-tracking, Property 11: RID and WID preservation across versions
# Validates: Requirements 2.3
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31)),
    new_res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31))
)
def test_rid_wid_preservation_across_versions(app, clean_db, name, org, type_, res_start, new_res_start):
    """
    Property 11: RID and WID preservation across versions
    For any resource update operation, the new version SHALL have the same 
    RID and WID as the previous version.
    """
    from app.services import ResourceService
    
    with app.app_context():
        # Create worker and resource
        wid, rid, version = ResourceService.create_worker_and_resource(
            name, org, type_, res_start
        )
        
        # Get the original resource
        original = ResourceRepository.get_by_rid_version(rid, version)
        
        # Update the resource
        updated_rid, new_version = ResourceService.update_resource(rid, res_start=new_res_start)
        
        # Get the new version
        new_resource = ResourceRepository.get_by_rid_version(updated_rid, new_version)
        
        # RID should be preserved
        assert new_resource.RID == original.RID, \
            f"RID changed from {original.RID} to {new_resource.RID}"
        
        # WID should be preserved
        assert new_resource.WID == original.WID, \
            f"WID changed from {original.WID} to {new_resource.WID}"


# Feature: worker-resource-tracking, Property 12: Temporal continuity across versions
# Validates: Requirements 2.4
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2020, 12, 31)),
    new_res_end=st.dates(min_value=date(2020, 1, 1), max_value=date(2030, 12, 31))
)
def test_temporal_continuity_across_versions(app, clean_db, name, org, type_, res_start, new_res_end):
    """
    Property 12: Temporal continuity across versions
    For any resource update operation, the new version's proc_start SHALL 
    equal the previous version's proc_end.
    """
    from app.services import ResourceService
    
    with app.app_context():
        # Create worker and resource
        wid, rid, version = ResourceService.create_worker_and_resource(
            name, org, type_, res_start
        )
        
        # Update the resource (new_res_end will be >= res_start due to date ranges)
        updated_rid, new_version = ResourceService.update_resource(rid, res_end=new_res_end)
        
        # Get both versions
        old_version = ResourceRepository.get_by_rid_version(rid, 1)
        new_resource = ResourceRepository.get_by_rid_version(updated_rid, new_version)
        
        # New version's proc_start should equal old version's proc_end
        assert new_resource.proc_start == old_version.proc_end, \
            f"New proc_start {new_resource.proc_start} != old proc_end {old_version.proc_end}"


# Feature: worker-resource-tracking, Property 13: New version proc_end defaults to infinity
# Validates: Requirements 2.5
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31)),
    new_res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31))
)
def test_new_version_proc_end_defaults_to_infinity(app, clean_db, name, org, type_, res_start, new_res_start):
    """
    Property 13: New version proc_end defaults to infinity
    For any resource update operation, the new version's proc_end SHALL equal 
    the infinity datetime constant (9999-12-31 23:59:00).
    """
    from app.services import ResourceService
    
    with app.app_context():
        # Create worker and resource
        wid, rid, version = ResourceService.create_worker_and_resource(
            name, org, type_, res_start
        )
        
        # Update the resource
        updated_rid, new_version = ResourceService.update_resource(rid, res_start=new_res_start)
        
        # Get the new version
        new_resource = ResourceRepository.get_by_rid_version(updated_rid, new_version)
        
        # New version's proc_end should be infinity
        assert new_resource.proc_end == INFINITY_DATETIME, \
            f"New version proc_end is {new_resource.proc_end}, expected {INFINITY_DATETIME}"


# Feature: worker-resource-tracking, Property 14: User input applied on update
# Validates: Requirements 2.6
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2015, 12, 31)),
    update_choice=st.sampled_from(['res_start', 'res_end', 'both']),
    new_res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2015, 12, 31)),
    new_res_end=st.dates(min_value=date(2015, 1, 1), max_value=date(2030, 12, 31))
)
def test_user_input_applied_on_update(app, clean_db, name, org, type_, res_start, 
                                      update_choice, new_res_start, new_res_end):
    """
    Property 14: User input applied on update
    For any resource update operation with user-provided res_start and/or res_end values, 
    the new version SHALL have the provided values for those fields, and SHALL copy 
    the unprovided values from the previous version.
    """
    from app.services import ResourceService
    from app.validation import ValidationError
    
    with app.app_context():
        # Create worker and resource
        wid, rid, version = ResourceService.create_worker_and_resource(
            name, org, type_, res_start
        )
        
        # Get the original resource
        original = ResourceRepository.get_by_rid_version(rid, version)
        
        # Update based on choice, but only if the result would be valid
        try:
            if update_choice == 'res_start':
                # new_res_start must be <= original.res_end (which is INFINITY_DATE)
                # This is always true, so we can proceed
                updated_rid, new_version = ResourceService.update_resource(rid, res_start=new_res_start)
                expected_res_start = new_res_start
                expected_res_end = original.res_end  # Should be copied
            elif update_choice == 'res_end':
                # original.res_start must be <= new_res_end
                if original.res_start > new_res_end:
                    # Skip this test case as it would violate validation
                    return
                updated_rid, new_version = ResourceService.update_resource(rid, res_end=new_res_end)
                expected_res_start = original.res_start  # Should be copied
                expected_res_end = new_res_end
            else:  # both
                # new_res_start must be <= new_res_end
                if new_res_start > new_res_end:
                    # Skip this test case as it would violate validation
                    return
                updated_rid, new_version = ResourceService.update_resource(
                    rid, res_start=new_res_start, res_end=new_res_end
                )
                expected_res_start = new_res_start
                expected_res_end = new_res_end
        except ValidationError:
            # If validation error occurs, skip this test case
            return
        
        # Get the new version
        new_resource = ResourceRepository.get_by_rid_version(updated_rid, new_version)
        
        # Check that values match expectations
        assert new_resource.res_start == expected_res_start, \
            f"res_start is {new_resource.res_start}, expected {expected_res_start}"
        assert new_resource.res_end == expected_res_end, \
            f"res_end is {new_resource.res_end}, expected {expected_res_end}"


# Feature: worker-resource-tracking, Property 15: Historical preservation
# Validates: Requirements 2.7
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31)),
    num_updates=st.integers(min_value=1, max_value=5)
)
def test_historical_preservation(app, clean_db, name, org, type_, res_start, num_updates):
    """
    Property 15: Historical preservation
    For any resource with RID R that has been updated N times, there SHALL exist 
    N+1 versions in the database with sequential version numbers from 1 to N+1.
    """
    from app.services import ResourceService
    
    with app.app_context():
        # Create worker and resource
        wid, rid, version = ResourceService.create_worker_and_resource(
            name, org, type_, res_start
        )
        
        # Perform N updates
        for i in range(num_updates):
            new_date = date(2000 + i, 1, 1)
            ResourceService.update_resource(rid, res_start=new_date)
        
        # Get all versions
        all_versions = ResourceRepository.get_all_versions(rid)
        
        # Should have N+1 versions
        expected_count = num_updates + 1
        assert len(all_versions) == expected_count, \
            f"Found {len(all_versions)} versions, expected {expected_count}"
        
        # Version numbers should be sequential from 1 to N+1
        version_numbers = [v.version for v in all_versions]
        expected_versions = list(range(1, expected_count + 1))
        assert version_numbers == expected_versions, \
            f"Version numbers are {version_numbers}, expected {expected_versions}"


# Feature: worker-resource-tracking, Property 16: Active resources filter
# Validates: Requirements 3.1
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    resources=st.lists(
        st.tuples(
            st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),  # name
            st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),  # org
            st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),  # type
            st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31))   # res_start
        ),
        min_size=1,
        max_size=5
    ),
    num_to_update=st.integers(min_value=0, max_value=3)
)
def test_active_resources_filter(app, clean_db, resources, num_to_update):
    """
    Property 16: Active resources filter
    For any query for active resources, all returned resources SHALL have 
    proc_end equal to the infinity datetime constant.
    """
    from app.services import ResourceService
    from app.database import get_db
    
    with app.app_context():
        # Clean database for this hypothesis example
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE resource, worker RESTART IDENTITY CASCADE")
            cursor.execute("ALTER SEQUENCE resource_rid_seq RESTART WITH 1")
        
        # Create multiple resources
        created_rids = []
        for name, org, type_, res_start in resources:
            wid, rid, version = ResourceService.create_worker_and_resource(
                name, org, type_, res_start
            )
            created_rids.append(rid)
        
        # Update some resources to create historical versions
        num_to_update = min(num_to_update, len(created_rids))
        for i in range(num_to_update):
            new_date = date(2010, 1, 1)
            ResourceService.update_resource(created_rids[i], res_start=new_date)
        
        # Get active resources
        active_resources = ResourceService.get_active_resources()
        
        # All returned resources should have proc_end = infinity
        for resource in active_resources:
            assert resource['proc_end'] == INFINITY_DATETIME, \
                f"Active resource has proc_end {resource['proc_end']}, expected {INFINITY_DATETIME}"
        
        # Should return exactly the number of created resources (one active version per resource)
        assert len(active_resources) == len(created_rids), \
            f"Found {len(active_resources)} active resources, expected {len(created_rids)}"


# Feature: worker-resource-tracking, Property 17: Active resources display completeness
# Validates: Requirements 3.2, 6.4
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31))
)
def test_active_resources_display_completeness(app, clean_db, name, org, type_, res_start):
    """
    Property 17: Active resources display completeness
    For any active resource returned, the result SHALL include RID, version, WID, 
    name, org, type, res_start, res_end, proc_start, and proc_end.
    """
    from app.services import ResourceService
    from app.database import get_db
    
    with app.app_context():
        # Clean database for this hypothesis example
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE resource, worker RESTART IDENTITY CASCADE")
            cursor.execute("ALTER SEQUENCE resource_rid_seq RESTART WITH 1")
        
        # Create a worker and resource
        wid, rid, version = ResourceService.create_worker_and_resource(
            name, org, type_, res_start
        )
        
        # Get active resources
        active_resources = ResourceService.get_active_resources()
        
        # Should have at least one resource
        assert len(active_resources) > 0, "No active resources returned"
        
        # Check that all required fields are present in each resource
        required_fields = ['rid', 'version', 'wid', 'name', 'org', 'type', 
                          'res_start', 'res_end', 'proc_start', 'proc_end']
        
        for resource in active_resources:
            for field in required_fields:
                assert field in resource, \
                    f"Required field '{field}' is missing from resource"
                assert resource[field] is not None, \
                    f"Required field '{field}' is None"


# Feature: worker-resource-tracking, Property 18: Worker-resource join correctness
# Validates: Requirements 3.3, 6.5
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31))
)
def test_worker_resource_join_correctness(app, clean_db, name, org, type_, res_start):
    """
    Property 18: Worker-resource join correctness
    For any resource returned (active or as-of query), the worker fields 
    (name, org, type) SHALL match the worker record with the same WID.
    """
    from app.services import ResourceService
    from app.database import get_db
    
    with app.app_context():
        # Clean database for this hypothesis example
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE resource, worker RESTART IDENTITY CASCADE")
            cursor.execute("ALTER SEQUENCE resource_rid_seq RESTART WITH 1")
        
        # Create a worker and resource
        wid, rid, version = ResourceService.create_worker_and_resource(
            name, org, type_, res_start
        )
        
        # Get active resources
        active_resources = ResourceService.get_active_resources()
        
        # Should have at least one resource
        assert len(active_resources) > 0, "No active resources returned"
        
        # For each resource, verify the worker fields match the worker record
        for resource in active_resources:
            # Get the worker record directly
            worker = WorkerRepository.get_by_wid(resource['wid'])
            
            assert worker is not None, \
                f"Worker with WID {resource['wid']} not found"
            
            # Verify the worker fields match
            assert resource['name'] == worker.name, \
                f"Resource name '{resource['name']}' does not match worker name '{worker.name}'"
            assert resource['org'] == worker.org, \
                f"Resource org '{resource['org']}' does not match worker org '{worker.org}'"
            assert resource['type'] == worker.type, \
                f"Resource type '{resource['type']}' does not match worker type '{worker.type}'"


# Feature: worker-resource-tracking, Property 19: As-of query default processing datetime
# Validates: Requirements 6.2
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31)),
    business_date=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31))
)
def test_as_of_query_default_processing_datetime(app, clean_db, name, org, type_, res_start, business_date):
    """
    Property 19: As-of query default processing datetime
    For any as-of query with only business date D specified, the processing datetime 
    SHALL default to the current system datetime (within a reasonable time window).
    """
    from app.services import ResourceService
    from app.database import get_db
    
    with app.app_context():
        # Clean database for this hypothesis example
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE resource, worker RESTART IDENTITY CASCADE")
            cursor.execute("ALTER SEQUENCE resource_rid_seq RESTART WITH 1")
        
        # Create a worker and resource
        wid, rid, version = ResourceService.create_worker_and_resource(
            name, org, type_, res_start
        )
        
        # Capture time before query
        before = datetime.now()
        
        # Execute as-of query without processing_datetime (should default to now)
        results = ResourceService.as_of_query(business_date)
        
        # Capture time after query
        after = datetime.now()
        
        # The query should have used a processing datetime between before and after
        # We can verify this by checking that the query returns the resource if it's valid
        # for the business_date at the current time
        
        # Get the created resource to check its temporal bounds
        resource = ResourceRepository.get_by_rid_version(rid, version)
        
        # If the business_date falls within the resource's business time range
        # and the current time falls within the resource's processing time range,
        # then the resource should be returned
        if (resource.res_start <= business_date < resource.res_end and
            resource.proc_start <= before and resource.proc_end > after):
            # Resource should be in results
            assert len(results) > 0, \
                "Resource should be returned when business_date and current time are valid"
            
            # Verify the returned resource is the one we created
            found = any(r['rid'] == rid for r in results)
            assert found, f"Created resource with RID {rid} not found in results"
        
        # The key property is that calling without processing_datetime should behave
        # the same as calling with processing_datetime=datetime.now()
        # We verify this by ensuring the query executed successfully and returned
        # results consistent with the current time being used as processing_datetime


# Feature: worker-resource-tracking, Property 20: Bi-temporal query correctness
# Validates: Requirements 6.3
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2020, 12, 31)),
    res_end=st.dates(min_value=date(2021, 1, 1), max_value=date(2030, 12, 31)),
    business_date=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31)),
    processing_datetime=st.datetimes(min_value=datetime(2000, 1, 1), max_value=datetime(2030, 12, 31))
)
def test_bi_temporal_query_correctness(app, clean_db, name, org, type_, res_start, 
                                       res_end, business_date, processing_datetime):
    """
    Property 20: Bi-temporal query correctness
    For any as-of query with business date D and processing datetime P, all returned 
    resources SHALL satisfy: proc_start <= P AND proc_end > P AND res_start <= D AND res_end > D.
    """
    from app.services import ResourceService
    from app.database import get_db
    
    with app.app_context():
        # Clean database for this hypothesis example
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE resource, worker RESTART IDENTITY CASCADE")
            cursor.execute("ALTER SEQUENCE resource_rid_seq RESTART WITH 1")
        
        # Create a worker and resource with specific temporal bounds
        wid, rid, version = ResourceService.create_worker_and_resource(
            name, org, type_, res_start
        )
        
        # Update the resource to set a specific res_end (not infinity)
        ResourceService.update_resource(rid, res_end=res_end)
        
        # Execute as-of query with specific business_date and processing_datetime
        results = ResourceService.as_of_query(business_date, processing_datetime)
        
        # Verify that all returned resources satisfy the bi-temporal conditions
        for resource in results:
            proc_start = resource['proc_start']
            proc_end = resource['proc_end']
            r_start = resource['res_start']
            r_end = resource['res_end']
            
            # Check processing time condition: proc_start <= P AND proc_end > P
            assert proc_start <= processing_datetime, \
                f"Resource proc_start {proc_start} is after query processing_datetime {processing_datetime}"
            assert proc_end > processing_datetime, \
                f"Resource proc_end {proc_end} is not after query processing_datetime {processing_datetime}"
            
            # Check business time condition: res_start <= D AND res_end > D
            assert r_start <= business_date, \
                f"Resource res_start {r_start} is after query business_date {business_date}"
            assert r_end > business_date, \
                f"Resource res_end {r_end} is not after query business_date {business_date}"
        
        # Additionally, verify that if a resource should be included, it is included
        # Get all versions of the resource we created
        all_versions = ResourceRepository.get_all_versions(rid)
        
        for resource in all_versions:
            # Check if this version should be in the results
            should_be_included = (
                resource.proc_start <= processing_datetime and
                resource.proc_end > processing_datetime and
                resource.res_start <= business_date and
                resource.res_end > business_date
            )
            
            if should_be_included:
                # Verify it's in the results
                found = any(
                    r['rid'] == resource.RID and r['version'] == resource.version
                    for r in results
                )
                assert found, \
                    f"Resource RID={resource.RID} version={resource.version} should be in results but is not"


# Feature: worker-resource-tracking, Property 21: Processing time validity
# Validates: Requirements 4.4
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31))
)
def test_processing_time_validity(app, clean_db, name, org, type_, res_start):
    """
    Property 21: Processing time validity
    For any resource record (created or updated), proc_start SHALL be less than 
    or equal to proc_end.
    """
    from app.services import ResourceService
    from app.database import get_db
    
    with app.app_context():
        # Clean database for this hypothesis example
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE resource, worker RESTART IDENTITY CASCADE")
            cursor.execute("ALTER SEQUENCE resource_rid_seq RESTART WITH 1")
        
        # Create a worker and resource
        wid, rid, version = ResourceService.create_worker_and_resource(
            name, org, type_, res_start
        )
        
        # Get the created resource
        resource = ResourceRepository.get_by_rid_version(rid, version)
        
        # Verify proc_start <= proc_end
        assert resource.proc_start <= resource.proc_end, \
            f"proc_start {resource.proc_start} is greater than proc_end {resource.proc_end}"
        
        # Update the resource to create a new version
        new_date = date(2010, 1, 1)
        updated_rid, new_version = ResourceService.update_resource(rid, res_start=new_date)
        
        # Get all versions and verify they all satisfy the constraint
        all_versions = ResourceRepository.get_all_versions(rid)
        
        for v in all_versions:
            assert v.proc_start <= v.proc_end, \
                f"Version {v.version}: proc_start {v.proc_start} is greater than proc_end {v.proc_end}"


# Feature: worker-resource-tracking, Property 22: Business time validity
# Validates: Requirements 4.5
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31)),
    res_end=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31))
)
def test_business_time_validity(app, clean_db, name, org, type_, res_start, res_end):
    """
    Property 22: Business time validity
    For any resource record (created or updated), res_start SHALL be less than 
    or equal to res_end.
    """
    from app.services import ResourceService
    from app.database import get_db
    from app.validation import ValidationError
    
    with app.app_context():
        # Clean database for this hypothesis example
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE resource, worker RESTART IDENTITY CASCADE")
            cursor.execute("ALTER SEQUENCE resource_rid_seq RESTART WITH 1")
        
        # Create a worker and resource
        wid, rid, version = ResourceService.create_worker_and_resource(
            name, org, type_, res_start
        )
        
        # Get the created resource
        resource = ResourceRepository.get_by_rid_version(rid, version)
        
        # Verify res_start <= res_end
        assert resource.res_start <= resource.res_end, \
            f"res_start {resource.res_start} is greater than res_end {resource.res_end}"
        
        # Try to update with valid or invalid date range
        if res_start <= res_end:
            # Valid range - should succeed
            updated_rid, new_version = ResourceService.update_resource(
                rid, res_start=res_start, res_end=res_end
            )
            
            # Get the new version
            new_resource = ResourceRepository.get_by_rid_version(updated_rid, new_version)
            
            # Verify res_start <= res_end
            assert new_resource.res_start <= new_resource.res_end, \
                f"Updated resource: res_start {new_resource.res_start} is greater than res_end {new_resource.res_end}"
        else:
            # Invalid range - should raise ValidationError
            try:
                ResourceService.update_resource(rid, res_start=res_start, res_end=res_end)
                # If we get here, the validation failed to catch the error
                assert False, f"Expected ValidationError for res_start {res_start} > res_end {res_end}"
            except ValidationError:
                # Expected - validation caught the error
                pass
        
        # Verify all versions satisfy the constraint
        all_versions = ResourceRepository.get_all_versions(rid)
        
        for v in all_versions:
            assert v.res_start <= v.res_end, \
                f"Version {v.version}: res_start {v.res_start} is greater than res_end {v.res_end}"


# Feature: worker-resource-tracking, Property 23: Single active version per resource
# Validates: Requirements 4.6
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31)),
    num_updates=st.integers(min_value=0, max_value=5)
)
def test_single_active_version_per_resource(app, clean_db, name, org, type_, res_start, num_updates):
    """
    Property 23: Single active version per resource
    For any RID with multiple versions, exactly one version SHALL have proc_end 
    equal to the infinity datetime constant.
    """
    from app.services import ResourceService
    from app.database import get_db
    
    with app.app_context():
        # Clean database for this hypothesis example
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE resource, worker RESTART IDENTITY CASCADE")
            cursor.execute("ALTER SEQUENCE resource_rid_seq RESTART WITH 1")
        
        # Create a worker and resource
        wid, rid, version = ResourceService.create_worker_and_resource(
            name, org, type_, res_start
        )
        
        # Perform N updates
        for i in range(num_updates):
            new_date = date(2000 + i, 1, 1)
            ResourceService.update_resource(rid, res_start=new_date)
        
        # Get all versions of the resource
        all_versions = ResourceRepository.get_all_versions(rid)
        
        # Count how many versions have proc_end = infinity
        active_versions = [v for v in all_versions if v.proc_end == INFINITY_DATETIME]
        
        # Should have exactly one active version
        assert len(active_versions) == 1, \
            f"Found {len(active_versions)} active versions for RID {rid}, expected exactly 1"
        
        # The active version should be the latest version
        latest_version = max(v.version for v in all_versions)
        assert active_versions[0].version == latest_version, \
            f"Active version is {active_versions[0].version}, expected {latest_version}"


# Feature: worker-resource-tracking, Property 24: Sequential version numbering
# Validates: Requirements 4.7
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(
    name=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    org=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    type_=st.text(min_size=1, max_size=50).filter(lambda x: '\x00' not in x and x.strip()),
    res_start=st.dates(min_value=date(2000, 1, 1), max_value=date(2030, 12, 31)),
    num_updates=st.integers(min_value=1, max_value=5)
)
def test_sequential_version_numbering(app, clean_db, name, org, type_, res_start, num_updates):
    """
    Property 24: Sequential version numbering
    For any RID with N versions, the version numbers SHALL be exactly {1, 2, 3, ..., N} 
    with no gaps or duplicates.
    """
    from app.services import ResourceService
    from app.database import get_db
    
    with app.app_context():
        # Clean database for this hypothesis example
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE resource, worker RESTART IDENTITY CASCADE")
            cursor.execute("ALTER SEQUENCE resource_rid_seq RESTART WITH 1")
        
        # Create a worker and resource
        wid, rid, version = ResourceService.create_worker_and_resource(
            name, org, type_, res_start
        )
        
        # Perform N updates
        for i in range(num_updates):
            new_date = date(2000 + i, 1, 1)
            ResourceService.update_resource(rid, res_start=new_date)
        
        # Get all versions of the resource
        all_versions = ResourceRepository.get_all_versions(rid)
        
        # Total number of versions should be num_updates + 1 (initial + updates)
        expected_count = num_updates + 1
        assert len(all_versions) == expected_count, \
            f"Found {len(all_versions)} versions, expected {expected_count}"
        
        # Extract version numbers
        version_numbers = sorted([v.version for v in all_versions])
        
        # Expected version numbers: [1, 2, 3, ..., N]
        expected_versions = list(range(1, expected_count + 1))
        
        # Verify version numbers are sequential with no gaps or duplicates
        assert version_numbers == expected_versions, \
            f"Version numbers are {version_numbers}, expected {expected_versions}"
        
        # Verify no duplicates (set should have same length as list)
        assert len(set(version_numbers)) == len(version_numbers), \
            f"Found duplicate version numbers: {version_numbers}"
        
        # Verify no gaps (each version should be previous + 1)
        for i in range(1, len(version_numbers)):
            assert version_numbers[i] == version_numbers[i-1] + 1, \
                f"Gap found between version {version_numbers[i-1]} and {version_numbers[i]}"
