from django.contrib import admin
from .models import AmbassadorProfile
from students.models import StudentProfile  # স্টুডেন্ট প্রোফাইল ইমপোর্ট

@admin.register(AmbassadorProfile)
class AmbassadorProfileAdmin(admin.ModelAdmin):
    # যে ফিল্ডগুলো অ্যাডমিন টেবিল লিস্টে দেখাবে
    list_display = (
        'user', 
        'phone', 
        'referral_code', 
        'total_registrations',  # 👈 কাস্টম মেথড ১
        'total_collected'       # 👈 কাস্টম মেথড ২
    )
    search_fields = ('user__username', 'referral_code', 'phone')

    # ১. কতজন স্টুডেন্ট এই অ্যাম্বাসেডরের মাধ্যমে রেজিস্টার করেছে
    @admin.display(description='Total Registrations')
    def total_registrations(self, obj):
        return StudentProfile.objects.filter(referred_by=obj).count()

    # ২. এই অ্যাম্বাসেডরের মাধ্যমে মোট কত টাকা কালেকশন হয়েছে (যদি পেমেন্ট মডেল থাকে)
    @admin.display(description='Total Collected')
    def total_collected(self, obj):
        # যদি আপনার Payment মডেলের সাথে লিংক থাকে, তবে হিসাব হবে
        # আপাতত একটি ডামি ভ্যালু বা ০ রিটার্ন রাখা হলো যেন এরর না দেয়
        return "৳0.00"