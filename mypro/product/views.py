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

from .decorators import custom_decorator
from .forms import CustomUserCreationForm
from .models import Productpage
from .serializers import ProductPageSerializer

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
            form.save()
            return redirect('login')
        
    else:
        form= CustomUserCreationForm()
        return render(request,'register.html',{'form':form})
 
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from .forms import CustomAuthenticationForm


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')  # This will be the email
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product-page')
            else:
                messages.error(request, 'Invalid email or password')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

