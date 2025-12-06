"""Flask application factory."""
import os
from flask import Flask
from flask_cors import CORS
from app.database import init_db


def create_app(config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    if config:
        app.config.update(config)
    else:
        app.config['DATABASE_URL'] = os.getenv(
            'DATABASE_URL',
            'postgresql://localhost/worker_resource_tracking'
        )
    
    # Enable CORS for frontend
    CORS(app)
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
