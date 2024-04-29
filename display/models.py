from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from email.policy import default
from unicodedata import category
from django.db import models
from datetime import datetime
from  accounts.models import UserProfile



class Display(models.Model) :
    url=models.URLField(unique=True)
    text = models.CharField(max_length=150) 
    
class  Display_Data(models.Model) :
         displays = models.ManyToManyField(Display,related_name='display_data')  
         users= models.ManyToManyField(UserProfile,related_name="display_user")
         choosenum=models.IntegerField()
         puplish_date =models.DateTimeField(default=datetime.now) 
class Meta:
        ordering =['-puplish_date']

    
    