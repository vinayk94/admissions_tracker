# Admissions Tracker

Admissions Tracker is a web application built with Django that allows users to track and share their university admission experiences. Users can create posts about their applications, view others' experiences, and gain insights into the admission process for various universities.

## Features

- Create and view admission posts
- Basic styling with Bootstrap and custom CSS
- Simple client-side form validation with JavaScript
- Responsive design for various screen sizes

## Technology Stack

- Backend: Django 3.2
- Frontend: HTML, CSS, JavaScript
- CSS Framework: Bootstrap 4.5
- Database: SQLite (development)

## Project Structure

```
admissions_tracker/
├── admissions_tracker/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── tracker/
│   ├── migrations/
│   ├── templates/
│   │   └── tracker/
│   │       ├── base.html
│   │       ├── home.html
│   │       └── create_post.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── main.js
├── manage.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/your-username/admissions-tracker.git
   cd admissions-tracker
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Open a web browser and navigate to `http://localhost:8000`

## Development Approach

1. Project Initialization:
   - Set up Django project with a custom user model
   - Created the 'tracker' app for admission-related functionality

2. Model Design:
   - Designed the AdmissionPost model to store application details

3. View and Template Creation:
   - Implemented views for displaying and creating posts
   - Created templates using Django's template language and Bootstrap for styling

4. Form Handling:
   - Created forms for user input and implemented form processing in views

5. Static Files:
   - Added custom CSS for additional styling
   - Implemented JavaScript for client-side interactivity and form validation

6. Testing:
   - Wrote basic tests for models and views

7. Documentation:
   - Created this README for project overview and setup instructions

## Next Steps

- Implement user authentication and authorization
- Add more advanced filtering and sorting options
- Create user profiles and dashboards
- Implement a commenting system
- Add data visualization for admission trends

