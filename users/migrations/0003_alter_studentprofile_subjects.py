# Generated by Django 5.1.6 on 2025-05-02 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0002_department'),
        ('users', '0002_studentprofile_department_studentprofile_subjects_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='subjects',
            field=models.ManyToManyField(blank=True, related_name='students', to='program.subject', verbose_name='Subjects Enrolled'),
        ),
    ]
