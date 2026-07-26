from django.urls import path
from . import views

app_name = 'payments'

# ⚠️ নিশ্চিত করুন নামটা একদম 'urlpatterns' (সবগুলো ছোট হাতের) এবং এটি একটি List [...]
urlpatterns = [
    # আপনার ভিউ ফাংশনের সাথে নাম মিলিয়ে নিন
    path('checkout/<int:payment_id>/', views.checkout, name='checkout'),
]

