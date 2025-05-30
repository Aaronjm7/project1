from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class CustomAccountManager(BaseUserManager):
    def create_user(self,email,username,first_name,password,**other_fields):
        email= self.normalize_email(email)
        user=self.model(email=email,username=username,first_name=first_name,**other_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,email,username,first_name,password,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_active',True)
        other_fields.setdefault('is_superuser',True)
        if other_fields.get('is_staff')is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email,username,first_name,password,**other_fields)

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=150,unique=True)
    first_name=models.CharField(max_length=150)
    
    is_staff =models.BooleanField(default=True)
    is_active =models.BooleanField(default=True)
    
    objects= CustomAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['username']
    
    def __str__(self):
        return self.email
class Productpage(models.Model):
 name=models.CharField(max_length=30)
 price=models.IntegerField()
 quantity=models.IntegerField()
   
