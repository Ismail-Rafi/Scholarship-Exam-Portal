from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'placeholder': 'ইউনিক ইউজারনেম লিখুন (E.g., rahim123)',
            'class': 'form-input-field'
        })
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'placeholder': 'শিক্ষার্থীর ইমেইল ঠিকানা',
            'class': 'form-input-field'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'একটি স্ট্রং পাসওয়ার্ড দিন',
            'class': 'form-input-field'
        })
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'পাসওয়ার্ডটি আবার লিখুন',
            'class': 'form-input-field'
        })
    )

    referral_code = forms.CharField(
        label="Referral Code (Optional)",
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'রেফারেল কোড (যদি থাকে)',
            'class': 'form-input-field'
        })
    )

    institution = forms.CharField(
        label="Institution Name",
        widget=forms.TextInput(attrs={
            'placeholder': 'বিদ্যালয় বা কলেজের নাম লিখুন',
            'class': 'form-input-field'
        })
    )
    
    CLASS_CHOICES = [
        ('', 'শ্রেণি নির্বাচন করুন'),
        ('5', '৫ম শ্রেণি (Class 5)'),
        ('6', '৬ষ্ঠ শ্রেণি (Class 6)'),
        ('7', '৭ম শ্রেণি (Class 7)'),
        ('8', '৮ম শ্রেণি (Class 8)'),
        ('9', '৯ম শ্রেণি (Class 9)'),
        ('10', '১০ম শ্রেণি (Class 10)'),
    ]
    student_class = forms.ChoiceField(
        label="Class",
        choices=CLASS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select-field'
        })
    )
    
    class_roll = forms.CharField(
        label="Class Roll No",
        widget=forms.TextInput(attrs={
            'placeholder': 'শ্রেণির রোল নম্বর (E.g., 05)',
            'class': 'form-input-field'
        })
    )
    section = forms.CharField(
        label="Section / Group",
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'শাখা বা গ্রুপ লিখুন (E.g., A)',
            'class': 'form-input-field'
        })
    )

    father_name = forms.CharField(
        label="Father's Name",
        widget=forms.TextInput(attrs={
            'placeholder': 'পিতার নাম (সার্টিফিকেট অনুযায়ী)',
            'class': 'form-input-field'
        })
    )
    father_occupation = forms.CharField(
        label="Father's Occupation",
        widget=forms.TextInput(attrs={
            'placeholder': 'পিতার পেশা (E.g., ব্যবসা, চাকুরিজীবী)',
            'class': 'form-input-field'
        })
    )
    mother_name = forms.CharField(
        label="Mother's Name",
        widget=forms.TextInput(attrs={
            'placeholder': 'মাতার নাম',
            'class': 'form-input-field'
        })
    )
    mother_occupation = forms.CharField(
        label="Mother's Occupation",
        widget=forms.TextInput(attrs={
            'placeholder': 'মাতার পেশা (E.g., গৃহিণী)',
            'class': 'form-input-field'
        })
    )
    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-date-field'
        })
    )
    address = forms.CharField(
        label="Full Address",
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'গ্রাম/মহল্লা, ডাকঘর, উপজেলা, জেলা',
            'class': 'form-textarea-field'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("⚠️ এই ইউজারনেমটি ইতিমধ্যে ব্যবহৃত হয়েছে! অন্য একটি চেষ্টা করুন।")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("⚠️ পাসওয়ার্ড দুটি ম্যাচ হয়নি! আবার চেষ্টা করুন।")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        if hasattr(user, 'role'):
            user.role = 'STUDENT'
            
        if commit:
            user.save()
        return user


class AmbassadorRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'placeholder': 'ইউনিক ইউজারনেম দিন', 'class': 'form-input-field'})
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'placeholder': 'ইমেইল এড্রেস', 'class': 'form-input-field'})
    )
    phone = forms.CharField(
        label="Phone Number",
        widget=forms.TextInput(attrs={'placeholder': 'মোবাইল নম্বর', 'class': 'form-input-field'})
    )
    institution = forms.CharField(
        label="Institution Name",
        widget=forms.TextInput(attrs={'placeholder': 'কলেজ/বিশ্ববিদ্যালয়ের নাম', 'class': 'form-input-field'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'পাসওয়ার্ড', 'class': 'form-input-field'})
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'পাসওয়ার্ডটি আবার দিন', 'class': 'form-input-field'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("⚠️ এই ইউজারনেমটি ইতিমধ্যে ব্যবহৃত হয়েছে!")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("⚠️ পাসওয়ার্ড দুটি মilenি! আবার চেষ্টা করুন।")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        if hasattr(user, 'role'):
            user.role = 'AMBASSADOR'
            
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'form-input-field',
            'placeholder': 'আপনার ইউজারনেম দিন'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input-field',
            'placeholder': 'আপনার পাসওয়ার্ড দিন'
        })
    )