# Django Admissions Tracker

Django Admissions Tracker is a web application designed to help students track and share their college or graduate school admission processes. Users can create posts about their application experiences, view others' experiences, and interact through likes and comments.

## Features

- User Registration and Authentication
- Create, Read, Update, and Delete Admission Posts
- Like and Comment on Posts
- Anonymous Posting Option
- Sorting and Filtering of Posts
- Responsive Design for Mobile and Desktop
- AJAX-powered Interactions for Smooth User Experience

## Technology Stack

- Backend: Django 3.x
- Frontend: HTML, CSS, JavaScript
- Database: SQLite (Development) / PostgreSQL (Production)
- CSS Framework: Bootstrap 4
- AJAX: Fetch API
- Deployment: Gunicorn, Nginx (Production)

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- virtualenv

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/django-admissions-tracker.git
   cd django-admissions-tracker
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add the following:
   ```
   DJANGO_SECRET_KEY=your_secret_key_here
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

8. Visit `http://localhost:8000` in your browser to view the application.

## Documentation

For more detailed information, please refer to the following documentation:

- [Deployment Guide](docs/deployment.md)
- [Contributing Guidelines](docs/contributing.md)
- [API Documentation](docs/api.md)
- [User Guide](docs/user_guide.md)
- [Development Guide](docs/development.md)

## Testing

To run the test suite:

```
python manage.py test
```



## Acknowledgments

- Django community for the amazing web framework
- Bootstrap team for the responsive CSS framework
- All contributors who have helped shape this project

