import mysql.connector
from mysql.connector import Error
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db_config import DB_CONFIG, DatabaseConfig

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
    from flask import Flask
    
    app = Flask(__name__)
    
    # Test database connection on app creation
    print("Testing database connection...")
    if test_database_connection():
        print("Database setup is ready!")
    else:
        print("Database connection failed. Please check your configuration.")
    
    return app

if __name__ == "__main__":
    # Run database connection test
    test_database_connection()