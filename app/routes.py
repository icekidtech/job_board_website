from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, User, JobPosting, Application

# Create a blueprint for main routes
main = Blueprint('main', __name__)

@main.route('/')
def home():
    """Homepage route - displays welcome message and overview"""
    # Get some basic statistics for the homepage
    total_jobs = JobPosting.query.filter_by(is_active=True).count()
    total_users = User.query.filter_by(is_active=True).count()
    
    return render_template('home.html', 
                         total_jobs=total_jobs, 
                         total_users=total_users)

@main.route('/jobs')
def jobs():
    """Job listings route - displays all active job postings"""
    # Get all active job postings, ordered by most recent
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of jobs per page
    
    jobs = JobPosting.query.filter_by(is_active=True)\
                          .order_by(JobPosting.posted_date.desc())\
                          .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('jobs.html', jobs=jobs)

@main.route('/login')
def login():
    """Login route - displays login form for users"""
    return render_template('login.html')

@main.route('/register')
def register():
    """Registration route - displays registration form for new users"""
    return render_template('register.html')

@main.route('/about')
def about():
    """About route - displays information about the job board"""
    return render_template('about.html')

# Error handlers
@main.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('errors/404.html'), 404

@main.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('errors/500.html'), 500