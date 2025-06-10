# Create your models here.
from django.db import models

class Attendance(models.Model):
    subject = models.ForeignKey('program.Subject', on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(verbose_name='Session Date')

    student = models.ForeignKey('users.StudentProfile', on_delete=models.CASCADE, null=True, blank=True, related_name='attendance')
    teacher = models.ForeignKey('users.TeacherProfile', on_delete=models.CASCADE, null=True, blank=True, related_name='attendance')

    present = models.BooleanField(default=True)

    class Meta:
        db_table = 'api_attendance'
        unique_together = ('subject', 'date', 'student', 'teacher')

    def __str__(self):
        role = "Student" if self.student else "Teacher"
        user = self.student.user.username if self.student else self.teacher.user.username
        status = 'Present' if self.present else 'Absent'
        return f"{role} {user} | {self.subject.name} | {self.date} | {status}"

    @property
    def absent(self): 
        return not self.present
