from django.shortcuts import render, HttpResponse

def checkout(request, payment_id):
    # এটি পেমেন্ট পেজের জন্য প্রাথমিক ভিউ
    return HttpResponse(f"Processing payment for ID: {payment_id}")