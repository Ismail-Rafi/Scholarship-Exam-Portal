from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from students.models import StudentProfile
from accounts.forms import AmbassadorRegistrationForm
from .models import AmbassadorProfile


@login_required
def ambassador_dashboard(request):
    ambassador_profile = getattr(request.user, 'ambassador_profile', None)
    
    referred_students = []
    total_registrations = 0
    
    if ambassador_profile:
        referred_students = StudentProfile.objects.filter(referred_by=ambassador_profile)
        total_registrations = referred_students.count()

    context = {
        'ambassador_profile': ambassador_profile,
        'referred_students': referred_students,
        'total_registrations': total_registrations,
    }
    return render(request, 'ambassadors/dashboard.html', context)


def register_ambassador(request):
    if request.method == 'POST':
        form = AmbassadorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            AmbassadorProfile.objects.create(
                user=user,
                phone=form.cleaned_data.get('phone'),
                institution=form.cleaned_data.get('institution')
            )
            
            messages.success(request, "🎉 রেজিস্ট্রেশন সফল হয়েছে! এখন লগইন করুন।")
            return redirect('accounts:login')
    else:
        form = AmbassadorRegistrationForm()
        
    return render(request, 'ambassadors/register.html', {'form': form})