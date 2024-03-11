from django.db import models

# Create your models here.
from email.policy import default
from unicodedata import category
from django.db import models
from datetime import datetime


class Display(models.Model) :
    num=models.BigAutoField()
    text = models.CharField(maxlength=150) 
    url=models.TextField()
    choosenum=models.IntegerField()
    choosepersonnum=models.IntegerField()
    #codenumber=models.IntegerField(default=0)
    
    puplish_date =models.DateTimeField(default=datetime.now) 
    def __str__(self):
        return self.name
    class Meta:
        ordering =['-puplish_date']