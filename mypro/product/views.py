# Create your views here.
import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.lockout import (is_locked_out, record_failed_attempt,
                           reset_failed_attempts)

from .decorators import custom_decorator
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .models import Productpage
from .serializers import ProductPageSerializer
from .tasks import send_welcome_email

logger=logging.getLogger(__name__)

class ProductPageCreateAPIView(generics.ListCreateAPIView):
    queryset=Productpage.objects.all()
    serializer_class=ProductPageSerializer
    
    
    def list(self,request, *args,**kwargs):
        logger.info("Board creation attempt: ",)
        return super().list(request,*args,**kwargs)
    def create(self,request,*args,**kwargs):
        logger.info("Board creation attempt: %s",request.data)
        return super().create(request,*args,**kwargs)
@custom_decorator
def product_page(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Capture the user instance
            send_welcome_email.delay(user.id)  # Call Celery task
            return redirect('login')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        logger.debug("Login attempt with POST data: %s", request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            logger.info(f"User {username} authenticated successfully.")
            login(request, form.get_user())
            reset_failed_attempts(username)
            return redirect('product-page')
        else:
            logger.debug(f"Form errors: {form.errors.as_json()}")
            messages.error(request, form.errors.get('__all__')[0])
    else:
        form = CustomAuthenticationForm()
        logger.debug("GET request for login page.")

    return render(request, 'login.html', {'form': form})