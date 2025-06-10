from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class User(models.Model):
    ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('hod', 'HOD'),
    )
    
    username = models.CharField(max_length=100, unique=True, verbose_name='Username')
    email = models.EmailField(unique=True, verbose_name='Email')
    role = models.CharField(max_length=20, choices=ROLES, verbose_name='Role')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    
    def save(self, *args, **kwargs):
        # Ensure role is lowercase
        self.role = self.role.lower()
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'api_user'
    
    def __str__(self):
        return f"{self.username} ({self.role})"