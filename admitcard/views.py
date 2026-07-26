from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import AdmitCard

def view_admit(request, card_id):
    """স্টুডেন্ট বা অ্যাডমিন যেন এডমিট কার্ড দেখতে বা প্রিন্ট করতে পারে"""
    card = get_object_or_404(AdmitCard, id=card_id)
    
    if card.file:
        response = HttpResponse(card.file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="AdmitCard_{card.registration.roll_number}.pdf"'
        return response
    
    return HttpResponse("Admit card PDF file is not generated yet.", status=404)