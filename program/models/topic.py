from django.db import models

class Topic(models.Model):
    chapter = models.ForeignKey(
        'program.Chapter',
        on_delete=models.CASCADE,
        related_name='topics',
        verbose_name='Chapter'
    )
    title = models.CharField(max_length=255, verbose_name='Topic Title')
    order = models.IntegerField(default=1, verbose_name='Topic Order')

    class Meta:
        db_table = 'api_topic'

    def __str__(self):
        return f"{self.title} - {self.chapter.title}"