from django.contrib import admin
from .models import StudentProfile, ExamRegistration

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'institution', 'class_or_year', 'referred_by')
    search_fields = ('user__username', 'user__email')

@admin.register(ExamRegistration)
class ExamRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'roll_number', 'registered_at')
    search_fields = ('roll_number', 'student__user__username')
