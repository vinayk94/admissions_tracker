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

## Summary of Work and Issues 8/28/2024:

Authentication and User Management:

Implemented registration functionality.
Added login functionality, but users need to log in again after registration.
Added a logout button, but its functionality needs verification.
Issue: User appears authenticated even when not logged in.


Post Interactions:

Implemented like functionality, with the count increasing when clicked.
Added "Show Comments" feature, but it's not fully functional.
Comment submission form is visible, but its functionality needs verification.


UI Components:

"Select Filters" and "Submit Your Entry" buttons are present but not functioning as expected.
The toggling of these components is registered in the console, but the UI doesn't reflect the changes.


JavaScript and CSS:

Updated main.js to handle toggling of filters and form containers.
Modified CSS to style the togglable content, but visibility issues persist.


Django Views and Templates:

Updated views.py to handle user registration and login.
Modified admission_dashboard.html to include new features and debug information.



Pending Issues:

Fix authentication status display (showing authenticated when not logged in).
Ensure smooth login after registration without requiring a second login.
Verify and fix the functionality of the logout button.
Make "Select Filters" and "Submit Your Entry" components visible when toggled.
Fully implement and test the comment submission functionality.
Verify that likes are being saved correctly and associated with the correct user.

Next Steps:

Debug the authentication system to correctly reflect user status.
Review and fix the visibility issues with togglable components.
Implement proper error handling and user feedback for all interactions.
Conduct thorough testing of all implemented features.
Refactor code for better organization and maintainability.