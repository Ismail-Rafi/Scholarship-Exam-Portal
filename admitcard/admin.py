from django.contrib import admin
from .models import AdmitCard

@admin.register(AdmitCard)
class AdmitCardAdmin(admin.ModelAdmin):
    list_display = ('registration', 'is_sent', 'sent_at', 'generated_at')
    list_filter = ('is_sent',)
