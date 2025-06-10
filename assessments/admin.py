from django.contrib import admin
from .models import Test, TestResult

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'chapter', 'topic', 'max_marks', 'date')
    list_filter = ('subject', 'chapter', 'topic')
    search_fields = ('name',)

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'test',
        'subject_display',
        'chapter_display',
        'topic_display',
        'marks_obtained',
        'completed_at'
    )
    list_filter = ('test__subject', 'test__chapter', 'test__topic', 'student__program')
    search_fields = ('student__user__username',)

    def subject_display(self, obj):
        return obj.subject.name
    subject_display.short_description = 'Subject'

    def chapter_display(self, obj):
        return obj.chapter.title if obj.chapter else '—'
    chapter_display.short_description = 'Chapter'

    def topic_display(self, obj):
        return obj.topic.title if obj.topic else '—'
    topic_display.short_description = 'Topic'
