from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class StudentProfile(models.Model):
    SEMESTER = [(x, x) for x in range(1, 9)]
    
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=15, unique=True, verbose_name='Student ID')
    program = models.ForeignKey('program.Program', on_delete=models.CASCADE, related_name='students', verbose_name='Program')
    semester = models.IntegerField(choices=SEMESTER, default=1, verbose_name='Semester')
    year = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name='Year')
    department = models.ForeignKey('program.Department', on_delete=models.CASCADE, null=True, blank=True, related_name='students')
    subjects = models.ManyToManyField('program.Subject', related_name='students', blank=True, verbose_name='Subjects Enrolled')
    def save(self, *args, **kwargs):
        # Auto-set year based on semester (like your Program model)
        if self.semester:
            if self.semester in [1, 2]:
                self.year = 1
            elif self.semester in [3, 4]:
                self.year = 2
            elif self.semester in [5, 6]:
                self.year = 3
            elif self.semester in [7, 8]:
                self.year = 4
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'api_student_profile'
    
    def __str__(self):
        return f"{self.user.username} - {self.student_id} - {self.program.name}"