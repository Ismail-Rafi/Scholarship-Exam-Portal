from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register-exam/', views.register_for_exam, name='register_exam'),
    path('profile/', views.edit_profile, name='edit_profile'),
]
