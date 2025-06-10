from django.contrib import admin
from .models import User, StudentProfile, TeacherProfile, HodProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'created_at')
    search_fields = ('username', 'email')
    list_filter = ('role',)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'program', 'semester', 'year')
    list_filter = ('program', 'semester', 'year')
    search_fields = ('student_id', 'user__username')

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'teacher_id')
    search_fields = ('teacher_id', 'user__username')
    filter_horizontal = ('subjects',)

@admin.register(HodProfile)
class HodProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'hod_id', 'department')
    search_fields = ('hod_id', 'user__username')
