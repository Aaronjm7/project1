from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model= CustomUser
        fields=['username','email','first_name','password1','password2']

class CustomAuthenticationForm(AuthenticationForm):
    username= forms.EmailField(
        widget= forms.EmailInput(attrs={
            'autofocus': True,
            'placeholder':'Enter your email'
        }),
        label="Email address"
    ) 
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder':'Enter your password'
        }),
        label="Password"
    )  
    
    class Meta:
        model=CustomUser 
        fields=('username','password')
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
        self.username_field=CustomUser._meta.get_field(CustomUser.USERNAME_FIELD)