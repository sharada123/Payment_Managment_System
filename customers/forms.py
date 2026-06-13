from django import forms
from .models import Customer
from django.contrib.auth.models import User

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ['username', 'password']