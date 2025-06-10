from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Program(models.Model):
    name = models.CharField(max_length=300, verbose_name='Program Name')
    institution = models.CharField(max_length=200, verbose_name='Institution', default='Default Institute')
    duration_years = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        default=4,
        verbose_name='Duration (Years)'
    )

    class Meta:
        db_table = 'api_program'

    def __str__(self):
        return f"{self.name} - {self.institution}"