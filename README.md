# Job Board Website

A simple job board website built with Python Flask, HTML, CSS, JavaScript, and MySQL.

## Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Set up your database configuration in `.env`
3. Test the database connection: `python app/__init__.py`
4. Run the application: `flask run`

## Features

- **User Management**: Role-based authentication for job seekers and employers
- **Job Postings**: Create, update, and manage job listings
- **Application System**: Apply for jobs and track application status
- **Database Models**: Well-structured SQLAlchemy models for users, jobs, and applications

## Documentation

For detailed project documentation, setup instructions, database schema, and architecture details, please see:

📖 **[Detailed Documentation](docs/detailed_explanation.md)**

## Project Structure

```
job_board_website/
├── app/                    # Main application code
│   ├── models.py          # Database models (User, JobPosting, Application)
│   └── __init__.py        # App factory with database setup
├── config/                 # Configuration files
├── docs/                   # Detailed documentation
├── static/                 # CSS, JS, images
├── templates/              # HTML templates
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
└── readme.md              # This file
```

## Database Models

The application uses three main models:
- **User**: Handles both job seekers and employers with role-based access
- **JobPosting**: Manages job listings with detailed information
- **Application**: Tracks job applications and their status

See the [detailed documentation](docs/detailed_explanation.md#database-models) for complete model specifications and relationships.

## Environment Setup

Copy `.env.example` to `.env` and update the configuration values according to your setup.

## Contributing

Please refer to the [detailed documentation](docs/detailed_explanation.md) for development guidelines and project structure information.