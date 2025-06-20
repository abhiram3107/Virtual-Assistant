# Generated by Django 5.1.6 on 2025-04-29 07:22

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('program', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='Username')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('role', models.CharField(choices=[('student', 'Student'), ('teacher', 'Teacher'), ('hod', 'HOD')], max_length=20, verbose_name='Role')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
            ],
            options={
                'db_table': 'api_user',
            },
        ),
        migrations.CreateModel(
            name='TeacherProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_id', models.CharField(max_length=15, unique=True, verbose_name='Teacher ID')),
                ('subjects', models.ManyToManyField(blank=True, related_name='teachers', to='program.subject', verbose_name='Subjects Taught')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_profile', to='users.user')),
            ],
            options={
                'db_table': 'api_teacher_profile',
            },
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=15, unique=True, verbose_name='Student ID')),
                ('semester', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)], default=1, verbose_name='Semester')),
                ('year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='Year')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='program.program', verbose_name='Program')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_profile', to='users.user')),
            ],
            options={
                'db_table': 'api_student_profile',
            },
        ),
        migrations.CreateModel(
            name='HodProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hod_id', models.CharField(max_length=15, unique=True, verbose_name='HOD ID')),
                ('department', models.CharField(max_length=100, verbose_name='Department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hod_profile', to='users.user')),
            ],
            options={
                'db_table': 'api_hod_profile',
            },
        ),
    ]
