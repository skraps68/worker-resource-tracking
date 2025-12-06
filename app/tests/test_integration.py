"""Integration tests for end-to-end workflows."""
import pytest
from datetime import date, datetime, timedelta
from app.models import INFINITY_DATE, INFINITY_DATETIME


class TestEndToEndWorkflows:
    """Test complete end-to-end workflows through the API."""
    
    def test_create_worker_and_resource_workflow(self, client, clean_db):
        """Test creating worker and resource through UI workflow.
        
        This simulates a user:
        1. Opening the creation panel
        2. Filling in worker details
        3. Submitting the form
        4. Verifying the resource appears in active resources
        """
        # Step 1: Create worker and resource
        create_response = client.post('/api/workers', json={
            'name': 'Alice Johnson',
            'org': 'Engineering',
            'type': 'Software Engineer',
            'res_start': '2024-01-15'
        })
        
        assert create_response.status_code == 201
        create_data = create_response.get_json()
        wid = create_data['WID']
        rid = create_data['RID']
        
        # Verify creation response
        assert wid > 0
        assert rid > 0
        assert create_data['version'] == 1
        
        # Step 2: Verify resource appears in active resources
        active_response = client.get('/api/resources/active')
        assert active_response.status_code == 200
        active_data = active_response.get_json()
        
        assert len(active_data) == 1
        resource = active_data[0]
        
        # Verify all fields are present and correct
        assert resource['RID'] == rid
        assert resource['version'] == 1
        assert resource['WID'] == wid
        assert resource['name'] == 'Alice Johnson'
        assert resource['org'] == 'Engineering'
        assert resource['type'] == 'Software Engineer'
        assert resource['res_start'] == '2024-01-15'
        assert resource['res_end'] == '9999-12-31'
        assert 'proc_start' in resource
        assert resource['proc_end'] == '9999-12-31T23:59:00'
    
    def test_update_resource_workflow(self, client, clean_db):
        """Test updating resource through UI workflow.
        
        This simulates a user:
        1. Creating a worker and resource
        2. Viewing active resources to find the RID
        3. Updating the resource dates
        4. Verifying the update appears in active resources
        """
        # Step 1: Create initial worker and resource
        create_response = client.post('/api/workers', json={
            'name': 'Bob Smith',
            'org': 'Marketing',
            'type': 'Marketing Manager',
            'res_start': '2024-01-01'
        })
        
        rid = create_response.get_json()['RID']
        
        # Step 2: View active resources (simulating user finding the RID)
        active_response = client.get('/api/resources/active')
        active_data = active_response.get_json()
        assert len(active_data) == 1
        assert active_data[0]['RID'] == rid
        assert active_data[0]['version'] == 1
        
        # Step 3: Update the resource
        update_response = client.put(f'/api/resources/{rid}', json={
            'res_start': '2024-02-01',
            'res_end': '2024-12-31'
        })
        
        assert update_response.status_code == 200
        update_data = update_response.get_json()
        assert update_data['RID'] == rid
        assert update_data['version'] == 2
        
        # Step 4: Verify updated resource in active resources
        active_response = client.get('/api/resources/active')
        active_data = active_response.get_json()
        
        assert len(active_data) == 1
        resource = active_data[0]
        assert resource['RID'] == rid
        assert resource['version'] == 2
        assert resource['res_start'] == '2024-02-01'
        assert resource['res_end'] == '2024-12-31'
    
    def test_view_active_resources_workflow(self, client, clean_db):
        """Test viewing active resources through UI workflow.
        
        This simulates a user:
        1. Creating multiple workers and resources
        2. Updating some resources
        3. Viewing the active resources list
        4. Verifying only current versions are shown
        """
        # Step 1: Create multiple workers and resources
        workers = [
            {'name': 'Carol White', 'org': 'Sales', 'type': 'Sales Rep', 'res_start': '2024-01-01'},
            {'name': 'David Brown', 'org': 'HR', 'type': 'HR Manager', 'res_start': '2024-02-01'},
            {'name': 'Eve Davis', 'org': 'Finance', 'type': 'Accountant', 'res_start': '2024-03-01'}
        ]
        
        rids = []
        for worker in workers:
            response = client.post('/api/workers', json=worker)
            rids.append(response.get_json()['RID'])
        
        # Step 2: Update one of the resources
        client.put(f'/api/resources/{rids[0]}', json={
            'res_end': '2024-06-30'
        })
        
        # Step 3: View active resources
        active_response = client.get('/api/resources/active')
        active_data = active_response.get_json()
        
        # Step 4: Verify results
        assert len(active_data) == 3
        
        # Verify first resource has version 2 (was updated)
        carol_resource = [r for r in active_data if r['name'] == 'Carol White'][0]
        assert carol_resource['version'] == 2
        assert carol_resource['res_end'] == '2024-06-30'
        
        # Verify other resources have version 1
        david_resource = [r for r in active_data if r['name'] == 'David Brown'][0]
        assert david_resource['version'] == 1
        
        eve_resource = [r for r in active_data if r['name'] == 'Eve Davis'][0]
        assert eve_resource['version'] == 1
    
    def test_as_of_query_workflow(self, client, clean_db):
        """Test executing as-of queries through UI workflow.
        
        This simulates a user:
        1. Creating a resource
        2. Updating it multiple times
        3. Executing as-of queries at different points in time
        4. Verifying correct historical data is returned
        """
        # Step 1: Create initial resource
        create_response = client.post('/api/workers', json={
            'name': 'Frank Miller',
            'org': 'Operations',
            'type': 'Operations Manager',
            'res_start': '2024-01-01'
        })
        
        rid = create_response.get_json()['RID']
        
        # Step 2: Make multiple updates with different dates
        # Update 1: Change res_end
        client.put(f'/api/resources/{rid}', json={
            'res_end': '2024-06-30'
        })
        
        # Update 2: Change res_start
        client.put(f'/api/resources/{rid}', json={
            'res_start': '2024-02-01'
        })
        
        # Update 3: Change both dates
        client.put(f'/api/resources/{rid}', json={
            'res_start': '2024-03-01',
            'res_end': '2024-09-30'
        })
        
        # Step 3: Execute as-of queries
        
        # Query 1: Business date within original range
        query1 = client.get('/api/resources/as-of?business_date=2024-03-15')
        data1 = query1.get_json()
        assert len(data1) == 1
        assert data1[0]['RID'] == rid
        
        # Query 2: Business date before res_start (should return nothing)
        query2 = client.get('/api/resources/as-of?business_date=2023-12-31')
        data2 = query2.get_json()
        assert len(data2) == 0
        
        # Query 3: Business date after res_end (should return nothing)
        query3 = client.get('/api/resources/as-of?business_date=2024-12-31')
        data3 = query3.get_json()
        assert len(data3) == 0
        
        # Query 4: Business date within current range
        query4 = client.get('/api/resources/as-of?business_date=2024-06-15')
        data4 = query4.get_json()
        assert len(data4) == 1
        assert data4[0]['version'] == 4  # Latest version
        assert data4[0]['res_start'] == '2024-03-01'
        assert data4[0]['res_end'] == '2024-09-30'


