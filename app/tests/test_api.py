"""Unit tests for API endpoints."""
import pytest
from datetime import date, datetime
from app.models import INFINITY_DATE, INFINITY_DATETIME


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


class TestCreateWorkerEndpoint:
    """Tests for POST /api/workers endpoint."""
    
    def test_create_worker_success(self, client, clean_db):
        """Test successful worker and resource creation."""
        response = client.post('/api/workers', json={
            'name': 'John Doe',
            'org': 'Engineering',
            'type': 'Developer',
            'res_start': '2024-01-01'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'WID' in data
        assert 'RID' in data
        assert data['version'] == 1
        assert isinstance(data['WID'], int)
        assert isinstance(data['RID'], int)
    
    def test_create_worker_missing_name(self, client, clean_db):
        """Test error when name is missing."""
        response = client.post('/api/workers', json={
            'org': 'Engineering',
            'type': 'Developer',
            'res_start': '2024-01-01'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'name' in data['error'].lower()
    
    def test_create_worker_missing_org(self, client, clean_db):
        """Test error when org is missing."""
        response = client.post('/api/workers', json={
            'name': 'John Doe',
            'type': 'Developer',
            'res_start': '2024-01-01'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'org' in data['error'].lower()
    
    def test_create_worker_missing_type(self, client, clean_db):
        """Test error when type is missing."""
        response = client.post('/api/workers', json={
            'name': 'John Doe',
            'org': 'Engineering',
            'res_start': '2024-01-01'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'type' in data['error'].lower()
    
    def test_create_worker_missing_res_start(self, client, clean_db):
        """Test error when res_start is missing."""
        response = client.post('/api/workers', json={
            'name': 'John Doe',
            'org': 'Engineering',
            'type': 'Developer'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'res_start' in data['error'].lower()
    
    def test_create_worker_invalid_date_format(self, client, clean_db):
        """Test error when res_start has invalid format."""
        response = client.post('/api/workers', json={
            'name': 'John Doe',
            'org': 'Engineering',
            'type': 'Developer',
            'res_start': 'invalid-date'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_create_worker_empty_name(self, client, clean_db):
        """Test error when name is empty."""
        response = client.post('/api/workers', json={
            'name': '',
            'org': 'Engineering',
            'type': 'Developer',
            'res_start': '2024-01-01'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data


class TestUpdateResourceEndpoint:
    """Tests for PUT /api/resources/:rid endpoint."""
    
    def test_update_resource_res_start(self, client, clean_db):
        """Test updating res_start."""
        # Create a worker and resource first
        create_response = client.post('/api/workers', json={
            'name': 'Jane Smith',
            'org': 'Marketing',
            'type': 'Manager',
            'res_start': '2024-01-01'
        })
        rid = create_response.get_json()['RID']
        
        # Update res_start
        response = client.put(f'/api/resources/{rid}', json={
            'res_start': '2024-02-01'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['RID'] == rid
        assert data['version'] == 2
    
    def test_update_resource_res_end(self, client, clean_db):
        """Test updating res_end."""
        # Create a worker and resource first
        create_response = client.post('/api/workers', json={
            'name': 'Bob Johnson',
            'org': 'Sales',
            'type': 'Representative',
            'res_start': '2024-01-01'
        })
        rid = create_response.get_json()['RID']
        
        # Update res_end
        response = client.put(f'/api/resources/{rid}', json={
            'res_end': '2024-12-31'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['RID'] == rid
        assert data['version'] == 2
    
    def test_update_resource_both_dates(self, client, clean_db):
        """Test updating both res_start and res_end."""
        # Create a worker and resource first
        create_response = client.post('/api/workers', json={
            'name': 'Alice Brown',
            'org': 'HR',
            'type': 'Coordinator',
            'res_start': '2024-01-01'
        })
        rid = create_response.get_json()['RID']
        
        # Update both dates
        response = client.put(f'/api/resources/{rid}', json={
            'res_start': '2024-02-01',
            'res_end': '2024-11-30'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['RID'] == rid
        assert data['version'] == 2
    
    def test_update_resource_no_dates(self, client, clean_db):
        """Test error when no dates are provided."""
        # Create a worker and resource first
        create_response = client.post('/api/workers', json={
            'name': 'Charlie Davis',
            'org': 'IT',
            'type': 'Support',
            'res_start': '2024-01-01'
        })
        rid = create_response.get_json()['RID']
        
        # Try to update without dates
        response = client.put(f'/api/resources/{rid}', json={})
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'at least one' in data['error'].lower()
    
    def test_update_resource_not_found(self, client, clean_db):
        """Test error when resource doesn't exist."""
        response = client.put('/api/resources/99999', json={
            'res_start': '2024-02-01'
        })
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
    
    def test_update_resource_invalid_date_range(self, client, clean_db):
        """Test error when res_start > res_end."""
        # Create a worker and resource first
        create_response = client.post('/api/workers', json={
            'name': 'David Wilson',
            'org': 'Finance',
            'type': 'Analyst',
            'res_start': '2024-01-01'
        })
        rid = create_response.get_json()['RID']
        
        # Try to update with invalid range
        response = client.put(f'/api/resources/{rid}', json={
            'res_start': '2024-12-31',
            'res_end': '2024-01-01'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_update_resource_invalid_date_format(self, client, clean_db):
        """Test error when date format is invalid."""
        # Create a worker and resource first
        create_response = client.post('/api/workers', json={
            'name': 'Eve Martinez',
            'org': 'Operations',
            'type': 'Supervisor',
            'res_start': '2024-01-01'
        })
        rid = create_response.get_json()['RID']
        
        # Try to update with invalid date format
        response = client.put(f'/api/resources/{rid}', json={
            'res_start': 'invalid-date'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data


class TestGetActiveResourcesEndpoint:
    """Tests for GET /api/resources/active endpoint."""
    
    def test_get_active_resources_empty(self, client, clean_db):
        """Test getting active resources when none exist."""
        response = client.get('/api/resources/active')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_active_resources_single(self, client, clean_db):
        """Test getting active resources with one resource."""
        # Create a worker and resource
        client.post('/api/workers', json={
            'name': 'Frank Garcia',
            'org': 'Legal',
            'type': 'Counsel',
            'res_start': '2024-01-01'
        })
        
        response = client.get('/api/resources/active')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        
        resource = data[0]
        assert 'RID' in resource
        assert 'version' in resource
        assert 'WID' in resource
        assert 'name' in resource
        assert resource['name'] == 'Frank Garcia'
        assert 'org' in resource
        assert resource['org'] == 'Legal'
        assert 'type' in resource
        assert resource['type'] == 'Counsel'
        assert 'res_start' in resource
        assert 'res_end' in resource
        assert 'proc_start' in resource
        assert 'proc_end' in resource
    
    def test_get_active_resources_multiple(self, client, clean_db):
        """Test getting active resources with multiple resources."""
        # Create multiple workers and resources
        client.post('/api/workers', json={
            'name': 'Grace Lee',
            'org': 'Design',
            'type': 'Designer',
            'res_start': '2024-01-01'
        })
        client.post('/api/workers', json={
            'name': 'Henry Chen',
            'org': 'Product',
            'type': 'Manager',
            'res_start': '2024-02-01'
        })
        
        response = client.get('/api/resources/active')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
    
    def test_get_active_resources_after_update(self, client, clean_db):
        """Test that only the latest version is returned after update."""
        # Create a worker and resource
        create_response = client.post('/api/workers', json={
            'name': 'Iris Wang',
            'org': 'Research',
            'type': 'Scientist',
            'res_start': '2024-01-01'
        })
        rid = create_response.get_json()['RID']
        
        # Update the resource
        client.put(f'/api/resources/{rid}', json={
            'res_end': '2024-12-31'
        })
        
        # Get active resources
        response = client.get('/api/resources/active')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['version'] == 2


class TestAsOfQueryEndpoint:
    """Tests for GET /api/resources/as-of endpoint."""
    
    def test_as_of_query_missing_business_date(self, client, clean_db):
        """Test error when business_date is missing."""
        response = client.get('/api/resources/as-of')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'business_date' in data['error'].lower()
    
    def test_as_of_query_with_business_date_only(self, client, clean_db):
        """Test as-of query with only business_date."""
        # Create a worker and resource
        client.post('/api/workers', json={
            'name': 'Jack Taylor',
            'org': 'Security',
            'type': 'Officer',
            'res_start': '2024-01-01'
        })
        
        response = client.get('/api/resources/as-of?business_date=2024-06-01')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 1
    
    def test_as_of_query_with_both_parameters(self, client, clean_db):
        """Test as-of query with both business_date and processing_datetime."""
        # Create a worker and resource
        client.post('/api/workers', json={
            'name': 'Karen White',
            'org': 'Compliance',
            'type': 'Auditor',
            'res_start': '2024-01-01'
        })
        
        response = client.get(
            '/api/resources/as-of?business_date=2024-06-01&processing_datetime=2024-12-01T12:00:00'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_as_of_query_invalid_date_format(self, client, clean_db):
        """Test error when date format is invalid."""
        response = client.get('/api/resources/as-of?business_date=invalid-date')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_as_of_query_returns_correct_fields(self, client, clean_db):
        """Test that as-of query returns all required fields."""
        # Create a worker and resource
        client.post('/api/workers', json={
            'name': 'Laura Green',
            'org': 'Training',
            'type': 'Instructor',
            'res_start': '2024-01-01'
        })
        
        response = client.get('/api/resources/as-of?business_date=2024-06-01')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        
        resource = data[0]
        assert 'RID' in resource
        assert 'version' in resource
        assert 'WID' in resource
        assert 'name' in resource
        assert 'org' in resource
        assert 'type' in resource
        assert 'res_start' in resource
        assert 'res_end' in resource
        assert 'proc_start' in resource
        assert 'proc_end' in resource
    
    def test_as_of_query_before_res_start(self, client, clean_db):
        """Test as-of query with business_date before res_start."""
        # Create a worker and resource
        client.post('/api/workers', json={
            'name': 'Mike Brown',
            'org': 'Logistics',
            'type': 'Coordinator',
            'res_start': '2024-06-01'
        })
        
        # Query before res_start
        response = client.get('/api/resources/as-of?business_date=2024-01-01')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 0
    
    def test_as_of_query_after_res_end(self, client, clean_db):
        """Test as-of query with business_date after res_end."""
        # Create a worker and resource
        create_response = client.post('/api/workers', json={
            'name': 'Nancy Clark',
            'org': 'Quality',
            'type': 'Inspector',
            'res_start': '2024-01-01'
        })
        rid = create_response.get_json()['RID']
        
        # Update to set res_end
        client.put(f'/api/resources/{rid}', json={
            'res_end': '2024-06-30'
        })
        
        # Query after res_end
        response = client.get('/api/resources/as-of?business_date=2024-12-31')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 0


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_create_worker_with_infinity_date(self, client, clean_db):
        """Test creating worker with res_start at infinity (boundary)."""
        response = client.post('/api/workers', json={
            'name': 'Oscar Hill',
            'org': 'Planning',
            'type': 'Strategist',
            'res_start': '9999-12-31'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'WID' in data
        assert 'RID' in data
    
    def test_update_resource_to_infinity(self, client, clean_db):
        """Test updating res_end to infinity."""
        # Create a worker and resource
        create_response = client.post('/api/workers', json={
            'name': 'Paula King',
            'org': 'Development',
            'type': 'Engineer',
            'res_start': '2024-01-01'
        })
        rid = create_response.get_json()['RID']
        
        # Update res_end to a specific date
        client.put(f'/api/resources/{rid}', json={
            'res_end': '2024-12-31'
        })
        
        # Update res_end back to infinity
        response = client.put(f'/api/resources/{rid}', json={
            'res_end': '9999-12-31'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['version'] == 3
    
    def test_multiple_updates_same_resource(self, client, clean_db):
        """Test multiple sequential updates to the same resource."""
        # Create a worker and resource
        create_response = client.post('/api/workers', json={
            'name': 'Quinn Adams',
            'org': 'Analytics',
            'type': 'Data Scientist',
            'res_start': '2024-01-01'
        })
        rid = create_response.get_json()['RID']
        
        # Perform multiple updates
        for i in range(5):
            response = client.put(f'/api/resources/{rid}', json={
                'res_start': f'2024-0{i+2}-01'
            })
            assert response.status_code == 200
            assert response.get_json()['version'] == i + 2
        
        # Verify only one active version
        active_response = client.get('/api/resources/active')
        data = active_response.get_json()
        assert len(data) == 1
        assert data[0]['version'] == 6
