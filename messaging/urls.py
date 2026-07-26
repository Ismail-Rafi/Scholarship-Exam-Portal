from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('new/', views.send_message, name='send_message'),
    path('my-messages/', views.my_messages, name='my_messages'),
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/<int:pk>/reply/', views.reply_message, name='reply_message'),
]
