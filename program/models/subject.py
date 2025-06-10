from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Subject(models.Model):
    SEMESTER = [(x, x) for x in range(1, 9)]

    program = models.ForeignKey(
        'program.Program',
        on_delete=models.CASCADE,
        related_name='subjects',
        verbose_name='Program'
    )
    name = models.CharField(max_length=255, verbose_name='Subject Name')
    semester = models.IntegerField(
        choices=SEMESTER,
        default=1,
        verbose_name='Semester'
    )

    class Meta:
        db_table = 'api_subject'

    def __str__(self):
        return f"{self.name} (Sem {self.semester} - {self.program.name})"