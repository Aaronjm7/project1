from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .views import ProductPageCreateAPIView, product_page,login_view,register

urlpatterns= [
    path('api/product/',ProductPageCreateAPIView.as_view(),name='product-list'),
    path('product/',product_page,name='product_page'),
    path('register/',register,name='register'),
    path('login/',login_view,name='login'),
    path('',product_page,name='product-page')
]
print("Loaded product.api_urls with paths:")
for pattern in urlpatterns:
    print(pattern)