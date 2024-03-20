from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from email.policy import default
from unicodedata import category
from django.db import models
from datetime import datetime


class Display(models.Model) :
    
    text = models.CharField(max_length=150) 
    url=models.URLField()
    choosenum=models.IntegerField()
    
    user= models.ManyToManyField(User)
    #codenumber=models.IntegerField(default=0)
    
    puplish_date =models.DateTimeField(default=datetime.now) 
    def __str__(self):
        return self.name
    class Meta:
        ordering =['-puplish_date']