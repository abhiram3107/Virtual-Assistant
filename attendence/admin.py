from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('subject', 'date', 'get_user', 'present')
    list_filter = ('subject', 'present', 'date')
    search_fields = ('student__user__username', 'teacher__user__username', 'subject__name')

    def get_user(self, obj):
        if obj.student:
            return f"Student: {obj.student.user.username}"
        elif obj.teacher:
            return f"Teacher: {obj.teacher.user.username}"
        return "-"
    
    get_user.short_description = 'Person'
