# Generated by Django 5.1 on 2024-08-27 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admissionpost',
            name='status',
            field=models.CharField(choices=[('APPLIED', 'Applied'), ('APPLYING', 'Applying'), ('ACCEPTED', 'Accepted'), ('ACCEPTED FROM WAITLIST', 'Accepted from Waitlist'), ('REJECTED', 'Rejected'), ('REJECTED FROM WAITLIST', 'Rejected from Waitlist'), ('WAITLISTED', 'Waitlisted'), ('INTERVIEW', 'Interview Invite'), ('ENROLLED', 'Enrolled'), ('QUESTION', 'Question'), ('NOTES', 'Notes')], max_length=24),
        ),
    ]
