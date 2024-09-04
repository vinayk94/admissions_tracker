release: python manage.py collectstatic --noinput
gunicorn --worker-class gevent --bind 0.0.0.0:$PORT admissions_tracker.wsgi:application