class TestCompleteWorkerLifecycle:
    """Test complete worker lifecycle with multiple updates and queries."""
    
    def test_worker_lifecycle_create_update_query_history(self, client, clean_db):
        """Test complete lifecycle: create, update multiple times, query history.
        
        This test validates:
        - Worker creation
        - Multiple resource updates
        - Historical preservation
        - Bi-temporal queries at various points
        """
        # Create worker and resource
        create_response = client.post('/api/workers', json={
            'name': 'Grace Lee',
            'org': 'Product',
            'type': 'Product Manager',
            'res_start': '2024-01-01'
        })
        
        assert create_response.status_code == 201
        rid = create_response.get_json()['RID']
        wid = create_response.get_json()['WID']
        
        # Capture processing time after creation
        import time
        time.sleep(0.1)  # Small delay to ensure different processing times
        
        # Update 1: Extend end date
        update1_response = client.put(f'/api/resources/{rid}', json={
            'res_end': '2024-12-31'
        })
        assert update1_response.status_code == 200
        assert update1_response.get_json()['version'] == 2
        
        time.sleep(0.1)
        
        # Update 2: Adjust start date
        update2_response = client.put(f'/api/resources/{rid}', json={
            'res_start': '2024-01-15'
        })
        assert update2_response.status_code == 200
        assert update2_response.get_json()['version'] == 3
        
        time.sleep(0.1)
        
        # Update 3: Change both dates
        update3_response = client.put(f'/api/resources/{rid}', json={
            'res_start': '2024-02-01',
            'res_end': '2024-11-30'
        })
        assert update3_response.status_code == 200
        assert update3_response.get_json()['version'] == 4
        
        # Verify only one active version
        active_response = client.get('/api/resources/active')
        active_data = active_response.get_json()
        assert len(active_data) == 1
        assert active_data[0]['version'] == 4
        assert active_data[0]['RID'] == rid
        
        # Query at different business dates
        # Should find resource at date within current range
        query1 = client.get('/api/resources/as-of?business_date=2024-06-15')
        data1 = query1.get_json()
        assert len(data1) == 1
        assert data1[0]['version'] == 4
        
        # Should not find resource at date before current res_start
        query2 = client.get('/api/resources/as-of?business_date=2024-01-10')
        data2 = query2.get_json()
        assert len(data2) == 0
        
        # Should not find resource at date after current res_end
        query3 = client.get('/api/resources/as-of?business_date=2024-12-15')
        data3 = query3.get_json()
        assert len(data3) == 0
        
        # Verify historical data is preserved by checking database directly
        # (In a real UI test, this would be done through a history view)
        from app.database import get_db
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT version FROM resource WHERE RID = %s ORDER BY version",
                (rid,)
            )
            versions = [row['version'] for row in cursor.fetchall()]
            assert versions == [1, 2, 3, 4]


