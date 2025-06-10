# program/models/department.py
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Department Name')

    class Meta:
        db_table = 'api_department'

    def __str__(self):
        return self.name
