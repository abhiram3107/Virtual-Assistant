from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class TestResult(models.Model):
    student = models.ForeignKey(
        'users.StudentProfile',
        on_delete=models.CASCADE,
        related_name='test_results',
        verbose_name='Student'
    )
    test = models.ForeignKey(
        'assessments.Test',
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='Test'
    )
    marks_obtained = models.FloatField(
        validators=[MinValueValidator(0)],
        verbose_name='Marks Obtained'
    )
    completed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Completed At'
    )

    def save(self, *args, **kwargs):
        if self.marks_obtained > self.test.max_marks:
            self.marks_obtained = self.test.max_marks
        super().save(*args, **kwargs)

    @property
    def subject(self):
        return self.test.subject

    @property
    def chapter(self):
        return self.test.chapter

    @property
    def topic(self):
        return self.test.topic

    class Meta:
        db_table = 'api_test_result'

    def __str__(self):
        return f"{self.student.user.username} - {self.test.name} - {self.marks_obtained}/{self.test.max_marks}"


# Function to get performance summary for a student

def get_performance_summary(student):
    from collections import defaultdict
    from assessments.models import TestResult  # avoid circular import

    summary = {
        'subjects': defaultdict(lambda: {'total': 0, 'scored': 0}),
        'chapters': defaultdict(lambda: {'total': 0, 'scored': 0}),
        'topics': defaultdict(lambda: {'total': 0, 'scored': 0}),
    }

    results = TestResult.objects.filter(student=student).select_related(
        'test__subject', 'test__chapter', 'test__topic'
    )

    for result in results:
        test = result.test

        subj = test.subject.name if test.subject else "Unknown Subject"
        chap = test.chapter.title if test.chapter else "No Chapter"
        top = test.topic.title if test.topic else "No Topic"

        summary['subjects'][subj]['total'] += test.max_marks
        summary['subjects'][subj]['scored'] += result.marks_obtained

        summary['chapters'][chap]['total'] += test.max_marks
        summary['chapters'][chap]['scored'] += result.marks_obtained

        summary['topics'][top]['total'] += test.max_marks
        summary['topics'][top]['scored'] += result.marks_obtained

    # calculate percentage
    def format_result(data):
        return {
            k: {
                'accuracy': round((v['scored'] / v['total']) * 100, 2) if v['total'] else 0.0,
                'scored': v['scored'],
                'total': v['total'],
            }
            for k, v in data.items()
        }

    return {
        'subject_performance': format_result(summary['subjects']),
        'chapter_performance': format_result(summary['chapters']),
        'topic_performance': format_result(summary['topics']),
    }
