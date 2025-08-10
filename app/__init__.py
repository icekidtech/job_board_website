from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os

# Initialize SQLAlchemy instance globally
db = SQLAlchemy()

def create_app():
    # Get the absolute path to the templates directory
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)
    
    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_board.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
    
    # Initialize SQLAlchemy with the app
    db.init_app(app)
    
    # Import models after db is initialized (to avoid circular imports)
    from app.models import User, JobPosting, Application
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    # Create tables within app context
    with app.app_context():
        db.create_all()
        print("Database tables created successfully with SQLite3!")
    
    return app
