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
        """Get all jobs this seeker has applied for with real database data"""
        if self.role != 'seeker':
            return []
        
        try:
            # Query applications with job details using SQLAlchemy joins
            from sqlalchemy import desc
            
            applications = db.session.query(
                Application.id.label('application_id'),
                Application.application_date,
                Application.status,
                Application.cover_letter,
                JobPosting.id.label('job_id'),
                JobPosting.title.label('job_title'),
                JobPosting.company_name,
                JobPosting.location,
                JobPosting.job_type,
                JobPosting.salary_range,
                JobPosting.posted_date
            ).join(
                JobPosting, Application.job_id == JobPosting.id
            ).filter(
                Application.seeker_id == self.id
            ).order_by(
                desc(Application.application_date)
            ).all()
            
            # Convert to list of dictionaries for template use
            applied_jobs = []
            for app in applications:
                applied_jobs.append({
                    'application_id': app.application_id,
                    'job_id': app.job_id,
                    'job_title': app.job_title,
                    'company_name': app.company_name or 'Not specified',
                    'location': app.location or 'Not specified',
                    'job_type': app.job_type or 'Not specified',
                    'salary_range': app.salary_range,
                    'application_date': app.application_date,
                    'status': app.status,
                    'cover_letter': app.cover_letter,
                    'posted_date': app.posted_date
                })
            
            return applied_jobs
            
        except Exception as e:
            print(f"Error fetching applied jobs: {e}")
            return []
    
    def get_posted_jobs(self):
        """Get all jobs posted by this employer with real database data"""
        if self.role != 'employer':
            return []
        
        try:
            # Query jobs with application counts using SQLAlchemy
            from sqlalchemy import func, desc
            
            jobs_with_counts = db.session.query(
                JobPosting.id,
                JobPosting.title,
                JobPosting.description,
                JobPosting.company_name,
                JobPosting.location,
                JobPosting.salary_range,
                JobPosting.job_type,
                JobPosting.posted_date,
                JobPosting.is_active,
                func.count(Application.id).label('application_count')
            ).outerjoin(
                Application, JobPosting.id == Application.job_id
            ).filter(
                JobPosting.employer_id == self.id
            ).group_by(
                JobPosting.id
            ).order_by(
                desc(JobPosting.posted_date)
            ).all()
            
            # Convert to list of dictionaries for template use
            posted_jobs = []
            for job in jobs_with_counts:
                posted_jobs.append({
                    'id': job.id,
                    'title': job.title,
                    'description': job.description,
                    'company_name': job.company_name,
                    'location': job.location or 'Remote',
                    'salary_range': job.salary_range,
                    'job_type': job.job_type or 'Full-time',
                    'posted_date': job.posted_date,
                    'is_active': job.is_active,
                    'application_count': job.application_count or 0,
                    'view_count': 0  # Placeholder for view tracking feature
                })
            
            return posted_jobs
            
        except Exception as e:
            print(f"Error fetching posted jobs: {e}")
            return []
    
    def get_recent_applications(self):
        """Get recent applications for this employer's jobs with real database data"""
        if self.role != 'employer':
            return []
        
        try:
            # Query applications for employer's jobs with seeker details
            from sqlalchemy import desc
            
            applications = db.session.query(
                Application.id.label('application_id'),
                Application.application_date,
                Application.status,
                Application.cover_letter,
                JobPosting.title.label('job_title'),
                User.username.label('applicant_name'),
                User.email.label('applicant_email')
            ).join(
                JobPosting, Application.job_id == JobPosting.id
            ).join(
                User, Application.seeker_id == User.id
            ).filter(
                JobPosting.employer_id == self.id
            ).order_by(
                desc(Application.application_date)
            ).limit(20).all()  # Limit to recent 20 applications
            
            # Convert to list of dictionaries for template use
            recent_applications = []
            for app in applications:
                recent_applications.append({
                    'application_id': app.application_id,
                    'applicant_name': app.applicant_name,
                    'applicant_email': app.applicant_email,
                    'job_title': app.job_title,
                    'application_date': app.application_date,
                    'status': app.status,
                    'cover_letter': app.cover_letter
                })
            
            return recent_applications
            
        except Exception as e:
            print(f"Error fetching recent applications: {e}")
            return []
    
    @staticmethod
    def get_system_overview():
        """Get system overview statistics for admin dashboard with real database data"""
        try:
            from sqlalchemy import func, and_, extract
            from datetime import datetime, timedelta
            
            # Calculate date ranges
            now = datetime.now()
            start_of_month = datetime(now.year, now.month, 1)
            start_of_today = datetime(now.year, now.month, now.day)
            
            # Total counts
            total_users = db.session.query(func.count(User.id)).scalar() or 0
            total_jobs = db.session.query(func.count(JobPosting.id)).filter(
                JobPosting.is_active == True
            ).scalar() or 0
            total_applications = db.session.query(func.count(Application.id)).scalar() or 0
            
            # User role counts
            total_employers = db.session.query(func.count(User.id)).filter(
                User.role == 'employer'
            ).scalar() or 0
            
            active_employers = db.session.query(func.count(User.id)).filter(
                and_(User.role == 'employer', User.is_active == True)
            ).scalar() or 0
            
            # Monthly counts
            new_users_this_month = db.session.query(func.count(User.id)).filter(
                User.created_at >= start_of_month
            ).scalar() or 0
            
            new_jobs_this_month = db.session.query(func.count(JobPosting.id)).filter(
                JobPosting.posted_date >= start_of_month
            ).scalar() or 0
            
            new_applications_this_month = db.session.query(func.count(Application.id)).filter(
                Application.application_date >= start_of_month
            ).scalar() or 0
            
            # Daily counts
            applications_today = db.session.query(func.count(Application.id)).filter(
                Application.application_date >= start_of_today
            ).scalar() or 0
            
            jobs_posted_today = db.session.query(func.count(JobPosting.id)).filter(
                JobPosting.posted_date >= start_of_today
            ).scalar() or 0
            
            new_users_today = db.session.query(func.count(User.id)).filter(
                User.created_at >= start_of_today
            ).scalar() or 0
            
            # Recent users
            recent_users_query = db.session.query(User).order_by(
                User.created_at.desc()
            ).limit(5).all()
            
            recent_users = []
            for user in recent_users_query:
                recent_users.append({
                    'username': user.username,
                    'role': user.role,
                    'created_at': user.created_at,
                    'is_active': user.is_active
                })
            
            # Recent jobs
            recent_jobs_query = db.session.query(
                JobPosting.title,
                JobPosting.company_name,
                JobPosting.posted_date,
                func.count(Application.id).label('application_count')
            ).outerjoin(
                Application, JobPosting.id == Application.job_id
            ).group_by(
                JobPosting.id
            ).order_by(
                JobPosting.posted_date.desc()
            ).limit(5).all()
            
            recent_jobs = []
            for job in recent_jobs_query:
                recent_jobs.append({
                    'title': job.title,
                    'company_name': job.company_name or 'N/A',
                    'posted_date': job.posted_date,
                    'application_count': job.application_count or 0
                })
            
            return {
                'total_users': total_users,
                'total_jobs': total_jobs,
                'total_applications': total_applications,
                'total_employers': total_employers,
                'active_employers': active_employers,
                'new_users_this_month': new_users_this_month,
                'new_jobs_this_month': new_jobs_this_month,
                'new_applications_this_month': new_applications_this_month,
                'applications_today': applications_today,
                'jobs_posted_today': jobs_posted_today,
                'new_users_today': new_users_today,
                'recent_users': recent_users,
                'recent_jobs': recent_jobs
            }
            
        except Exception as e:
            print(f"Error fetching system overview: {e}")
            # Return default values if query fails
            return {
                'total_users': 0,
                'total_jobs': 0,
                'total_applications': 0,
                'total_employers': 0,
                'active_employers': 0,
                'new_users_this_month': 0,
                'new_jobs_this_month': 0,
                'new_applications_this_month': 0,
                'applications_today': 0,
                'jobs_posted_today': 0,
                'new_users_today': 0,
                'recent_users': [],
                'recent_jobs': []
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