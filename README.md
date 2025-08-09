# Job Board Website

A simple job board website built with Python Flask, HTML, CSS, JavaScript, and MySQL.

## Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Set up your database configuration in `.env`
3. Test the database connection: `python app/__init__.py`
4. Run the application: `python run.py`
5. Visit `http://127.0.0.1:5000` in your browser

## Features

- **User Authentication**: Secure registration and login system with role-based access for job seekers and employers
- **User Management**: Role-based authentication with session management and password security
- **Job Postings**: Create, update, and manage job listings
- **Application System**: Apply for jobs and track application status
- **Database Models**: Well-structured SQLAlchemy models for users, jobs, and applications
- **Modern UI**: Responsive design with Bootstrap 5, animations, and interactive components
- **Enhanced UX**: Real-time form validation, loading states, and smooth animations

## Dashboard Features

The application includes comprehensive role-based dashboards that provide personalized user experiences:

- **Job Seeker Dashboard**: Track application status, view applied jobs, and access quick actions for job searching
- **Employer Dashboard**: Manage job postings, review applications, and monitor hiring metrics  
- **Admin Dashboard**: System-wide overview with user management, job oversight, and platform statistics

Each dashboard is tailored to specific user roles with appropriate access controls and relevant data visualization. Dashboards feature responsive design, interactive components, and real-time status tracking.

See the [detailed documentation](docs/detailed_explanation.md#dashboard-features) for complete dashboard specifications, access control details, and implementation information.

## Authentication System

The application includes a comprehensive authentication system featuring:
- **Secure Registration**: User registration with password hashing and validation
- **Session Management**: Flask sessions with configurable timeouts and "remember me" functionality
- **Role-Based Access**: Differentiated access for job seekers and employers
- **Password Security**: Werkzeug password hashing with salt generation
- **Form Validation**: Real-time validation with comprehensive error handling
- **Dynamic Navigation**: Context-aware navigation based on authentication status

Users can register as either job seekers or employers, with the interface adapting to their role. The system includes comprehensive form validation, secure password handling, and persistent sessions.

See the [detailed documentation](docs/detailed_explanation.md#authentication-system) for complete authentication specifications and security details.

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
- **Authentication** (`/login`, `/register`, `/logout`) - User authentication and session management
- **About** (`/about`) - Platform information and mission

See the [detailed documentation](docs/detailed_explanation.md#routes-and-templates) for complete route specifications and template details.

## Documentation

For detailed project documentation, setup instructions, database schema, authentication system, UI design, and architecture details, please see:

📖 **[Detailed Documentation](docs/detailed_explanation.md)**

## Project Structure

```
job_board_website/
├── app/                    # Main application code
│   ├── models.py          # Database models (User, JobPosting, Application)
│   ├── routes.py          # Flask routes and authentication logic
│   └── __init__.py        # App factory with database and session setup
├── config/                 # Configuration files
├── docs/                   # Detailed documentation
├── static/                 # CSS, JS, images
│   ├── css/
│   │   └── style.css      # Enhanced responsive styles with animations
│   └── js/
│       └── main.js        # Interactive JavaScript with validation
├── templates/              # HTML templates with Bootstrap 5
│   ├── base.html          # Base template with dynamic navigation
│   ├── home.html          # Animated homepage with statistics
│   ├── jobs.html          # Job listings with search functionality
│   ├── login.html         # Login form with validation
│   ├── register.html      # Registration form with role selection
│   └── ...                # Other templates
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── run.py                  # Application runner
└── readme.md              # This file
```

## Database Models

The application uses three main models:
- **User**: Handles both job seekers and employers with role-based access and secure authentication
- **JobPosting**: Manages job listings with detailed information
- **Application**: Tracks job applications and their status

See the [detailed documentation](docs/detailed_explanation.md#database-models) for complete model specifications and relationships.

## Environment Setup

Copy `.env.example` to `.env` and update the configuration values according to your setup.

## Contributing

Please refer to the [detailed documentation](docs/detailed_explanation.md) for development guidelines and project structure information.

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For questions or issues, please check the [detailed documentation](docs/detailed_explanation.md) or open an issue in the project repository.
