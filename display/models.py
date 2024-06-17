from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from email.policy import default
from unicodedata import category
from django.db import models
from datetime import datetime
from  accounts.models import UserProfile

class SearchTxt(models.Model):
       text=models.CharField(unique=True,max_length=150,default="word")
       date=models.DateTimeField(default=datetime.now)

class Display(models.Model):
    searchtxt = models.ForeignKey(SearchTxt, on_delete=models.CASCADE, default=1)
    url = models.URLField(unique=True)
    text = models.CharField(max_length=150)
    isyoutube = models.BooleanField(default=True)
    displaydegree = models.IntegerField(default=1)

    def evaluate_site(self):
        total_score = 0
        display_data_records = self.display_data_set.all()
        for record in display_data_records:
            if record.choosenum == 1:
                total_score += 1
            elif record.choosenum == 2:
                total_score -= 1
        self.displaydegree = total_score
        self.save()

class Display_Data(models.Model):
    displays = models.ForeignKey(Display, on_delete=models.CASCADE, default=1)
    users = models.ManyToManyField(UserProfile, default=1)
    choosenum = models.IntegerField()
    puplish_date = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        super(Display_Data, self).save(*args, **kwargs)
        self.displays.evaluate_site()

    class Meta:
        ordering = ['-puplish_date']


    
    