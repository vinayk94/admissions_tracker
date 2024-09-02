
```markdown
# Development Guide for Django Admissions Tracker

This guide provides information for developers working on the Django Admissions Tracker project.

## Setting Up the Development Environment

1. Clone the Repository
   ```
   git clone https://github.com/vinayk94/admissions_tracker.git
   cd django-admissions-tracker
   ```

2. Set Up a Virtual Environment
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install Dependencies
   ```
   pip install -r requirements.txt
   ```

4. Configure Environment Variables
   Create a `.env` file in the project root with the following contents:
   ```
   DJANGO_SECRET_KEY=your_development_secret_key
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. Run Migrations
   ```
   python manage.py migrate
   ```

6. Create a Superuser
   ```
   python manage.py createsuperuser
   ```

7. Start the Development Server
   ```
   python manage.py runserver
   ```

## Project Structure

```
admissions_tracker/
├── admissions_tracker/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── tracker/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── templates/
│   ├── tests.py
│
```