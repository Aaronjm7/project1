from django.urls import path
from .views import ProductPageCreateAPIView,CartItemDeleteView,CartItemListCreateView,WishlistItemListCreateView,WishlistItemDeleteView

urlpatterns = [
    path('product/', ProductPageCreateAPIView.as_view(), name='product-list'),
    path('cart/',CartItemListCreateView.as_view(),name='api-cart-list'),
    path('cart/<int:pk>/',CartItemDeleteView.as_view(),name='api-cart-delete'),
    path('wishlist/',WishlistItemListCreateView.as_view(),name='wishlist'),
    path('wishlist/<int:pk>/',WishlistItemDeleteView.as_view(),name='wishlist-delete'),
]
