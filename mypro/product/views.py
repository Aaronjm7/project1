# Create your views here.
import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import connection, reset_queries
from django.db.models import F, Sum
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.lockout import (is_locked_out, record_failed_attempt,
                           reset_failed_attempts)

from .decorators import custom_decorator
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .models import CartItem, Productpage, Wishlist
from .serializers import (CartIteSerializer, ProductPageSerializer,
                          WishlistItemSerializer)
from .tasks import send_welcome_email

logger=logging.getLogger(__name__)

class ProductPageCreateAPIView(generics.ListCreateAPIView):
    queryset=Productpage.objects.all()
    serializer_class=ProductPageSerializer
    filter_backends = [SearchFilter]
    search_fields =['name']
    
    def list(self,request, *args,**kwargs):
        logger.info("Board creation attempt: ",)
        return super().list(request,*args,**kwargs)
    def create(self,request,*args,**kwargs):
        logger.info("Board creation attempt: %s",request.data)
        return super().create(request,*args,**kwargs)
    



@custom_decorator
def product_page(request):
    return render(request,'index.html')

@custom_decorator
def cart(request):
    return render(request,'cart.html')


def wishlist(request):
    return render(request,'wishlist.html')
 
    
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


class CartItemListCreateView(generics.ListCreateAPIView):
    serializer_class=CartIteSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
     return CartItem.objects.select_related('product').filter(user=self.request.user)

    
    

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        reset_queries()
        total_items = sum(item.quantity for item in queryset)
        total_price = sum(item.quantity * item.product.price for item in queryset)
        total_queries = len(connection.queries)
        print("Total SQL Queries:",total_queries)
        return Response({
            'items': serializer.data,
            'total_items': total_items,
            'total_price': total_price
        })


        
    def perform_create(self,serializer):
        serializer.save(user= self.request.user)
    


class CartItemDeleteView(generics.DestroyAPIView):
   def get_queryset(self):
     return CartItem.objects.select_related('product').filter(user=self.request.user)

    
class WishlistItemListCreateView(generics.ListCreateAPIView):
    serializer_class= WishlistItemSerializer
    permission_classes= [IsAuthenticated]
    
    def get_queryset(self):
        return Wishlist.objects.select_related('product').filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Pure Python-based calculation
        
        total_items = len(queryset)
        total_price = sum(item.product.price for item in queryset if item.product and item.product.price)

        return Response({
            'items': serializer.data,
            'total_items': total_items,
            'total_price': total_price
        })


class WishlistItemDeleteView(generics.DestroyAPIView):
    serializer_class=WishlistItemSerializer
    permission_classes=[IsAuthenticated]
    queryset= Wishlist.objects.all()
                        