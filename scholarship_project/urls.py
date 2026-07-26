from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render


def direct_home_view(request):
    return render(request, 'home.html')


urlpatterns = [
    path('', direct_home_view, name='main_home'), 
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),
    path('student/', include('students.urls')),
    path('ambassador/', include('ambassadors.urls')),
    path('control-panel/', include('adminpanel.urls')),
    path('support/', include('messaging.urls')),
    path('exams/', include('exams.urls')),
    path('payments/', include('payments.urls')),
    path('admit-card/', include(('admitcard.urls', 'admitcard'), namespace='admitcard')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)