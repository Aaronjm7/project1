from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from utils.lockout import is_locked_out, record_failed_attempt

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            'placeholder': 'Enter your email'
        }),
        label="Email address"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password'
        }),
        label="Password"
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username_field = CustomUser._meta.get_field(CustomUser.USERNAME_FIELD)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and is_locked_out(username):
            raise ValidationError(
                "Account locked due to too many incorrect logins.",
                code='locked_out'
            )

        user = authenticate(self.request, username=username, password=password)

        if user is None:
            if username:
                record_failed_attempt(username)
            raise ValidationError(
                "Please enter a correct email and password. Note that both fields may be case-sensitive.",
                code='invalid_login'
            )

        self.confirm_login_allowed(user)
        return self.cleaned_data