class TestBiTemporalQueries:
    """Test bi-temporal queries at various points in time."""
    
    def test_bitemporal_query_with_processing_time(self, client, clean_db):
        """Test bi-temporal queries with explicit processing datetime.
        
        This validates that queries can retrieve historical states
        as they were known at specific processing times.
        """
        # Create resource
        create_response = client.post('/api/workers', json={
            'name': 'Henry Wilson',
            'org': 'Research',
            'type': 'Researcher',
            'res_start': '2024-01-01'
        })
        
        rid = create_response.get_json()['RID']
        
        # Capture processing time after creation
        from datetime import datetime
        proc_time_1 = datetime.now()
        
        import time
        time.sleep(0.2)
        
        # Update resource
        client.put(f'/api/resources/{rid}', json={
            'res_end': '2024-06-30'
        })
        
        proc_time_2 = datetime.now()
        
        time.sleep(0.2)
        
        # Another update
        client.put(f'/api/resources/{rid}', json={
            'res_start': '2024-02-01'
        })
        
        # Query at first processing time (should get version 1)
        query1 = client.get(
            f'/api/resources/as-of?business_date=2024-03-01&'
            f'processing_datetime={proc_time_1.isoformat()}'
        )
        data1 = query1.get_json()
        assert len(data1) == 1
        assert data1[0]['version'] == 1
        assert data1[0]['res_end'] == '9999-12-31'
        
        # Query at second processing time (should get version 2)
        query2 = client.get(
            f'/api/resources/as-of?business_date=2024-03-01&'
            f'processing_datetime={proc_time_2.isoformat()}'
        )
        data2 = query2.get_json()
        assert len(data2) == 1
        assert data2[0]['version'] == 2
        assert data2[0]['res_end'] == '2024-06-30'
        
        # Query at current time (should get version 3)
        query3 = client.get('/api/resources/as-of?business_date=2024-03-01')
        data3 = query3.get_json()
        assert len(data3) == 1
        assert data3[0]['version'] == 3
    
    def test_bitemporal_query_multiple_resources(self, client, clean_db):
        """Test bi-temporal queries with multiple resources.
        
        This validates that queries correctly filter across
        both time dimensions for multiple resources.
        """
        # Create multiple resources with different date ranges
        resources = [
            {'name': 'Iris Chen', 'org': 'Design', 'type': 'Designer', 
             'res_start': '2024-01-01'},
            {'name': 'Jack Taylor', 'org': 'Support', 'type': 'Support Agent', 
             'res_start': '2024-03-01'},
            {'name': 'Karen White', 'org': 'Legal', 'type': 'Lawyer', 
             'res_start': '2024-06-01'}
        ]
        
        rids = []
        for resource in resources:
            response = client.post('/api/workers', json=resource)
            rids.append(response.get_json()['RID'])
        
        # Update first resource to end in June
        client.put(f'/api/resources/{rids[0]}', json={
            'res_end': '2024-06-30'
        })
        
        # Update second resource to end in September
        client.put(f'/api/resources/{rids[1]}', json={
            'res_end': '2024-09-30'
        })
        
        # Query at different business dates
        
        # February: Should find only first resource
        query1 = client.get('/api/resources/as-of?business_date=2024-02-15')
        data1 = query1.get_json()
        assert len(data1) == 1
        assert data1[0]['name'] == 'Iris Chen'
        
        # April: Should find first two resources
        query2 = client.get('/api/resources/as-of?business_date=2024-04-15')
        data2 = query2.get_json()
        assert len(data2) == 2
        names = {r['name'] for r in data2}
        assert names == {'Iris Chen', 'Jack Taylor'}
        
        # July: Should find second and third resources
        query3 = client.get('/api/resources/as-of?business_date=2024-07-15')
        data3 = query3.get_json()
        assert len(data3) == 2
        names = {r['name'] for r in data3}
        assert names == {'Jack Taylor', 'Karen White'}
        
        # November: Should find only third resource
        query4 = client.get('/api/resources/as-of?business_date=2024-11-15')
        data4 = query4.get_json()
        assert len(data4) == 1
        assert data4[0]['name'] == 'Karen White'


