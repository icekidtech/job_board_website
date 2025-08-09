"""
Flask application factory and configuration
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os

# Initialize extensions
db = SQLAlchemy()

def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    from config.db_config import config, DatabaseConfig
    app.config.from_object(config[config_name])
    
    # Ensure database directory exists
    DatabaseConfig.create_database_directory()
    
    # Initialize extensions
    db.init_app(app)
    
    # Session configuration
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
    
    # Add custom Jinja2 filter for line breaks
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        """Convert newlines to HTML line breaks"""
        if text:
            return text.replace('\n', '<br>')
        return text
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    # Create database tables
    with app.app_context():
        from app.models import User, JobPosting, Application
        db.create_all()
        print("Database tables created successfully with SQLite3!")
    
    return app

def test_database_connection():
    """Test SQLite database connection and setup"""
    try:
        from config.db_config import DatabaseConfig
        
        # Check if we can create the database directory
        DatabaseConfig.create_database_directory()
        
        # Create a test app to check database connection
        app = create_app('testing')
        
        with app.app_context():
            from app.models import db, User
            
            # Test database operations
            db.create_all()
            
            # Try to query (this will create the database file if it doesn't exist)
            user_count = User.query.count()
            
            print("✅ SQLite3 database connection successful!")
            print(f"📊 Current user count: {user_count}")
            print(f"📁 Database location: {DatabaseConfig.get_database_path()}")
            
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == '__main__':
    """Test database connection when run directly"""
    test_database_connection()