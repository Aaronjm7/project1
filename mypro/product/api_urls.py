from django.urls import path
from .views import ProductPageCreateAPIView

urlpatterns = [
    path('product/', ProductPageCreateAPIView.as_view(), name='product-list'),
]
