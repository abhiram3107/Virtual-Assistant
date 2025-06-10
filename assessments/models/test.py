from django.db import models
from django.core.validators import MinValueValidator

class Test(models.Model):
    subject = models.ForeignKey(
        'program.Subject',
        on_delete=models.CASCADE,
        related_name='tests',
        verbose_name='Subject'
    )
    chapter = models.ForeignKey(
        'program.Chapter',
        on_delete=models.SET_NULL,
        related_name='tests',
        verbose_name='Chapter',
        null=True,
        blank=True
    )
    topic = models.ForeignKey(
        'program.Topic',
        on_delete=models.SET_NULL,
        related_name='tests',
        verbose_name='Topic',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=255, verbose_name='Test Name')
    max_marks = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Maximum Marks'
    )
    date = models.DateField(verbose_name='Test Date')

    class Meta:
        db_table = 'api_test'

    def __str__(self):
        return f"{self.name} - {self.subject.name}"
