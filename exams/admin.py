from django.contrib import admin
from .models import Exam

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam_date', 'exam_time', 'venue', 'registration_fee', 'is_active')
    list_filter = ('is_active',)
