from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone



class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    #user_nickname=models.CharField(max_length=150)
    #nikename_url=models.URLField(default="https://www.facebook.com/profile.php?id=100068020764035")
    userphoto =models.ImageField(upload_to='imageprofile/%Y/%m/%d/')
    userdegree =models.IntegerField(default=1)

    def __str__(self):
        return self.user.username
