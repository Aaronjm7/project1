"""
URL configuration for mypro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view=get_schema_view(
    openapi.Info(
        title="Products",
        default_version="v1",
        description="API documentation using Swagger",
        terms_of_service="https://youtu.be/dQw4w9WgXcQ?si=4c_JUd2IUnZjwqbJ",
        contact=openapi.Contact(email="aaronjma7@gmail.com"),
        license=openapi.License(name="Lol"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.html_urls')),
    path('api/',include('product.api_urls')),
    path('swagger/',schema_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-ui'),
    path('redoc/',schema_view.with_ui('redoc',cache_timeout=0),name='schema-redoc'),
]

