from django.urls import path
from . import views

app_name = 'admitcard'

urlpatterns = [
    path('view/<int:card_id>/', views.view_admit, name='view_admit'),
]