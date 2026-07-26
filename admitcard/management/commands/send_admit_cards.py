"""
Management command: auto-generates & emails admit cards for students
whose exam date is coming up within ADMIT_CARD_SEND_DAYS_BEFORE days,
and who have NOT already received one, and whose payment is fully PAID.

Run daily via cron, e.g.:
    0 8 * * * /path/to/venv/bin/python manage.py send_admit_cards

(Or schedule with Celery beat for a fully automated setup.)
"""
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from students.models import ExamRegistration
from payments.models import Payment
from admitcard.utils import generate_and_send_admit_card


class Command(BaseCommand):
    help = "Auto-generate and send admit cards for upcoming exams"

    def handle(self, *args, **options):
        days_before = getattr(settings, 'ADMIT_CARD_SEND_DAYS_BEFORE', 7)
        target_date = timezone.now().date() + timedelta(days=days_before)

        registrations = ExamRegistration.objects.filter(
            exam__exam_date=target_date
        ).select_related('exam', 'student', 'student__user')

        sent_count = 0
        skipped_count = 0

        for reg in registrations:
            # Skip if admit card already sent
            if hasattr(reg, 'admit_card') and reg.admit_card.is_sent:
                skipped_count += 1
                continue

            # Only send if fully paid
            payment = Payment.objects.filter(student=reg.student, exam=reg.exam).first()
            if not payment or payment.status != Payment.Status.PAID:
                self.stdout.write(self.style.WARNING(
                    f"Skipped {reg.roll_number}: payment not completed."
                ))
                skipped_count += 1
                continue

            generate_and_send_admit_card(reg)
            sent_count += 1
            self.stdout.write(self.style.SUCCESS(f"Sent admit card: {reg.roll_number}"))

        self.stdout.write(self.style.SUCCESS(
            f"Done. Sent: {sent_count}, Skipped: {skipped_count}"
        ))
