from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class AmbassadorRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input-field'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input-field'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input-field'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input-field'}))
    institution = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input-field'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if hasattr(user, 'role'):
            user.role = 'AMBASSADOR'  
        if commit:
            user.save()
        return user