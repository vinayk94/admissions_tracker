```markdown
# Deployment Guide

This guide provides detailed instructions for deploying the Django Admissions Tracker project to a production environment.

## Prerequisites

- A Linux server (Ubuntu 20.04 LTS recommended)
- Python 3.8+
- PostgreSQL 12+
- Nginx
- Domain name (optional, but recommended)

## Step-by-Step Deployment

1. Server Setup
   - Update and upgrade packages:
     ```
     sudo apt update && sudo apt upgrade -y
     ```
   - Install required packages:
     ```
     sudo apt install python3-pip python3-venv postgresql nginx -y
     ```

2. Database Configuration
   - Install PostgreSQL:
     ```
     sudo apt install postgresql postgresql-contrib -y
     ```
   - Create a database and user:
     ```
     sudo -u postgres psql
     CREATE DATABASE admissions_tracker;
     CREATE USER admissions_user WITH PASSWORD 'your_secure_password';
     GRANT ALL PRIVILEGES ON DATABASE admissions_tracker TO admissions_user;
     \q
     ```

3. Application Setup
   - Clone the repository:
     ```
     git clone https://github.com/yourusername/django-admissions-tracker.git
     cd django-admissions-tracker
     ```
   - Set up virtual environment:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Install dependencies:
     ```
     pip install -r requirements.txt
     pip install gunicorn psycopg2-binary
     ```

4. Environment Configuration
   - Create a `.env` file in the project root:
     ```
     DJANGO_SECRET_KEY=your_production_secret_key
     DJANGO_DEBUG=False
     DJANGO_ALLOWED_HOSTS=your_domain.com,www.your_domain.com
     DB_NAME=admissions_tracker
     DB_USER=admissions_user
     DB_PASSWORD=your_secure_password
     DB_HOST=localhost
     DB_PORT=5432
     ```

5. Gunicorn Setup
   - Create a systemd service file `/etc/systemd/system/gunicorn_admissions.service`:
     ```
     [Unit]
     Description=gunicorn daemon for Admissions Tracker
     After=network.target

     [Service]
     User=your_username
     Group=www-data
     WorkingDirectory=/path/to/django-admissions-tracker
     ExecStart=/path/to/django-admissions-tracker/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/path/to/django-admissions-tracker/admissions_tracker.sock admissions_tracker.wsgi:application

     [Install]
     WantedBy=multi-user.target
     ```
   - Start and enable the service:
     ```
     sudo systemctl start gunicorn_admissions
     sudo systemctl enable gunicorn_admissions
     ```

6. Nginx Configuration
   - Create a new site configuration in `/etc/nginx/sites-available/admissions_tracker`:
     ```
     server {
         listen 80;
         server_name your_domain.com www.your_domain.com;

         location = /favicon.ico { access_log off; log_not_found off; }
         location /static/ {
             root /path/to/django-admissions-tracker;
         }

         location / {
             include proxy_params;
             proxy_pass http://unix:/path/to/django-admissions-tracker/admissions_tracker.sock;
         }
     }
     ```
   - Enable the site and restart Nginx:
     ```
     sudo ln -s /etc/nginx/sites-available/admissions_tracker /etc/nginx/sites-enabled
     sudo nginx -t
     sudo systemctl restart nginx
     ```

7. SSL/TLS Configuration
   - Install Certbot:
     ```
     sudo apt install certbot python3-certbot-nginx -y
     ```
   - Obtain and install a certificate:
     ```
     sudo certbot --nginx -d your_domain.com -d www.your_domain.com
     ```

8. Final Steps
   - Collect static files:
     ```
     python manage.py collectstatic
     ```
   - Run migrations:
     ```
     python manage.py migrate
     ```

## Troubleshooting

- If you encounter a "502 Bad Gateway" error, check the Gunicorn socket file permissions and the Nginx configuration.
- For database connection issues, verify the database credentials in the `.env` file and ensure the PostgreSQL service is running.
- If static files are not loading, check the `STATIC_ROOT` setting in your Django settings and ensure you've run `collectstatic`.

```