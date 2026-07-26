import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_referral_code():
    return f"AMB-{uuid.uuid4().hex[:6].upper()}"


class AmbassadorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ambassador_profile')
    phone = models.CharField(max_length=15)
    institution = models.CharField(max_length=200)
    referral_code = models.CharField(
        max_length=20, 
        unique=True, 
        default=generate_referral_code 
    )

    def __str__(self):
        return f"{self.user.username} - {self.referral_code}"