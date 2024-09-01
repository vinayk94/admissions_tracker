# Generated by Django 5.1 on 2024-09-01 10:33

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('anonymous_username', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='tracker_user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='tracker_user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AdmissionPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree_type', models.CharField(choices=[('BS', 'Bachelor of Science'), ('BA', 'Bachelor of Arts'), ('MS', 'Master of Science'), ('MA', 'Master of Arts'), ('PHD', 'Doctor of Philosophy'), ('OTHER', 'Other')], max_length=5)),
                ('major', models.CharField(max_length=100)),
                ('university', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=50)),
                ('application_round', models.CharField(max_length=20)),
                ('status', models.CharField(choices=[('APPLIED', 'Applied'), ('APPLYING', 'Applying'), ('ACCEPTED', 'Accepted'), ('ACCEPTED FROM WAITLIST', 'Accepted from Waitlist'), ('REJECTED', 'Rejected'), ('REJECTED FROM WAITLIST', 'Rejected from Waitlist'), ('WAITLISTED', 'Waitlisted'), ('INTERVIEW', 'Interview Invite'), ('ENROLLED', 'Enrolled'), ('QUESTION', 'Question'), ('NOTES', 'Notes')], max_length=24)),
                ('notification_method', models.CharField(max_length=20)),
                ('gpa', models.FloatField(blank=True, null=True)),
                ('gpa_scale', models.FloatField(default=4.0)),
                ('test_type', models.CharField(blank=True, max_length=20, null=True)),
                ('test_score', models.IntegerField(blank=True, null=True)),
                ('student_type', models.CharField(choices=[('DOMESTIC', 'Domestic'), ('INTERNATIONAL', 'International')], max_length=13)),
                ('continent', models.CharField(blank=True, choices=[('AF', 'Africa'), ('AS', 'Asia'), ('EU', 'Europe'), ('NA', 'North America'), ('SA', 'South America'), ('OC', 'Oceania'), ('AN', 'Antarctica')], max_length=2, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('financial_aid', models.BooleanField(default=False)),
                ('scholarship', models.CharField(blank=True, max_length=100, null=True)),
                ('post_grad_plans', models.CharField(blank=True, max_length=100, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('notify_comments', models.BooleanField(default=False)),
                ('likes', models.ManyToManyField(blank=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='tracker.comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='tracker.admissionpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
