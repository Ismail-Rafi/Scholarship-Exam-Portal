from django.db import models


class Exam(models.Model):
    """A scholarship exam event. e.g. 'Scholarship Exam 2026'"""
    name = models.CharField(max_length=200)
    exam_date = models.DateField()
    exam_time = models.TimeField()
    venue = models.CharField(max_length=255)
    registration_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    registration_deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.exam_date})"

    class Meta:
        ordering = ['-exam_date']
