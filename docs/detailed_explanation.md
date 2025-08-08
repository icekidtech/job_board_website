# Job Board Website - Detailed Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Setup Instructions](#setup-instructions)
4. [Database Schema](#database-schema)
5. [Database Models](#database-models)
6. [Routes and Templates](#routes-and-templates)
7. [API Endpoints](#api-endpoints)
8. [Development Guidelines](#development-guidelines)

## Project Overview

### Purpose
This job board website allows employers to post job listings and job seekers to browse and apply for positions. The platform provides a simple, user-friendly interface for both posting and searching job opportunities.

### Technology Stack
- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: MySQL with SQLAlchemy ORM
- **Environment**: Python virtual environment

### Key Features (Planned)
- Job listing creation and management
- Job search and filtering
- User registration and authentication
- Application tracking
- Admin dashboard

## Architecture

### Project Structure
```
job_board_website/
├── app/                    # Main application package
│   ├── __init__.py        # App factory and DB connection test
│   ├── models.py          # SQLAlchemy database models
│   ├── routes.py          # Flask routes and views
│   └── utils/             # Utility functions
├── config/                # Configuration files
│   └── db_config.py       # Database configuration
├── docs/                  # Documentation
│   └── detailed_explanation.md
├── static/                # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css      # Custom styles
│   ├── js/
│   │   └── main.js        # JavaScript functionality
│   └── images/
├── templates/             # Jinja2 HTML templates
│   ├── base.html          # Base template with navigation
│   ├── home.html          # Homepage template
│   ├── jobs.html          # Job listings template
│   ├── login.html         # Login form template
│   ├── register.html      # Registration form template
│   ├── about.html         # About page template
│   └── errors/            # Error page templates
│       ├── 404.html
│       └── 500.html
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── .gitignore            # Git ignore rules
├── run.py                # Application runner script
└── readme.md             # Brief project overview
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)

### 1. Environment Setup
```bash
# Clone or navigate to project directory
cd /path/to/job_board_website

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Install MySQL (if not already installed)
sudo apt install mysql-server

# Start MySQL service
sudo systemctl start mysql

# Create database and user (run in MySQL console)
mysql -u root -p
```

```sql
CREATE DATABASE job_board_db;
CREATE USER 'job_user'@'localhost' IDENTIFIED BY 'job_password';
GRANT ALL PRIVILEGES ON job_board_db.* TO 'job_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your database credentials
nano .env
```

### 4. Test Database Connection
```bash
# Run the database connection test
python app/__init__.py
```

### 5. Run the Application
```bash
# Start the Flask development server
python run.py

# Alternative: using Flask CLI
flask run
```

## Database Schema

### Database Tables Overview

The job board application uses three main tables to manage users, job postings, and applications:

1. **users** - Stores user accounts for both job seekers and employers
2. **job_postings** - Contains job listings created by employers
3. **applications** - Tracks job applications submitted by seekers

### Entity Relationship Diagram

```
users (1) ----< job_postings (1) ----< applications (n)
  |                                         ^
  |                                         |
  +----------- seeker_id ------------------+
```

## Database Models

### User Model (`users` table)

The User model handles both job seekers and employers with role-based differentiation.

**Fields:**
- `id` (Integer, Primary Key) - Unique user identifier
- `username` (String(80), Unique, Required) - User's display name
- `email` (String(120), Unique, Required) - User's email address
- `password` (String(255), Required) - Hashed password for security
- `role` (Enum: 'seeker'/'employer', Required) - User type with default 'seeker'
- `created_at` (DateTime, Required) - Account creation timestamp
- `updated_at` (DateTime, Required) - Last profile update timestamp
- `is_active` (Boolean, Required) - Account status flag

**Relationships:**
- One-to-many with JobPosting (as employer)
- One-to-many with Application (as seeker)

**Key Features:**
- Password hashing using Werkzeug security functions
- Role-based access control
- Automatic timestamp management
- Data serialization methods

### JobPosting Model (`job_postings` table)

The JobPosting model represents job listings created by employers.

**Fields:**
- `id` (Integer, Primary Key) - Unique job posting identifier
- `title` (String(200), Required) - Job position title
- `description` (Text, Required) - Detailed job description
- `company_name` (String(100), Optional) - Company/organization name
- `location` (String(100), Optional) - Job location
- `salary_range` (String(50), Optional) - Salary information
- `job_type` (Enum: 'full-time'/'part-time'/'contract'/'internship') - Employment type
- `employer_id` (Integer, Foreign Key to users.id, Required) - Job poster reference
- `posted_date` (DateTime, Required) - Job posting creation timestamp
- `updated_at` (DateTime, Required) - Last job update timestamp
- `is_active` (Boolean, Required) - Job posting status
- `deadline` (DateTime, Optional) - Application deadline

**Relationships:**
- Many-to-one with User (employer)
- One-to-many with Application

**Key Features:**
- Flexible job type categorization
- Deadline tracking with expiration checks
- Cascade deletion of related applications
- Employer information integration

### Application Model (`applications` table)

The Application model tracks job applications submitted by seekers.

**Fields:**
- `id` (Integer, Primary Key) - Unique application identifier
- `job_id` (Integer, Foreign Key to job_postings.id, Required) - Applied job reference
- `seeker_id` (Integer, Foreign Key to users.id, Required) - Applicant reference
- `application_date` (DateTime, Required) - Application submission timestamp
- `cover_letter` (Text, Optional) - Applicant's cover letter
- `resume_path` (String(255), Optional) - Path to uploaded resume file
- `status` (Enum: 'pending'/'reviewed'/'accepted'/'rejected') - Application status
- `notes` (Text, Optional) - Employer notes about the application
- `updated_at` (DateTime, Required) - Last status update timestamp

**Relationships:**
- Many-to-one with JobPosting
- Many-to-one with User (seeker)

**Key Features:**
- Unique constraint preventing duplicate applications per job/seeker
- Status tracking with update methods
- File upload support for resumes
- Employer note system

### Model Relationships Summary

```python
# User relationships
user.job_postings  # Jobs posted by this employer
user.applications  # Applications submitted by this seeker

# JobPosting relationships
job.employer      # User who posted this job
job.applications  # All applications for this job

# Application relationships
application.job_posting  # The job being applied for
application.seeker      # The user who applied
```

### Database Operations

**Creating Tables:**
```python
from app.models import create_tables
create_tables(app)  # Creates all tables if they don't exist
```

**Example Usage:**
```python
# Create a new employer
employer = User(username='techcorp', email='hr@techcorp.com', 
                password='secure123', role='employer')

# Create a job posting
job = JobPosting(title='Software Developer', 
                description='Python developer needed...',
                employer_id=employer.id,
                company_name='TechCorp Inc.',
                location='Remote',
                job_type='full-time')

# Create an application
application = Application(job_id=job.id, seeker_id=seeker.id,
                         cover_letter='I am interested...')
```

## Routes and Templates

### Route Structure

The application uses Flask blueprints to organize routes in [`app/routes.py`](app/routes.py). All routes are registered under the 'main' blueprint.

### Main Routes

#### Homepage Route (`/`)
- **Purpose**: Landing page with overview and statistics
- **Template**: [`templates/home.html`](templates/home.html)
- **Features**:
  - Displays total number of active jobs and users
  - Welcome message and platform overview
  - Feature highlights and call-to-action buttons
  - Responsive design with Bootstrap components

#### Job Listings Route (`/jobs`)
- **Purpose**: Browse and search available job postings
- **Template**: [`templates/jobs.html`](templates/jobs.html)
- **Features**:
  - Paginated job listings (10 per page)
  - Search and filter functionality
  - Job cards with key information (title, company, location, type)
  - Responsive grid layout
  - "No results" state handling

#### Login Route (`/login`)
- **Purpose**: User authentication form
- **Template**: [`templates/login.html`](templates/login.html)
- **Features**:
  - Email and password input fields
  - "Remember me" checkbox
  - Links to registration and password recovery
  - Form validation and error handling

#### Registration Route (`/register`)
- **Purpose**: New user account creation
- **Template**: [`templates/register.html`](templates/register.html)
- **Features**:
  - Username, email, and password fields
  - Role selection (job seeker or employer)
  - Password confirmation
  - Terms of service agreement

#### About Route (`/about`)
- **Purpose**: Information about the platform
- **Template**: [`templates/about.html`](templates/about.html)
- **Features**:
  - Mission statement and platform overview
  - How-it-works explanation
  - Call-to-action buttons

### Template Architecture

#### Base Template ([`templates/base.html`](templates/base.html))
- **Purpose**: Common layout and structure for all pages
- **Features**:
  - Responsive navigation bar with brand and menu items
  - Flash message display system
  - Bootstrap 5 integration
  - Footer with copyright information
  - JavaScript and CSS includes

#### Template Inheritance
All page templates extend the base template using Jinja2 inheritance:

```html
{% extends "base.html" %}
{% block title %}Page Title{% endblock %}
{% block content %}
<!-- Page-specific content -->
{% endblock %}
```

### Error Handling

#### 404 Not Found ([`templates/errors/404.html`](templates/errors/404.html))
- Custom 404 error page with helpful navigation
- User-friendly message and link to homepage

#### 500 Internal Server Error ([`templates/errors/500.html`](templates/errors/500.html))
- Custom 500 error page for server errors
- Database session rollback on errors
- Graceful error recovery

### Static Assets

#### CSS Styling ([`static/css/style.css`](static/css/style.css))
- Custom styles complementing Bootstrap
- Responsive design enhancements
- Card hover effects and transitions
- Form styling and validation states

#### JavaScript Functionality ([`static/js/main.js`](static/js/main.js))
- Auto-hiding alert messages
- Smooth scrolling for anchor links
- Form validation enhancements
- Utility functions for dynamic content

### Navigation Structure

The main navigation includes:
- **Home** - Landing page
- **Jobs** - Job listings with search
- **About** - Platform information
- **Login** - User authentication
- **Register** - Account creation

### Responsive Design

All templates use Bootstrap 5 for responsive design:
- Mobile-first approach
- Flexible grid system
- Responsive navigation with collapsible menu
- Touch-friendly buttons and forms

## API Endpoints

### Planned Endpoints

#### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `POST /api/logout` - User logout

#### Jobs
- `GET /api/jobs` - List all jobs
- `GET /api/jobs/<id>` - Get specific job
- `POST /api/jobs` - Create new job (employers only)
- `PUT /api/jobs/<id>` - Update job (owner only)
- `DELETE /api/jobs/<id>` - Delete job (owner only)

#### Applications
- `POST /api/jobs/<id>/apply` - Apply for job
- `GET /api/applications` - Get user's applications
- `GET /api/jobs/<id>/applications` - Get applications for job (owner only)

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused

### Git Workflow
- Create feature branches for new features
- Write descriptive commit messages
- Test changes before committing

### Security Considerations
- Never commit sensitive data (passwords, API keys)
- Use environment variables for configuration
- Implement proper input validation
- Use parameterized queries to prevent SQL injection

### Testing
- Write unit tests for business logic
- Test database operations
- Validate API endpoints
- Test user interface functionality

## Next Steps

1. ✅ Database setup and connection
2. ✅ Create database models
3. ✅ Basic routes and templates
4. 🔄 Implement user authentication
5. 🔄 Build job listing functionality
6. 🔄 Create application system
7. 🔄 Add search and filtering
8. 🔄 Implement admin features

---

*Last updated: August 8, 2025*