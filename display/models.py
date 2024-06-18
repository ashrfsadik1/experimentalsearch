from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from email.policy import default
from unicodedata import category
from django.db import models
from datetime import datetime
from  accounts.models import UserProfile
from django.db.models import Count, Sum

class SearchTxt(models.Model):
       text=models.CharField(unique=True,max_length=150,default="word")
       date=models.DateTimeField(default=datetime.now)

class Display(models.Model):
    
    url = models.URLField(unique=True)
    text = models.CharField(max_length=150)
    isyoutube = models.BooleanField(default=True)
    displaydegree = models.IntegerField(default=1)

    def evaluate_site(self):
        # الحصول على عدد السجلات التي تساوي 1 وعدد السجلات التي تساوي 2
        aggregates = self.display_data_set.aggregate(
            count_1=Count('id', filter=models.Q(choosenum=1)),
            count_2=Count('id', filter=models.Q(choosenum=2))
        )

        count_1 = aggregates['count_1'] or 0
        count_2 = aggregates['count_2'] or 0
        print("hello")
        print (count_1)
        print(count_2)
        # حساب الدرجة النهائية
        total_score = count_1 - count_2
        print("hi")
        print(total_score)

        # تحديث درجة العرض
        self.displaydegree = total_score
        self.save()
class searchtxt_display(models.Model):
     searchtxt = models.ForeignKey(SearchTxt, on_delete=models.CASCADE, default=1)
     display=models.ForeignKey(Display,on_delete=models.CASCADE,default=1)
     
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


    
    