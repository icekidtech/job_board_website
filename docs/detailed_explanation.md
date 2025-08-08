# Job Board Website - Detailed Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Setup Instructions](#setup-instructions)
4. [Database Schema](#database-schema)
5. [API Endpoints](#api-endpoints)
6. [Development Guidelines](#development-guidelines)

## Project Overview

### Purpose
This job board website allows employers to post job listings and job seekers to browse and apply for positions. The platform provides a simple, user-friendly interface for both posting and searching job opportunities.

### Technology Stack
- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL
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
│   ├── models/            # Database models
│   ├── routes/            # URL routes and views
│   └── utils/             # Utility functions
├── config/                # Configuration files
│   └── db_config.py       # Database configuration
├── docs/                  # Documentation
│   └── detailed_explanation.md
├── static/                # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/             # Jinja2 HTML templates
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── .gitignore            # Git ignore rules
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
flask run
```

## Database Schema

### Planned Tables

#### Users Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`
- `user_type` (employer/job_seeker)
- `created_at`
- `updated_at`

#### Jobs Table
- `id` (Primary Key)
- `title`
- `description`
- `company_name`
- `location`
- `salary_range`
- `job_type` (full-time/part-time/contract)
- `posted_by` (Foreign Key to Users)
- `created_at`
- `updated_at`
- `is_active`

#### Applications Table
- `id` (Primary Key)
- `job_id` (Foreign Key to Jobs)
- `user_id` (Foreign Key to Users)
- `cover_letter`
- `resume_path`
- `status` (pending/reviewed/accepted/rejected)
- `applied_at`

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
2. 🔄 Create database models
3. 🔄 Implement user authentication
4. 🔄 Build job listing functionality
5. 🔄 Create application system
6. 🔄 Design user interface
7. 🔄 Add search and filtering
8. 🔄 Implement admin features

---

*Last updated: August 8, 2025*