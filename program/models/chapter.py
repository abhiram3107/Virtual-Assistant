from django.db import models

class Chapter(models.Model):
    subject = models.ForeignKey(
        'program.Subject',
        on_delete=models.CASCADE,
        related_name='chapters',
        verbose_name='Subject'
    )
    title = models.CharField(max_length=255, verbose_name='Chapter Title')
    order = models.IntegerField(default=1, verbose_name='Chapter Order')

    class Meta:
        db_table = 'api_chapter'

    def __str__(self):
        return f"{self.title} - {self.subject.name}"