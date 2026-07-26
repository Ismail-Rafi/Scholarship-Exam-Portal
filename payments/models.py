from django.db import models


class Payment(models.Model):
    """
    Tracks a student's registration payment for a given exam.
    total_fee - amount_paid = due automatically via a property.
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PARTIAL = 'PARTIAL', 'Partial'
        PAID = 'PAID', 'Fully Paid'

    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='payments')
    exam = models.ForeignKey('exams.Exam', on_delete=models.CASCADE, related_name='payments')
    total_fee = models.DecimalField(max_digits=8, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    payment_method = models.CharField(max_length=50, blank=True, help_text="bKash, Nagad, Cash, etc.")
    transaction_id = models.CharField(max_length=100, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def due_amount(self):
        return self.total_fee - self.amount_paid

    def save(self, *args, **kwargs):
        # auto-update status based on paid amount
        if self.amount_paid <= 0:
            self.status = self.Status.PENDING
        elif self.amount_paid < self.total_fee:
            self.status = self.Status.PARTIAL
        else:
            self.status = self.Status.PAID
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.exam} - {self.status}"

    class Meta:
        unique_together = ('student', 'exam')
