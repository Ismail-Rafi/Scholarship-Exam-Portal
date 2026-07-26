from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .forms import StudentRegistrationForm, AmbassadorRegistrationForm, LoginForm
from .models import User
from exams.models import Exam
from students.models import ExamRegistration
from admitcard.models import AdmitCard

try:
    from admitcard.utils import generate_and_send_admit_card
except ImportError:
    from admitcard.services import generate_and_send_admit_card


def home_view(request):
    all_exams = Exam.objects.all().order_by('registration_deadline')
    return render(request, 'home.html', {'exams': all_exams})


def register_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            referral_code = form.cleaned_data.get('referral_code')
            from students.models import StudentProfile
            from ambassadors.models import AmbassadorProfile

            ambassador = None
            if referral_code:
                ambassador = AmbassadorProfile.objects.filter(
                    referral_code=referral_code
                ).first()
                if not ambassador:
                    messages.warning(request, "Referral code not found. Registered without an ambassador link.")

            StudentProfile.objects.create(user=user, referred_by=ambassador)

            login(request, user)
            messages.success(request, "Registration successful! Welcome.")
            return redirect('accounts:redirect_dashboard')
    else:
        form = StudentRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if user.is_staff or user.is_superuser:
                return redirect('accounts:admin_dashboard')
            elif hasattr(user, 'role') and user.role == 'AMBASSADOR':
                return redirect('ambassadors:dashboard')
            else:
                return redirect('students:dashboard')
        else:
            messages.error(request, "⚠️ ইউজারনেম বা পাসওয়ার্ড ভুল হয়েছে!")
    else:
        form = AuthenticationForm()
        
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def redirect_dashboard(request):
    user = request.user

    if user.is_staff or user.is_superuser:
        return redirect('accounts:admin_dashboard')
    elif hasattr(user, 'role') and user.role == 'AMBASSADOR':
        return redirect('ambassadors:dashboard')
    else:
        return redirect('students:dashboard')


@staff_member_required(login_url='accounts:login')
def main_admin_dashboard(request):
    registrations = ExamRegistration.objects.select_related('student', 'exam').order_by('-registered_at')
    
    context = {
        'registrations': registrations,
        'total_applicants': registrations.count(),
        'pending_count': registrations.filter(is_approved=False).count(),
        'approved_count': registrations.filter(is_approved=True).count(),
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@staff_member_required(login_url='accounts:login')
def approve_registration(request, reg_id):
    registration = get_object_or_404(ExamRegistration, id=reg_id)
    
    registration.is_approved = True
    registration.save()
    
    try:
        generate_and_send_admit_card(registration)
        messages.success(request, f"✅ {registration.student}-এর আবেদন অ্যাপ্রুভ করা হয়েছে এবং ইমেইলে এডমিট কার্ড পাঠানো হয়েছে!")
    except Exception as e:
        AdmitCard.objects.get_or_create(registration=registration)
        messages.warning(request, f"✅ আবেদন অ্যাপ্রুভ হয়েছে, কিন্তু ইমেইল পাঠাতে সমস্যা হয়েছে: {e}")
        
    return redirect('accounts:admin_dashboard')