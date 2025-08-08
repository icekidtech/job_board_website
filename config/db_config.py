import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DatabaseConfig:
    """Database configuration class"""
    
    # MySQL connection settings
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'job_user')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'job_password')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'job_board_db')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
    }

# Alternative dictionary approach for direct mysql-connector usage
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'job_user'),
    'password': os.getenv('MYSQL_PASSWORD', 'job_password'),
    'database': os.getenv('MYSQL_DATABASE', 'job_board_db'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'charset': 'utf8mb4',
    'autocommit': True
}