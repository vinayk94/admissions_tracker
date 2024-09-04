release: python manage.py check
release: python manage.py collectstatic --noinput
gunicorn --preload --worker-class gevent --bind 0.0.0.0:$PORT admissions_tracker.wsgi:application

