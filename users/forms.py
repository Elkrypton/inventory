from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import AccountUser
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):

    class Meta:
        model = AccountUser
        fields = ['email','first_name', 'last_name','password1', 'password2']

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        try:
            validate_password(password1, self.instance)
        
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        
        return password1