class TestConcurrentUpdates:
    """Test concurrent update scenarios."""
    
    def test_sequential_updates_maintain_consistency(self, client, clean_db):
        """Test that sequential updates maintain data consistency.
        
        This validates that multiple updates in sequence
        properly maintain version numbers and temporal continuity.
        """
        # Create resource
        create_response = client.post('/api/workers', json={
            'name': 'Laura Martinez',
            'org': 'Quality',
            'type': 'QA Engineer',
            'res_start': '2024-01-01'
        })
        
        rid = create_response.get_json()['RID']
        
        # Perform 10 sequential updates
        for i in range(10):
            response = client.put(f'/api/resources/{rid}', json={
                'res_start': f'2024-{(i % 12) + 1:02d}-01'
            })
            assert response.status_code == 200
            assert response.get_json()['version'] == i + 2
        
        # Verify only one active version
        active_response = client.get('/api/resources/active')
        active_data = active_response.get_json()
        assert len(active_data) == 1
        assert active_data[0]['version'] == 11
        
        # Verify all versions exist in database
        from app.database import get_db
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) as count FROM resource WHERE RID = %s",
                (rid,)
            )
            count = cursor.fetchone()['count']
            assert count == 11
            
            # Verify version sequence
            cursor.execute(
                "SELECT version FROM resource WHERE RID = %s ORDER BY version",
                (rid,)
            )
            versions = [row['version'] for row in cursor.fetchall()]
            assert versions == list(range(1, 12))
            
            # Verify only one has proc_end = infinity
            cursor.execute(
                "SELECT COUNT(*) as count FROM resource WHERE RID = %s AND proc_end = %s",
                (rid, INFINITY_DATETIME)
            )
            active_count = cursor.fetchone()['count']
            assert active_count == 1
    
    def test_rapid_updates_different_resources(self, client, clean_db):
        """Test rapid updates to different resources.
        
        This validates that the system can handle multiple
        resources being updated in quick succession.
        """
        # Create multiple resources
        rids = []
        for i in range(5):
            response = client.post('/api/workers', json={
                'name': f'Worker {i}',
                'org': f'Org {i}',
                'type': f'Type {i}',
                'res_start': '2024-01-01'
            })
            rids.append(response.get_json()['RID'])
        
        # Update all resources rapidly
        for rid in rids:
            response = client.put(f'/api/resources/{rid}', json={
                'res_end': '2024-12-31'
            })
            assert response.status_code == 200
        
        # Verify all resources are active with version 2
        active_response = client.get('/api/resources/active')
        active_data = active_response.get_json()
        assert len(active_data) == 5
        
        for resource in active_data:
            assert resource['version'] == 2
            assert resource['res_end'] == '2024-12-31'
    
    def test_update_nonexistent_resource(self, client, clean_db):
        """Test attempting to update a resource that doesn't exist.
        
        This validates proper error handling for invalid operations.
        """
        response = client.put('/api/resources/99999', json={
            'res_start': '2024-01-01'
        })
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert '99999' in data['error'] or 'not found' in data['error'].lower()
