from django.db import models

class TeacherProfile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='teacher_profile')
    teacher_id = models.CharField(max_length=15, unique=True, verbose_name='Teacher ID')
    subjects = models.ManyToManyField('program.Subject', related_name='teachers', blank=True, verbose_name='Subjects Taught')
    department = models.ForeignKey('program.Department', null=True, blank=True,on_delete=models.CASCADE, related_name='teachers')
    class Meta:
        db_table = 'api_teacher_profile'
    
    def __str__(self):
        return f"{self.user.username} - {self.teacher_id}"