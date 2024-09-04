release: python manage.py check
release: python manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:$PORT --workers 3 --worker-class sync admissions_tracker.wsgi:application



