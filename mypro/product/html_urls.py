from django.urls import path
from .views import product_page, register, login_view,cart,wishlist

urlpatterns = [
    path('product/', product_page, name='product_page'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('', product_page, name='product-page'),# Home page
    path('cart/',cart,name='cart_view'),
    path('wishlist/',wishlist,name='wishlist_view'),
]
