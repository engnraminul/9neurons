from django.forms import ModelForm
from Login.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'address', 'phone', 'university_name', 'profile_picture']
        widgets = {
            'password': forms.PasswordInput(),
        }


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password',)
        #fields = ('email', 'password_1', 'password_2',)