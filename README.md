# Admissions Tracker

This project is a web application for tracking university admissions.

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/your-username/admissions-tracker.git
   cd admissions-tracker
   ```

2. Create a virtual environment and activate it:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add the necessary environment variables:
   ```
   DJANGO_SECRET_KEY=your_secret_key_here
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

7. Open a web browser and navigate to `http://localhost:8000`

## Development vs Production

- For local development, the project uses SQLite and local file storage.
- For production, configure the necessary environment variables for database and AWS S3 storage.



## License

