from django.db import models
from django.conf import settings


class SupportMessage(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        REPLIED = 'REPLIED', 'Replied'
        CLOSED = 'CLOSED', 'Closed'

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    admin_reply = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.subject} - {self.student}"

    class Meta:
        ordering = ['-created_at']
