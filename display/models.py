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
        # حساب عدد السجلات التي تنتمي إلى هذا العرض والتي لديها choosenum = 1 و choosenum = 2
        count_1 = self.display_data_set.filter(choosenum=1).count()
        count_2 = self.display_data_set.filter(choosenum=2).count()

        # حساب الدرجة النهائية
        total_score = count_1 - count_2
        
        
         # حساب countsucssesorfail وتحديد current
        countsucssesorfail = count_1 + count_2
        if countsucssesorfail > 5:
            current = round(countsucssesorfail / 6)  # تقريب النتيجة إلى أقرب عدد صحيح
            # استخراج عدد معين من آخر السجلات التي تقيم الموقع
           
            last_records = self.display_data_set.order_by('-puplish_date')[current:]
            # استخراج عدد السجلات التي choosenum=1 وعدد السجلات التي choosenum=2 من last_records
            count_successfulcurrent = last_records.filter(choosenum=1).count()
            count_failedcurrent = last_records.filter(choosenum=2).count()
           # حساب الدرجة النهائية
            total_score_current = count_successfulcurrent - count_failedcurrent
            total_score=total_score+total_score_current


        # تحديث درجة العرض
        self.displaydegree = total_score
        print("hello")
        print(self.displaydegree)

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


    
    