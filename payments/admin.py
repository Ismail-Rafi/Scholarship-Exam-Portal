from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'total_fee', 'amount_paid', 'due_amount', 'status', 'payment_method')
    list_filter = ('status', 'exam')
    search_fields = ('student__user__username', 'transaction_id')
