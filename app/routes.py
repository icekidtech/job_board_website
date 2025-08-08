from flask import Blueprint, render_template, request, redirect, url_for, flash, session
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

@main.route('/login', methods=['GET', 'POST'])
def login():
    """Login route - handles user authentication"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me')
        
        # Validate form data
        if not email or not password:
            flash('Please provide both email and password.', 'error')
            return render_template('login.html')
        
        # Find user by email
        user = User.query.filter_by(email=email, is_active=True).first()
        
        if user and user.check_password(password):
            # Login successful - create session
            session['user_id'] = user.id
            session['user_role'] = user.role
            session['username'] = user.username
            
            # Handle "remember me" functionality
            if remember_me:
                session.permanent = True
            
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Redirect based on user role
            if user.role == 'employer':
                return redirect(url_for('main.jobs'))  # Could redirect to employer dashboard
            else:
                return redirect(url_for('main.jobs'))  # Could redirect to job search
        else:
            flash('Invalid email or password. Please try again.', 'error')
    
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    """Registration route - handles user registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')
        terms = request.form.get('terms')
        
        # Validate form data
        if not all([username, email, password, confirm_password, role, terms]):
            flash('Please fill in all required fields and accept the terms.', 'error')
            return render_template('register.html')
        
        # Check password confirmation
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return render_template('register.html')
        
        # Validate password length
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')
        
        # Validate role
        if role not in ['seeker', 'employer']:
            flash('Please select a valid role.', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            if existing_user.username == username:
                flash('Username already exists. Please choose a different one.', 'error')
            else:
                flash('Email already registered. Please use a different email.', 'error')
            return render_template('register.html')
        
        try:
            # Create new user
            new_user = User(username=username, email=email, password=password, role=role)
            db.session.add(new_user)
            db.session.commit()
            
            # Auto-login after successful registration
            session['user_id'] = new_user.id
            session['user_role'] = new_user.role
            session['username'] = new_user.username
            
            flash(f'Account created successfully! Welcome to Job Board, {username}!', 'success')
            
            # Redirect based on user role
            if role == 'employer':
                return redirect(url_for('main.jobs'))  # Could redirect to employer dashboard
            else:
                return redirect(url_for('main.jobs'))  # Could redirect to job search
                
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@main.route('/logout')
def logout():
    """Logout route - clears user session"""
    username = session.get('username', 'User')
    session.clear()
    flash(f'You have been logged out successfully. Goodbye, {username}!', 'info')
    return redirect(url_for('main.home'))

@main.route('/about')
def about():
    """About route - displays information about the job board"""
    return render_template('about.html')

# Utility function to check if user is logged in
def is_logged_in():
    """Check if user is currently logged in"""
    return 'user_id' in session

# Utility function to get current user
def get_current_user():
    """Get current logged-in user object"""
    if is_logged_in():
        return User.query.get(session['user_id'])
    return None

# Make utility functions available in templates
@main.app_template_global()
def current_user():
    """Template global function to get current user"""
    return get_current_user()

@main.app_template_global()
def logged_in():
    """Template global function to check login status"""
    return is_logged_in()

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