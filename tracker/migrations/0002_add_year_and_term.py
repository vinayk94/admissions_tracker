from django.db import migrations, models

def set_default_year_and_term(apps, schema_editor):
    AdmissionPost = apps.get_model('tracker', 'AdmissionPost')
    for post in AdmissionPost.objects.all():
        post.year = 2025
        post.term = 'SPRING'
        post.save()

class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),  # replace with your last migration
    ]

    operations = [
        migrations.AddField(
            model_name='admissionpost',
            name='year',
            field=models.IntegerField(default=2025),
        ),
        migrations.AddField(
            model_name='admissionpost',
            name='term',
            field=models.CharField(choices=[('FALL', 'Fall'), ('SPRING', 'Spring'), ('SUMMER', 'Summer'), ('WINTER', 'Winter')], default='SPRING', max_length=10),
        ),
        migrations.RunPython(set_default_year_and_term),
    ]