from django.shortcuts import render , redirect,reverse
from urllib.parse import unquote
from .models import Display,Display_Data
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Count
# Create your views here.
class mydata:
    def __init__(self, embed_url, title, countArry, Darry, message):
        self.embed_url = embed_url
        self.title = title
        self.countArry = countArry
        self.Darry = Darry
        #self.message = message
def check_url_exists_and_person(url_to_check):
    personArray = []

    for i in range(1, 6):
        latest_successful_record = Display_Data.objects.filter(displays__url=url_to_check, choosenum=i).order_by('-date_published').first()

        if latest_successful_record:
            latest_successful_person = latest_successful_record.users
        else:
            latest_successful_person = None

        personArray.append(latest_successful_person )

       

    return personArray

def check_url_exists_and_date(url_to_check):
    dateArray = []

    for i in range(1, 6):
        latest_successful_record = Display_Data.objects.filter(displays__url=url_to_check, choosenum=i).order_by('-date_published').first()

        if latest_successful_record:
            latest_successful_date = latest_successful_record.date_published
        else:
            latest_successful_date = None

        dateArray.append(latest_successful_date )

       

    return dateArray

def check_url_exists_and_date(url_to_check):
    
    try:
        dateArray= []
        # محاولة استرداد سجل بناءً على الرابط المعطى
        #display_obj = Display.objects.get(url=url_to_check)
        
        for i in range(1, 6):
        
         latest_successful_record = Display_Data.objects.filter(displays__url=url_to_check, choosenum=i).order_by('-puplish_date').first()
         if latest_successful_record:
            latest_successful_date = latest_successful_record.puplish_date
         else:
            latest_successful_date = None

         dateArray.append(latest_successful_date )
        return dateArray  # الرابط موجود في قاعدة البيانات
    except Display.DoesNotExist:
        countArray= [0,0,0,0,0]
        return dateArray
def check_url_exists_and_evluate(url_to_check):
    try:
        countArray= []
        # محاولة استرداد سجل بناءً على الرابط المعطى
        #display_obj = Display.objects.get(url=url_to_check)
        
        for i in range(1, 6):
        # حساب عدد السجلات where choosenum = i
         count = Display_Data.objects.filter(displays__url=url_to_check, choosenum=i).count() 
         #count = Display_Data.objects.filter(display_data__url=url_to_check, choosenum=i).count()
         print(count)# إضافة عدد السجلات إلى القائمة
         countArray.append(count)
        return countArray  # الرابط موجود في قاعدة البيانات
    except Display.DoesNotExist:
        countArray= [0,0,0,0,0]
        return countArray
def display_video(request, url):
    embed_url=""
    # تشكيل الـ URL الكامل لإطار الفيديو على YouTube
    embed_url = f"https://www.youtube.com/embed/{url}"
    full_url = f"https://www.youtube.com/watch?v={url}"
    soup = BeautifulSoup(requests.get(full_url).content, "html.parser")
    title = soup.title.text
    # استخدم نموذج "display_data"
    countArry=check_url_exists_and_evluate(embed_url)
    Darry=check_url_exists_and_date(embed_url)
    data = mydata(embed_url, title, countArry, Darry)
# استخدم "Count" لحساب عدد السجلات
        

# طباعة النتيجة

                 

        # مرر الـ embed_url وعنوان الفيديو إلى القالب
    return render(request, 'display/videoA.html', {'data':data})
    #return render(request, 'display/videoA.html', {'embed_url': embed_url , 'title': title,'carry_0': countArry[0], 'carry_1': countArry[1], 'carry_2': countArry[2], 'carry_3': countArry[3], 'carry_4': countArry[4],'d0':Darry[0],'d1':Darry[1],'d2':Darry[2],'d3':Darry[3],'d4':Darry[4]})
    

def display_web(request, url):
    # تشكيل الـ URL الكامل لإطار الفيديو على YouTube
    full_url = unquote(url)

    # استخراج عنوان الموقع من URL
    soup = BeautifulSoup(requests.get(full_url).content, "html.parser")
    title = soup.title.text
    return render(request, 'display/webviewA.html', {'embed_url': full_url, 'title': title})

""" def submit_operation(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        text = request.POST.get('title')
        choosenum = request.POST.get('CHOOSE')

        if Display.objects.filter(url=url).exists():
            display = Display.objects.get(url=url)
            display_data = Display_Data.objects.create(choosenum=choosenum, user=request.user, date_published=datetime.now())
            display_data.displays.add(display)
        else:
            display = Display.objects.create(url=url, text=text)
            display_data = Display_Data.objects.create(choosenum=choosenum, user=request.user, date_published=datetime.now())
            display_data.displays.add(display)        # ... (إعادة توجيه المستخدم)

        #return redirect('searchpage') 
        return redirect(request.META.get('HTTP_REFERER')) """
def submit_operation(request):
 if request.method == 'POST':
    url = request.POST.get('url')
    text = request.POST.get('title')
    choosenum = request.POST.get('CHOOSE')

    try:
        choosenum = int(choosenum)
    except e:
       raise ValueError("couldn't convert choosenum into int")
       # or you can handle the error in a way you like

    if Display.objects.filter(url=url).exists():
        display = Display.objects.get(url=url)
        display_data = Display_Data.objects.create(choosenum=choosenum)
        display_data.displays.add(display)
        display_data.users.add(request.user)
    else:
        display = Display.objects.create(url=url, text=text)
        display_data = Display_Data.objects.create(choosenum=choosenum)
        display_data.displays.add(display)        # ... (إعادة توجيه المستخدم)
        display_data.users.add(request.user)

    #return redirect('searchpage') 
    return redirect(request.META.get('HTTP_REFERER'))