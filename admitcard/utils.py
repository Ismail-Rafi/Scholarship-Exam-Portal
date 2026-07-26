import io
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from .models import AdmitCard


def generate_admit_card_pdf(registration):
    """Builds a PDF admit card in-memory and returns bytes."""
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    student = registration.student
    exam = registration.exam
    user = student.user

    exam_date_str = exam.exam_date.strftime('%d %B %Y') if getattr(exam, 'exam_date', None) else "To be announced"
    exam_time_str = exam.exam_time.strftime('%I:%M %p') if getattr(exam, 'exam_time', None) else "See Instructions"
    venue_str = getattr(exam, 'venue', 'Main Campus')

    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width / 2, height - 60, "SCHOLARSHIP EXAM ADMIT CARD")

    p.setFont("Helvetica", 12)
    lines = [
        f"Exam Name       : {exam.name}",
        f"Roll Number     : {registration.roll_number}",
        f"Student Name    : {user.get_full_name() or user.username}",
        f"Institution     : {student.institution or 'N/A'}",
        f"Exam Date       : {exam_date_str}",
        f"Exam Time       : {exam_time_str}",
        f"Venue           : {venue_str}",
    ]
    y = height - 120
    for line in lines:
        p.drawString(70, y, line)
        y -= 30

    p.setFont("Helvetica-Oblique", 9)
    p.drawString(70, 80, "Please bring this admit card and a valid photo ID to the exam hall.")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer.getvalue()


def generate_and_send_admit_card(registration):
    """Generates the PDF, saves it, and emails it to the student."""
    admit_card, _ = AdmitCard.objects.get_or_create(registration=registration)

    pdf_bytes = generate_admit_card_pdf(registration)
    filename = f"admit_card_{registration.roll_number}.pdf"
    
    admit_card.file.save(filename, ContentFile(pdf_bytes), save=False)

    student_email = registration.student.user.email if hasattr(registration.student, 'user') else None
    if student_email:
        email = EmailMessage(
            subject=f"Your Admit Card - {registration.exam.name}",
            body=(
                f"Dear {registration.student.user.get_full_name() or registration.student.user.username},\n\n"
                f"Your admit card for {registration.exam.name} is attached.\n"
                f"Roll Number: {registration.roll_number}\n"
                f"Exam Date: {registration.exam.exam_date}\n\n"
                f"Best of luck!\nScholarship Exam Team"
            ),
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@scholarship.com'),
            to=[student_email],
        )
        email.attach(filename, pdf_bytes, 'application/pdf')
        email.send(fail_silently=True)

    admit_card.is_sent = True
    admit_card.sent_at = timezone.now()
    admit_card.save()
    return admit_card