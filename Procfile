release: python manage.py check
release: python manage.py collectstatic --noinput
gunicorn --worker-class gevent --bind 0.0.0.0:$PORT --log-level debug admissions_tracker.wsgi:application
