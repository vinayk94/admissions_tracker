from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string


class User(AbstractUser):
    anonymous_username = models.CharField(max_length=30, unique=True, blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='tracker_user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='tracker_user_set',
        related_query_name='user',
    )

    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)

    def generate_verification_token(self):
        self.verification_token = get_random_string(64)
        self.save()

    def get_display_name(self):
        return self.anonymous_username or "Anonymous User"

class AdmissionPost(models.Model):
    DEGREE_CHOICES = [
        ('BS', 'Bachelor of Science'),
        ('BA', 'Bachelor of Arts'),
        ('MS', 'Master of Science'),
        ('MA', 'Master of Arts'),
        ('PHD', 'Doctor of Philosophy'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('APPLIED', 'Applied'),
        ('APPLYING', 'Applying'),
        ('ACCEPTED', 'Accepted'),
        ('ACCEPTED FROM WAITLIST', 'Accepted from Waitlist'),
        ('REJECTED', 'Rejected'),
        ('REJECTED FROM WAITLIST', 'Rejected from Waitlist'),
        ('WAITLISTED', 'Waitlisted'),
        ('INTERVIEW', 'Interview Invite'),
        ('ENROLLED', 'Enrolled'),
        ('QUESTION', 'Question'),
        ('NOTES', 'Notes'),
    ]

    STUDENT_TYPE_CHOICES = [
        ('DOMESTIC', 'Domestic'),
        ('INTERNATIONAL', 'International'),
    ]

    CONTINENT_CHOICES = [
        ('AF', 'Africa'),
        ('AS', 'Asia'),
        ('EU', 'Europe'),
        ('NA', 'North America'),
        ('SA', 'South America'),
        ('OC', 'Oceania'),
        ('AN', 'Antarctica'),
    ]

    TERM_CHOICES = [
        ('FALL', 'Fall'),
        ('SPRING', 'Spring'),
        ('SUMMER', 'Summer'),
        ('WINTER', 'Winter'),
    ]
    year = models.IntegerField(default=2025)  # Default to 2025 for existing records
    term = models.CharField(max_length=10, choices=TERM_CHOICES, default='SPRING')  # Default to Spring for existing records
    

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    degree_type = models.CharField(max_length=5, choices=DEGREE_CHOICES)
    major = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    application_round = models.CharField(max_length=20)
    status = models.CharField(max_length=24, choices=STATUS_CHOICES)
    notification_method = models.CharField(max_length=20)
    gpa = models.FloatField(null=True, blank=True)
    gpa_scale = models.FloatField(default=4.0)
    test_type = models.CharField(max_length=20, null=True, blank=True)
    test_score = models.IntegerField(null=True, blank=True)
    student_type = models.CharField(max_length=13, choices=STUDENT_TYPE_CHOICES)
    continent = models.CharField(max_length=2, choices=CONTINENT_CHOICES, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    financial_aid = models.BooleanField(default=False)
    scholarship = models.CharField(max_length=100, null=True, blank=True)
    post_grad_plans = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(blank=True, null=True)
    notify_comments = models.BooleanField(default=False)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"{self.get_degree_type_display()} in {self.major} at {self.university}"

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    post = models.ForeignKey(AdmissionPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"Comment by {self.user.get_display_name()} on {self.post}"

    class Meta:
        ordering = ['created_at']