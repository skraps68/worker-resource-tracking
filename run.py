"""Application entry point."""
from app import create_app
from app.database import create_schema
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = create_app()

if __name__ == '__main__':
    # Create database schema on startup
    with app.app_context():
        create_schema()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
