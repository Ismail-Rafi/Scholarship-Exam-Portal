from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import role_required
from accounts.models import User

from .models import ExamRegistration
from .forms import ExamRegistrationForm, StudentProfileForm
from payments.models import Payment
from admitcard.models import AdmitCard
from exams.models import Exam


@role_required(User.Role.STUDENT)
def dashboard(request):
    profile = request.user.student_profile
    registrations = ExamRegistration.objects.filter(student=profile).select_related('exam')
    payments = Payment.objects.filter(student=profile).select_related('exam')
    admit_cards = AdmitCard.objects.filter(registration__student=profile)

    context = {
        'profile': profile,
        'registrations': registrations,
        'payments': payments,
        'admit_cards': admit_cards,
    }
    return render(request, 'students/dashboard.html', context)


@role_required(User.Role.STUDENT)
def register_for_exam(request):
    profile = request.user.student_profile
    if request.method == 'POST':
        form = ExamRegistrationForm(request.POST)
        if form.is_valid():
            exam = form.cleaned_data['exam']
            registration, created = ExamRegistration.objects.get_or_create(student=profile, exam=exam)
            if created:
                Payment.objects.get_or_create(
                    student=profile, exam=exam,
                    defaults={'total_fee': exam.registration_fee}
                )
                messages.success(request, f"Registered for {exam.name} successfully!")
            else:
                messages.info(request, "You are already registered for this exam.")
            return redirect('students:dashboard')
    else:
        form = ExamRegistrationForm()

    exams = Exam.objects.filter(is_active=True)
    return render(request, 'students/register_exam.html', {'form': form, 'exams': exams})


@role_required(User.Role.STUDENT)
def edit_profile(request):
    profile = request.user.student_profile
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('students:dashboard')
    else:
        form = StudentProfileForm(instance=profile)
    return render(request, 'students/edit_profile.html', {'form': form})
