from django.db import models
from django.utils import timezone

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
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('WAITLISTED', 'Waitlisted'),
        ('INTERVIEW', 'Interview Invite'),
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

    # Basic Information
    degree_type = models.CharField(max_length=5, choices=DEGREE_CHOICES)
    major = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    
    # Application Details
    application_round = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    notification_method = models.CharField(max_length=20)
    
    # Academic Information
    gpa = models.FloatField(null=True, blank=True)
    gpa_scale = models.FloatField(default=4.0)
    
    # Standardized Tests
    test_type = models.CharField(max_length=20, null=True, blank=True)
    test_score = models.IntegerField(null=True, blank=True)
    
    # Student Information
    student_type = models.CharField(max_length=13, choices=STUDENT_TYPE_CHOICES)
    continent = models.CharField(max_length=2, choices=CONTINENT_CHOICES, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)  # For domestic students
    
    # Financial Information
    financial_aid = models.BooleanField(default=False)
    scholarship = models.CharField(max_length=100, null=True, blank=True)
    
    # Post-Graduation Plans
    post_grad_plans = models.CharField(max_length=100, null=True, blank=True)
    
    # Additional Notes
    notes = models.TextField(null=True, blank=True)

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_degree_type_display()} in {self.major} at {self.university}"

    class Meta:
        ordering = ['-created_at']