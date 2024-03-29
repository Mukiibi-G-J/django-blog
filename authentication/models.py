from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomManager(BaseUserManager):
    def create_user(self, email, username, first_name,last_name,phone_number, password=None,**extra_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name ,last_name=last_name, phone_number=phone_number, **extra_fields)
        
        user.set_password(password)                
            
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email, username, first_name,last_name, phone_number,password=None, **extra_fields, ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super user must be assigned to is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Super user must be assigned to is_superuser=True')
        user = self.create_user(email, username, first_name, last_name, phone_number, password, **extra_fields)
        # user.is_staff = True
        # user.is_superuser = True
        user.save(using=self._db)
        return user
 
    
   
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
        email = models.EmailField(_('email address'), unique=True)
        username = models.CharField(max_length=255, unique=True)
        first_name = models.CharField(max_length=255)
        last_name = models.CharField(max_length=255)
        phone_number = models.CharField(max_length=255)
        start_date = models.DateField(default=timezone.now)
        about = models.TextField(_('about'), blank=True, max_length=255)
        is_staff = models.BooleanField(default=False)
        otp = models.CharField(max_length=255, blank=True)
        is_verified = models.BooleanField(default=False)
        is_staff = models.BooleanField(default=False)
        is_superuser = models.BooleanField(default=False)
        
        objects = CustomManager()
        
        
        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['username', 'first_name', 'last_name', "phone_number"]
        
        def _str_(self):
            return self.username
            
        

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    