# Job Board Website

A simple job board website built with Python Flask, HTML, CSS, JavaScript, and MySQL.

## Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Set up your database configuration in `.env`
3. Test the database connection: `python app/__init__.py`
4. Run the application: `python run.py`
5. Visit `http://127.0.0.1:5000` in your browser

## Features

- **User Management**: Role-based authentication for job seekers and employers
- **Job Postings**: Create, update, and manage job listings
- **Application System**: Apply for jobs and track application status
- **Database Models**: Well-structured SQLAlchemy models for users, jobs, and applications
- **Modern UI**: Responsive design with Bootstrap 5, animations, and interactive components
- **Enhanced UX**: Real-time form validation, loading states, and smooth animations

## User Interface

The application features a modern, responsive user interface with:
- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Interactive Components**: Animated statistics, hover effects, and smooth transitions
- **Form Validation**: Real-time validation with visual feedback and error handling
- **Loading States**: User-friendly loading indicators and progress feedback
- **Accessibility**: WCAG-compliant design with keyboard navigation and screen reader support

See the [detailed documentation](docs/detailed_explanation.md#user-interface-design) for complete UI specifications and design system details.

## Routes

The application includes the following main routes:
- **Homepage** (`/`) - Welcome page with platform overview and animated statistics
- **Job Listings** (`/jobs`) - Browse and search job postings with advanced filtering
- **Login** (`/login`) - User authentication with enhanced validation
- **Registration** (`/register`) - New user account creation
- **About** (`/about`) - Platform information and mission

See the [detailed documentation](docs/detailed_explanation.md#routes-and-templates) for complete route specifications and template details.

## Documentation

For detailed project documentation, setup instructions, database schema, UI design, and architecture details, please see:

📖 **[Detailed Documentation](docs/detailed_explanation.md)**

## Project Structure

```
job_board_website/
├── app/                    # Main application code
│   ├── models.py          # Database models (User, JobPosting, Application)
│   ├── routes.py          # Flask routes and views
│   └── __init__.py        # App factory with database setup
├── config/                 # Configuration files
├── docs/                   # Detailed documentation
├── static/                 # CSS, JS, images
│   ├── css/
│   │   └── style.css      # Enhanced responsive styles with animations
│   └── js/
│       └── main.js        # Interactive JavaScript with validation
├── templates/              # HTML templates with Bootstrap 5
│   ├── base.html          # Base template with navigation
│   ├── home.html          # Animated homepage with statistics
│   ├── jobs.html          # Job listings with search functionality
│   ├── login.html         # Login form with validation
│   └── ...                # Other templates
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── run.py                  # Application runner
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