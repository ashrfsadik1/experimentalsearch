from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from display.models import Display,Display_Data
from datetime import datetime
from django.utils import timezone



class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    user_nickname=models.CharField(max_length=150)
    userphoto =models.ImageField(upload_to='imageprofile/%Y/%m/%d/')
    #usershopphoto =models.ImageField(upload_to='imageshopprofile/%Y/%m/%d/')
    
    #neighborhood=models.CharField(max_length=60)
    #shopname=models.CharField(max_length=60) 
    #shopaddress=models.CharField(max_length=120)
    #zip_number=models.CharField(max_length=5)
    def __str__(self):
        return self.user.username
class UserUrl(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    url=models.URLField(default="https://www.facebook.com/profile.php?id=100068020764035")
