import mysql.connector
from mysql.connector import Error
import sys
import os
from flask import Flask
from datetime import timedelta

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db_config import DB_CONFIG, DatabaseConfig
from app.models import db, create_tables

def test_database_connection():
    """Test the database connection"""
    connection = None
    try:
        # Using dictionary config
        connection = mysql.connector.connect(**DB_CONFIG)
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"✅ Successfully connected to MySQL Server version {db_info}")
            
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            database_name = cursor.fetchone()
            print(f"✅ Connected to database: {database_name[0]}")
            
            return True
            
    except Error as e:
        print(f"❌ Error while connecting to MySQL: {e}")
        return False
        
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("🔌 MySQL connection is closed")

def create_app():
    """Factory function to create Flask app"""
    # Get the project root directory (one level up from app/)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create Flask app with correct template and static folder paths
    app = Flask(__name__, 
                template_folder=os.path.join(project_root, 'templates'),
                static_folder=os.path.join(project_root, 'static'))
    
    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseConfig.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = DatabaseConfig.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = DatabaseConfig.SQLALCHEMY_ENGINE_OPTIONS
    
    # Session configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)  # Remember me duration
    
    # Initialize database with app
    db.init_app(app)
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    # Test database connection on app creation
    print("Testing database connection...")
    if test_database_connection():
        print("Database setup is ready!")
        
        # Create tables if they don't exist
        create_tables(app)
        
    else:
        print("Database connection failed. Please check your configuration.")
    
    return app

if __name__ == "__main__":
    # Run database connection test
    test_database_connection()