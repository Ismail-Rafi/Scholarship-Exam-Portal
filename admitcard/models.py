from django.db import models


class AdmitCard(models.Model):
    registration = models.OneToOneField(
        'students.ExamRegistration', on_delete=models.CASCADE, related_name='admit_card'
    )
    file = models.FileField(upload_to='admit_cards/', blank=True, null=True)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Admit Card - {self.registration.roll_number}"
