from django.shortcuts import render
from .models import Exam

def exam_list(request):
    exams = Exam.objects.filter(is_active=True)
    return render(request, 'exams/exam_list.html', {'exams': exams})
