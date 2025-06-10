from django.db import models

class HodProfile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='hod_profile')
    hod_id = models.CharField(max_length=15, unique=True, verbose_name='HOD ID')
    department = models.ForeignKey('program.Department', on_delete=models.CASCADE, null=True, blank=True, related_name='hods')
    
    class Meta:
        db_table = 'api_hod_profile'
    
    def __str__(self):
        return f"HOD: {self.user.username} - {self.hod_id} - {self.department}"