from django import forms
from .models import Customer
from django.contrib.auth.models import User

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'tasks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'PAN Card\nIncome Certificate\nShop Act'
            }),
        }

class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ['username', 'password']


class AddServiceForm(forms.Form):
    service_name = forms.CharField(
        max_length=200,
        label="Service Name"
    )

    service_fee = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Service Fee"
    )