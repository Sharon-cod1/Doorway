from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)