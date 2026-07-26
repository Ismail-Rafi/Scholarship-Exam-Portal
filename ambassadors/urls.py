


from django.urls import path
from . import views

app_name = 'ambassadors'  #

urlpatterns = [
    path('dashboard/', views.ambassador_dashboard, name='dashboard'),
    path('register/', views.register_ambassador, name='register'),
]
