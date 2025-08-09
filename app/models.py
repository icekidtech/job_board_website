from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy instance
db = SQLAlchemy()

class User(db.Model):
    """User model for both job seekers and employers"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)  # Will store hashed password
    role = db.Column(db.Enum('seeker', 'employer', name='user_roles'), nullable=False, default='seeker')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    job_postings = db.relationship('JobPosting', backref='employer', lazy=True, foreign_keys='JobPosting.employer_id')
    applications = db.relationship('Application', backref='seeker', lazy=True, foreign_keys='Application.seeker_id')
    
    def __init__(self, username, email, password, role='seeker'):
        """Initialize user with hashed password"""
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role
    
    def check_password(self, password):
        """Check if provided password matches the stored hash"""
        return check_password_hash(self.password, password)
    
    def set_password(self, password):
        """Set new password (hashed)"""
        self.password = generate_password_hash(password)
    
    def to_dict(self):
        """Convert user object to dictionary (excluding password)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_applied_jobs(self):
        """Get all jobs this seeker has applied for (placeholder data)"""
        if self.role != 'seeker':
            return []
        
        # Placeholder data - replace with actual database queries later
        from datetime import datetime, timedelta
        placeholder_applications = [
            {
                'job_title': 'Senior Python Developer',
                'company_name': 'TechCorp Inc.',
                'job_type': 'Full-time',
                'application_date': datetime.now() - timedelta(days=5),
                'status': 'pending'
            },
            {
                'job_title': 'Frontend Developer',
                'company_name': 'WebSolutions Ltd.',
                'job_type': 'Contract',
                'application_date': datetime.now() - timedelta(days=12),
                'status': 'reviewed'
            },
            {
                'job_title': 'Data Analyst',
                'company_name': 'DataFlow Corp.',
                'job_type': 'Full-time',
                'application_date': datetime.now() - timedelta(days=18),
                'status': 'rejected'
            }
        ]
        return placeholder_applications
    
    def get_posted_jobs(self):
        """Get all jobs posted by this employer (placeholder data)"""
        if self.role != 'employer':
            return []
        
        # Placeholder data - replace with actual database queries later
        from datetime import datetime, timedelta
        placeholder_jobs = [
            {
                'title': 'Python Developer',
                'job_type': 'Full-time',
                'location': 'Remote',
                'posted_date': datetime.now() - timedelta(days=7),
                'is_active': True,
                'application_count': 15,
                'view_count': 120
            },
            {
                'title': 'UI/UX Designer',
                'job_type': 'Part-time',
                'location': 'New York',
                'posted_date': datetime.now() - timedelta(days=14),
                'is_active': True,
                'application_count': 8,
                'view_count': 85
            },
            {
                'title': 'Project Manager',
                'job_type': 'Full-time',
                'location': 'San Francisco',
                'posted_date': datetime.now() - timedelta(days=21),
                'is_active': False,
                'application_count': 22,
                'view_count': 200
            }
        ]
        return placeholder_jobs
    
    def get_recent_applications(self):
        """Get recent applications for this employer's jobs (placeholder data)"""
        if self.role != 'employer':
            return []
        
        # Placeholder data - replace with actual database queries later
        from datetime import datetime, timedelta
        placeholder_applications = [
            {
                'applicant_name': 'John Smith',
                'applicant_email': 'john.smith@email.com',
                'job_title': 'Python Developer',
                'application_date': datetime.now() - timedelta(days=1),
                'status': 'pending'
            },
            {
                'applicant_name': 'Sarah Johnson',
                'applicant_email': 'sarah.j@email.com',
                'job_title': 'UI/UX Designer',
                'application_date': datetime.now() - timedelta(days=3),
                'status': 'reviewed'
            },
            {
                'applicant_name': 'Mike Wilson',
                'applicant_email': 'mike.wilson@email.com',
                'job_title': 'Python Developer',
                'application_date': datetime.now() - timedelta(days=5),
                'status': 'accepted'
            }
        ]
        return placeholder_applications
    
    @staticmethod
    def get_system_overview():
        """Get system overview statistics for admin dashboard (placeholder data)"""
        from datetime import datetime, timedelta
        
        # Placeholder data - replace with actual database queries later
        return {
            'total_users': 1247,
            'total_jobs': 89,
            'total_applications': 432,
            'total_employers': 156,
            'active_employers': 98,
            'new_users_this_month': 78,
            'new_jobs_this_month': 23,
            'new_applications_this_month': 145,
            'applications_today': 12,
            'jobs_posted_today': 3,
            'new_users_today': 5,
            'recent_users': [
                {
                    'username': 'tech_recruiter',
                    'role': 'employer',
                    'created_at': datetime.now() - timedelta(days=1),
                    'is_active': True
                },
                {
                    'username': 'job_seeker_123',
                    'role': 'seeker',
                    'created_at': datetime.now() - timedelta(days=2),
                    'is_active': True
                },
                {
                    'username': 'dev_company',
                    'role': 'employer',
                    'created_at': datetime.now() - timedelta(days=3),
                    'is_active': True
                }
            ],
            'recent_jobs': [
                {
                    'title': 'Senior Software Engineer',
                    'company_name': 'TechCorp',
                    'posted_date': datetime.now() - timedelta(days=1),
                    'application_count': 8
                },
                {
                    'title': 'Marketing Manager',
                    'company_name': 'MarketPro',
                    'posted_date': datetime.now() - timedelta(days=2),
                    'application_count': 5
                },
                {
                    'title': 'Data Scientist',
                    'company_name': 'DataFlow',
                    'posted_date': datetime.now() - timedelta(days=3),
                    'application_count': 12
                }
            ]
        }


