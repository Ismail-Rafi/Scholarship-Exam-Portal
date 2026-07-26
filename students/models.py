from django.db import models
from django.conf import settings


class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    institution = models.CharField(max_length=200, blank=True)
    class_or_year = models.CharField(max_length=50, blank=True, help_text="e.g. Class 10 / 1st Year")
    address = models.TextField(blank=True)
    referred_by = models.ForeignKey(
        'ambassadors.AmbassadorProfile', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='referred_students'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class ExamRegistration(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='registrations')
    exam = models.ForeignKey('exams.Exam', on_delete=models.CASCADE, related_name='registrations')
    roll_number = models.CharField(max_length=30, unique=True, blank=True)
    is_approved = models.BooleanField(default=False, help_text="Designates whether this registration has been approved by admin.")
    registered_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.roll_number:
            self.roll_number = f"SE{self.exam_id}{self.id:05d}"
            super().save(update_fields=['roll_number'])

    def __str__(self):
        return f"{self.student} -> {self.exam} ({self.roll_number})"

    class Meta:
        unique_together = ('student', 'exam')