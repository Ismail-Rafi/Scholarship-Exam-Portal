from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.home_view, name='home'),

    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard-redirect/', views.redirect_dashboard, name='redirect_dashboard'),
    path('main-admin/', views.main_admin_dashboard, name='admin_dashboard'),
    path('approve-registration/<int:reg_id>/', views.approve_registration, name='approve_registration'),

]
