
from django.shortcuts import render
from django.db.models import Sum, Count

from accounts.decorators import role_required
from accounts.models import User

from students.models import ExamRegistration, StudentProfile
from payments.models import Payment
from ambassadors.models import AmbassadorProfile
from messaging.models import SupportMessage
from exams.models import Exam


@role_required(User.Role.ADMIN)
def admin_dashboard(request):
    total_forms_sold = ExamRegistration.objects.count()
    total_paid = Payment.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    total_fee_expected = Payment.objects.aggregate(Sum('total_fee'))['total_fee__sum'] or 0
    total_due = total_fee_expected - total_paid

    ambassadors = AmbassadorProfile.objects.all()
    ambassador_stats = [
        {
            'name': a.user.get_full_name() or a.user.username,
            'code': a.referral_code,
            'registrations': a.total_registrations,
            'collected': a.total_collected,
            'due': a.total_due,
        }
        for a in ambassadors
    ]

    open_messages = SupportMessage.objects.filter(status=SupportMessage.Status.OPEN).count()

    context = {
        'total_forms_sold': total_forms_sold,
        'total_paid': total_paid,
        'total_due': total_due,
        'total_fee_expected': total_fee_expected,
        'ambassador_stats': ambassador_stats,
        'open_messages': open_messages,
        'exams': Exam.objects.all(),
        'total_students': StudentProfile.objects.count(),
    }
    return render(request, 'adminpanel/admin_dashboard.html', context)


@role_required(User.Role.STAFF)
def staff_dashboard(request):
    """
    Secure but LIMITED panel -- staff can view students / registrations /
    support messages, but financial figures are intentionally excluded.
    """
    students = StudentProfile.objects.select_related('user').all()[:50]
    registrations = ExamRegistration.objects.select_related('student__user', 'exam').all()[:50]
    open_messages = SupportMessage.objects.filter(status=SupportMessage.Status.OPEN)

    context = {
        'students': students,
        'registrations': registrations,
        'open_messages': open_messages,
    }
    return render(request, 'adminpanel/staff_dashboard.html', context)
