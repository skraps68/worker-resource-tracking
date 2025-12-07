"""API routes for worker and resource management."""
from flask import Blueprint, request, jsonify
from datetime import datetime, date
from app.services import ResourceService
from app.validation import ValidationError


api_bp = Blueprint('api', __name__)


@api_bp.route('/workers', methods=['POST'])
def create_worker():
    """Create a new worker and associated resource."""
    data = request.get_json()
    
    # Validate required fields
    required = ['name', 'org', 'type', 'res_start']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Required field {field} is missing'}), 400
    
    # Validate non-empty string fields
    for field in ['name', 'org', 'type']:
        if not data[field] or not str(data[field]).strip():
            return jsonify({'error': f'Field {field} cannot be empty'}), 400
    
    try:
        # Parse res_start
        res_start = date.fromisoformat(data['res_start'])
        
        # Create worker and resource
        wid, rid, version = ResourceService.create_worker_and_resource(
            data['name'], data['org'], data['type'], res_start
        )
        
        return jsonify({'WID': wid, 'RID': rid, 'version': version}), 201
    
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except ValueError as e:
        return jsonify({'error': f'Invalid date format for res_start'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/resources/<int:rid>', methods=['PUT'])
def update_resource(rid):
    """Update a resource by creating a new version."""
    data = request.get_json()
    
    # Validate at least one date is provided
    if 'res_start' not in data and 'res_end' not in data:
        return jsonify({'error': 'At least one of res_start or res_end must be provided'}), 400
    
    try:
        # Parse dates if provided
        res_start = date.fromisoformat(data['res_start']) if 'res_start' in data else None
        res_end = date.fromisoformat(data['res_end']) if 'res_end' in data else None
        
        # Validate date range if both are provided
        if res_start is not None and res_end is not None:
            if res_start > res_end:
                return jsonify({'error': 'res_start must be less than or equal to res_end'}), 400
        
        # Update resource
        rid, version = ResourceService.update_resource(rid, res_start, res_end)
        
        return jsonify({'RID': rid, 'version': version}), 200
    
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except ValueError as e:
        if 'not found' in str(e):
            return jsonify({'error': str(e)}), 404
        return jsonify({'error': 'Invalid date format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/resources/active', methods=['GET'])
def get_active_resources():
    """Get all active resources (business date constrained to today)."""
    try:
        resources = ResourceService.get_active_resources()
        
        # Convert to JSON-serializable format
        result = []
        for r in resources:
            result.append({
                'RID': r['rid'],
                'version': r['version'],
                'WID': r['wid'],
                'name': r['name'],
                'org': r['org'],
                'type': r['type'],
                'res_start': r['res_start'].isoformat(),
                'res_end': r['res_end'].isoformat(),
                'proc_start': r['proc_start'].isoformat(),
                'proc_end': r['proc_end'].isoformat()
            })
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/resources/open', methods=['GET'])
def get_open_resource_records():
    """Get all open resource records (proc_end = infinity)."""
    try:
        resources = ResourceService.get_open_resource_records()
        
        # Convert to JSON-serializable format
        result = []
        for r in resources:
            result.append({
                'RID': r['rid'],
                'version': r['version'],
                'WID': r['wid'],
                'name': r['name'],
                'org': r['org'],
                'type': r['type'],
                'res_start': r['res_start'].isoformat(),
                'res_end': r['res_end'].isoformat(),
                'proc_start': r['proc_start'].isoformat(),
                'proc_end': r['proc_end'].isoformat()
            })
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/resources/as-of', methods=['GET'])
def as_of_query():
    """Execute bi-temporal as-of query."""
    business_date_str = request.args.get('business_date')
    processing_datetime_str = request.args.get('processing_datetime')
    
    if not business_date_str:
        return jsonify({'error': 'business_date parameter is required'}), 400
    
    try:
        # Parse dates
        business_date = date.fromisoformat(business_date_str)
        processing_datetime = None
        if processing_datetime_str:
            processing_datetime = datetime.fromisoformat(processing_datetime_str)
        
        # Execute query
        resources = ResourceService.as_of_query(business_date, processing_datetime)
        
        # Convert to JSON-serializable format
        result = []
        for r in resources:
            result.append({
                'RID': r['rid'],
                'version': r['version'],
                'WID': r['wid'],
                'name': r['name'],
                'org': r['org'],
                'type': r['type'],
                'res_start': r['res_start'].isoformat(),
                'res_end': r['res_end'].isoformat(),
                'proc_start': r['proc_start'].isoformat(),
                'proc_end': r['proc_end'].isoformat()
            })
        
        return jsonify(result), 200
    
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