class JobPosting(db.Model):
    """Job posting model for employer job listings"""
    __tablename__ = 'job_postings'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    company_name = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    salary_range = db.Column(db.String(50), nullable=True)
    job_type = db.Column(db.Enum('full-time', 'part-time', 'contract', 'internship', name='job_types'), 
                        nullable=False, default='full-time')
    employer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    posted_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    deadline = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    applications = db.relationship('Application', backref='job_posting', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, title, description, employer_id, company_name=None, location=None, 
                 salary_range=None, job_type='full-time', deadline=None):
        """Initialize job posting"""
        self.title = title
        self.description = description
        self.employer_id = employer_id
        self.company_name = company_name
        self.location = location
        self.salary_range = salary_range
        self.job_type = job_type
        self.deadline = deadline
    
    def to_dict(self):
        """Convert job posting object to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'company_name': self.company_name,
            'location': self.location,
            'salary_range': self.salary_range,
            'job_type': self.job_type,
            'employer_id': self.employer_id,
            'employer_name': self.employer.username if self.employer else None,
            'posted_date': self.posted_date.isoformat() if self.posted_date else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'applications_count': len(self.applications)
        }
    
    def is_expired(self):
        """Check if job posting has passed its deadline"""
        if self.deadline:
            return datetime.utcnow() > self.deadline
        return False
    
    def __repr__(self):
        return f'<JobPosting {self.title}>'


class Application(db.Model):
    """Application model for job applications"""
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job_postings.id'), nullable=False, index=True)
    seeker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    application_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    cover_letter = db.Column(db.Text, nullable=True)
    resume_path = db.Column(db.String(255), nullable=True)  # Path to uploaded resume file
    status = db.Column(db.Enum('pending', 'reviewed', 'accepted', 'rejected', name='application_status'), 
                      nullable=False, default='pending')
    notes = db.Column(db.Text, nullable=True)  # Employer notes about the application
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Unique constraint to prevent duplicate applications
    __table_args__ = (db.UniqueConstraint('job_id', 'seeker_id', name='unique_job_seeker_application'),)
    
    def __init__(self, job_id, seeker_id, cover_letter=None, resume_path=None):
        """Initialize application"""
        self.job_id = job_id
        self.seeker_id = seeker_id
        self.cover_letter = cover_letter
        self.resume_path = resume_path
    
    def to_dict(self):
        """Convert application object to dictionary"""
        return {
            'id': self.id,
            'job_id': self.job_id,
            'job_title': self.job_posting.title if self.job_posting else None,
            'seeker_id': self.seeker_id,
            'seeker_name': self.seeker.username if self.seeker else None,
            'application_date': self.application_date.isoformat() if self.application_date else None,
            'cover_letter': self.cover_letter,
            'resume_path': self.resume_path,
            'status': self.status,
            'notes': self.notes,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def update_status(self, new_status, notes=None):
        """Update application status with optional notes"""
        valid_statuses = ['pending', 'reviewed', 'accepted', 'rejected']
        if new_status in valid_statuses:
            self.status = new_status
            if notes:
                self.notes = notes
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def __repr__(self):
        return f'<Application {self.id}: Job {self.job_id} by User {self.seeker_id}>'


# Helper function to create all tables
def create_tables(app):
    """Create all database tables"""
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")


# Helper function to drop all tables (for development/testing)
def drop_tables(app):
    """Drop all database tables"""
    with app.app_context():
        db.drop_all()
        print("🗑️ Database tables dropped successfully!")