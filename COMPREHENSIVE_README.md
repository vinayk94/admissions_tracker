# Comprehensive Guide to Django Admissions Tracker Project

## Table of Contents
1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Django Basics](#django-basics)
4. [Settings](#settings)
5. [URLs and Routing](#urls-and-routing)
6. [Models](#models)
7. [Views](#views)
8. [Forms](#forms)
9. [Templates](#templates)
10. [Static Files](#static-files)
11. [User Authentication](#user-authentication)
12. [AJAX and JavaScript](#ajax-and-javascript)
13. [CSS and Styling](#css-and-styling)
14. [Testing](#testing)
15. [Deployment Considerations](#deployment-considerations)

## 1. Project Overview

This project is an Admissions Tracker application built with Django. It allows users to create and view admission posts, like posts, and comment on them. The application includes user authentication, AJAX interactions, and responsive design.

Key features:
- User registration and authentication
- Creation and display of admission posts
- Liking and commenting on posts
- Sorting and filtering posts
- Responsive design with Bootstrap

## 2. Project Structure

The project follows a typical Django project structure:

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
│   │   ├── registration/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── tracker/
│   │       ├── admission_dashboard.html
│   │       ├── base.html
│   │       ├── create_post.html
│   │       └── home.html
│   ├── templatetags/
│   │   ├── __init__.py
│   │   └── custom_filters.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── main.js
├── manage.py
└── requirements.txt
```

This structure separates the project configuration (`admissions_tracker/`) from the main application code (`tracker/`). The `static/` directory contains CSS and JavaScript files, while `templates/` holds HTML templates.

## 3. Django Basics

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It follows the Model-View-Template (MVT) architectural pattern:

- **Model**: Defines the data structure. In Django, this is where you define your database schemas and data relations.
- **View**: Contains the logic that processes the requests and returns responses.
- **Template**: Defines how the data should be presented to the user.

Key Django concepts used in this project:

- **ORM (Object-Relational Mapping)**: Django's ORM allows you to interact with your database using Python code instead of SQL.
- **URL Dispatching**: Django uses a URL configuration to map URLs to views.
- **Template Engine**: Django's template language allows you to dynamically generate HTML.
- **Forms**: Django provides a powerful form library for creating HTML forms and handling user input.
- **Authentication**: Django includes a built-in authentication system.

## 4. Settings

The project uses a split settings configuration for different environments:

- [`base.py`](admissions_tracker/settings/base.py): Contains common settings used across all environments.
- [`local.py`](admissions_tracker/settings/local.py): Settings specific to the development environment.
- [`production.py`](admissions_tracker/settings/production.py): Settings for the production environment.

Key settings in `base.py`:

```python
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')
```

These settings use environment variables for security-sensitive information, following the [12-factor app](https://12factor.net/) methodology.

The `INSTALLED_APPS` setting lists all the Django apps used in the project:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tracker',
]
```

This includes Django's built-in apps and our custom `tracker` app.

## 5. URLs and Routing

Django uses a URL configuration to map URLs to views. The main URL configuration is in [`admissions_tracker/urls.py`](admissions_tracker/urls.py):

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('tracker.urls')),
]
```

This configuration:
- Maps `/admin/` to the Django admin site.
- Includes Django's built-in authentication URLs under `/accounts/`.
- Includes the `tracker` app's URLs at the root level.

The `tracker` app has its own URL configuration in [`tracker/urls.py`](tracker/urls.py):

```python
urlpatterns = [
    path('', views.admission_dashboard, name='admission_dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('api/like/<int:post_id>/', views.like_post, name='like_post'),
    path('api/comment/<int:post_id>/', views.add_comment, name='add_comment'),
    # ... other URL patterns ...
]
```

This defines the URL structure for the application, mapping URLs to specific view functions.

## 6. Models

Models in Django represent database tables. The project defines several models in [`tracker/models.py`](tracker/models.py):

```python
class User(AbstractUser):
    anonymous_username = models.CharField(max_length=30, unique=True, blank=True, null=True)

class AdmissionPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    degree_type = models.CharField(max_length=5, choices=DEGREE_CHOICES)
    major = models.CharField(max_length=100)
    # ... other fields ...

class Comment(models.Model):
    post = models.ForeignKey(AdmissionPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    # ... other fields ...
```

Key points:
- The `User` model extends Django's `AbstractUser` to add custom fields.
- `AdmissionPost` represents a single admission post, with fields for various details about the application.
- `Comment` represents comments on admission posts, with a foreign key to both `AdmissionPost` and `User`.

## 7. Views

Views in Django handle the logic for processing requests and returning responses. The project's views are defined in [`tracker/views.py`](tracker/views.py). Here are some key views:

```python
def admission_dashboard(request):
    sort_by = request.GET.get('sort', '-created_at')
    posts = AdmissionPost.objects.annotate(comment_count=Count('comments')).order_by(sort_by)
    
    if request.method == 'POST':
        form = AdmissionPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated:
                post.user = request.user
            post.save()
            messages.success(request, "Your admission post has been created successfully.")
            return redirect('admission_dashboard')
    else:
        form = AdmissionPostForm()
    
    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'tracker/admission_dashboard.html', context)
```

This view handles both GET and POST requests for the main dashboard:
- For GET requests, it retrieves and sorts admission posts.
- For POST requests, it handles the creation of new admission posts.

Other views handle user authentication, commenting, and liking posts.

## 8. Forms

Django's form library is used to create HTML forms and handle user input. The project defines forms in [`tracker/forms.py`](tracker/forms.py):

```python
class AdmissionPostForm(forms.ModelForm):
    class Meta:
        model = AdmissionPost
        fields = ['degree_type', 'major', 'university', 'country', 'application_round', 'status', 'gpa', 'test_type', 'test_score', 'student_type', 'post_grad_plans', 'notes', 'notify_comments', 'email']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'notify_comments': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CustomUserCreationForm(UserCreationForm):
    anonymous_username = forms.CharField(max_length=30, required=False, help_text="Optional. This will be displayed instead of your username.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('anonymous_username',)
```

These forms:
- Define the fields to be included in the form.
- Specify widgets and attributes for form rendering.
- Include custom validation logic.

## 9. Templates

Django uses a template language to generate HTML dynamically. The project's main templates are located in the `tracker/templates/` directory. Here's an excerpt from [`admission_dashboard.html`](tracker/templates/tracker/admission_dashboard.html):

```html
{% extends 'tracker/base.html' %}
{% load static %}
{% load custom_filters %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-md-12">
            <h1 class="mt-4 mb-4">Admissions Tracker Dashboard</h1>
            <!-- ... other HTML ... -->
            {% for post in posts %}
            <div class="timeline-item card mb-4">
                <div class="card-body">
                    <!-- ... post details ... -->
                </div>
            </div>
            {% empty %}
            <p>No admission posts available. Be the first to submit one!</p>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/main.js' %}"></script>
{% endblock %}
```

Key points:
- The template extends a base template (`base.html`).
- It uses template tags like `{% extends %}`, `{% load %}`, and `{% block %}`.
- It includes a loop to display admission posts.
- It loads static files (CSS and JavaScript).

## 10. Static Files

Static files (CSS, JavaScript, images) are managed by Django's staticfiles app. The project's static files are located in the `static/` directory.

CSS is defined in [`static/css/styles.css`](static/css/styles.css):

```css
body {
    background-color: #f8f9fa;
}

.container {
    max-width: 800px;
}

/* ... other styles ... */
```

JavaScript is defined in [`static/js/main.js`](static/js/main.js):

```javascript
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded');

    // ... event listeners and AJAX calls ...
});
```

These files are included in the HTML templates using the `{% static %}` template tag.

## 11. User Authentication

The project uses Django's built-in authentication system, with some customizations. Key components:

- Custom user model defined in [`tracker/models.py`](tracker/models.py).
- Custom user creation form in [`tracker/forms.py`](tracker/forms.py).
- Authentication views in [`tracker/views.py`](tracker/views.py).
- Login and registration templates in `tracker/templates/registration/`.

The `@login_required` decorator is used to restrict access to certain views to authenticated users only.

## 12. AJAX and JavaScript

The project uses AJAX for dynamic interactions like liking posts and adding comments. These are implemented in [`static/js/main.js`](static/js/main.js):

```javascript
document.querySelectorAll('.like-btn').forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        const postId = this.dataset.postId;
        const isAuthenticated = this.dataset.authenticated === 'true';

        if (!isAuthenticated) {
            if (confirm('You need to log in to like this post. Go to login page?')) {
                window.location.href = `/accounts/login/?next=${encodeURIComponent(window.location.pathname)}`;
            }
            return;
        }

        fetch(`/api/like/${postId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.textContent = `Like (${data.likes_count})`;
                this.classList.toggle('liked', data.liked);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
```

This code:
- Adds click event listeners to like buttons.
- Sends AJAX requests to the server when a button is clicked.
- Updates the UI based on the server's response.

## 13. CSS and Styling

The project uses a combination of Bootstrap and custom CSS for styling. The custom styles are defined in [`static/css/styles.css`](static/css/styles.css):

```css
body {
    background-color: #f8f9fa;
}

.container {
    max-width: 800px;
}

.timeline-item {
    transition: box-shadow 0.3s ease-in-out;
}

.timeline-item:hover {
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

/* ... other styles ... */
```

These styles:
- Set a light background color for the body.
- Limit the maximum width of the main container.
- Add hover effects to timeline items.
- Define colors for different status indicators.

## 14. Testing

The project includes basic tests in [`tracker/tests.py`](tracker/tests.py):

... [Previous content remains the same]

## 14. Testing (continued)

```python
class AdmissionPostModelTest(TestCase):
    def setUp(self):
        AdmissionPost.objects.create(
            degree_type='BS',
            major='Computer Science',
            university='Test University',
            country='Test Country',
            application_round='Fall 2024',
            status='APPLIED',
            gpa=3.8,
            test_type='GRE',
            test_score=320,
            student_type='DOMESTIC'
        )

    def test_admission_post_creation(self):
        post = AdmissionPost.objects.get(university='Test University')
        self.assertEqual(post.major, 'Computer Science')
        self.assertEqual(post.status, 'APPLIED')

class AdmissionPostViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.create_post_url = reverse('create_post')

    def test_home_view(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/home.html')

    def test_create_post_view(self):
        response = self.client.get(self.create_post_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/create_post.html')

    def test_create_post_form_submission(self):
        post_data = {
            'degree_type': 'MS',
            'major': 'Data Science',
            'university': 'Test University',
            'country': 'Test Country',
            'application_round': 'Fall 2024',
            'status': 'APPLIED',
            'gpa': 3.9,
            'test_type': 'GRE',
            'test_score': 325,
            'student_type': 'INTERNATIONAL'
        }
        response = self.client.post(self.create_post_url, data=post_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertTrue(AdmissionPost.objects.filter(major='Data Science').exists())
```

These tests cover:
1. Model creation and field validation
2. View responses and template usage
3. Form submission and database updates

Testing is crucial for ensuring the reliability and correctness of your application. Django's test framework is built on top of Python's unittest module and provides additional testing tools specific to web applications.

Key testing concepts:
- `TestCase`: A base class for Django tests that provides useful methods for testing web applications.
- `setUp`: A method called before each test method to set up any objects or conditions needed for the tests.
- `Client`: A dummy Web browser for simulating GET and POST requests.
- `reverse`: A function to generate URLs by their name, as defined in `urls.py`.

To run these tests, use the command:
```
python manage.py test
```

## 15. Deployment Considerations

When deploying this Django application to a production environment, several factors need to be considered:

1. **Environment Variables**: Sensitive information like `SECRET_KEY`, database credentials, and other configuration details should be stored as environment variables, not in the code. The project already uses `os.getenv()` to read these variables.

2. **Debug Mode**: Ensure that `DEBUG` is set to `False` in production. This is handled in the `production.py` settings file:

   ```python
   DEBUG = False
   ```

3. **Static Files**: In production, you'll want to serve static files efficiently. The project is configured to use AWS S3 for static file storage in production:

   ```python
   AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
   AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
   AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
   AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
   AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

   STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
   STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
   ```

4. **Database**: The production settings use PostgreSQL instead of SQLite:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': os.getenv('DB_NAME'),
           'USER': os.getenv('DB_USER'),
           'PASSWORD': os.getenv('DB_PASSWORD'),
           'HOST': os.getenv('DB_HOST'),
           'PORT': os.getenv('DB_PORT'),
       }
   }
   ```

5. **WSGI Server**: For production, you'll need a WSGI server like Gunicorn. The `wsgi.py` file is already configured to use the production settings:

   ```python
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admissions_tracker.settings.production')
   ```

6. **Security Settings**: Ensure that `ALLOWED_HOSTS` is properly set in production to prevent HTTP Host header attacks.

7. **SSL/HTTPS**: Always use HTTPS in production. This can be configured at the web server level (e.g., Nginx) or using a service like Cloudflare.

8. **Monitoring and Logging**: Set up proper monitoring and logging for your production application. Services like Sentry can be integrated for error tracking.

## Conclusion

This Django Admissions Tracker project demonstrates many key concepts in modern web development:

1. **Model-View-Template (MVT) Architecture**: Django's interpretation of the MVC pattern, separating data models, business logic, and presentation.

2. **Database ORM**: Using Django's ORM for database operations, providing an abstraction layer over SQL.

3. **User Authentication**: Implementing user registration, login, and logout functionality using Django's built-in authentication system.

4. **Forms and Validation**: Using Django forms for data input and validation.

5. **AJAX and Frontend Interactivity**: Implementing dynamic page updates using JavaScript and AJAX calls to backend API endpoints.

6. **Responsive Design**: Using Bootstrap and custom CSS for a mobile-friendly layout.

7. **Testing**: Writing and running tests to ensure application reliability.

8. **Environment-specific Settings**: Separating settings for development and production environments.

9. **Security Considerations**: Implementing CSRF protection, using environment variables for sensitive data, and configuring production-ready settings.

10. **Deployment Readiness**: Configuring the application for production deployment, including database choice, static file serving, and WSGI server setup.

This project serves as a comprehensive example of a Django web application, covering aspects from development to deployment. It provides a solid foundation for building and understanding complex web applications using Django and modern web technologies.