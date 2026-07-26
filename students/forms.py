from django import forms
from .models import StudentProfile, ExamRegistration


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['institution', 'class_or_year', 'address']


class ExamRegistrationForm(forms.ModelForm):
    class Meta:
        model = ExamRegistration
        fields = ['exam']
