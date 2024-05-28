from django.shortcuts import render , redirect,reverse
from urllib.parse import unquote,urlparse

from .models import Display,Display_Data
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Count
from accounts.models import UserProfile
import re


# Create your views here.
class mydata:
    def __init__(self, embed_url, title, countArry, Darry):
        self.embed_url = embed_url
        self.title = title
        self.countArry = countArry
        self.Darry = Darry
        
 

# def check_url_exists_and_person(url_to_check):
#     user_info_array = []

#     for i in range(1, 6):
#         latest_successful_record = Display_Data.objects.filter(displays__url=url_to_check, choosenum=i).order_by('-puplish_date').first()

#         if latest_successful_record:  # Check if record exists before accessing attributes
#             user_info = {
#                 'user_nickname': latest_successful_record.users.user_nickname,
#                 'url': latest_successful_record.users.nikename_url,
#             }
#             user_info_array.append(user_info)
#         else:
#             # Handle the case where no matching record is found (optional)
#             # You can add logic here to handle missing data, e.g., return an empty dictionary
#             pass

#     return user_info_array
          

def check_url_exists_and_date(url_to_check):
    dateArray = []

    for i in range(1, 6):
        latest_successful_record = Display_Data.objects.filter(displays__url=url_to_check, choosenum=i).order_by('-date_published').first()

        if latest_successful_record:
            latest_successful_date = latest_successful_record.puplish_date
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
         # إضافة عدد السجلات إلى القائمة
         countArray.append(count)
        return countArray  # الرابط موجود في قاعدة البيانات
    except Display.DoesNotExist:
        countArray= [0,0,0,0,0]
        return countArray
def display_video(request, url):
    
    # تشكيل الـ URL الكامل لإطار الفيديو على YouTube
    embed_url = f"https://www.youtube.com/embed/{url}"
    full_url = f"https://www.youtube.com/watch?v={url}" #للاستخلاص من خلال الامر soup
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
    embed_url = unquote(url)

    # استخراج عنوان الموقع من URL
    soup = BeautifulSoup(requests.get(embed_url).content, "html.parser")
    title = soup.title.text
    countArry=check_url_exists_and_evluate( embed_url)
    Darry=check_url_exists_and_date( embed_url)
    print ( embed_url)
    print(title)
    
    
    data = mydata( embed_url, title, countArry, Darry)
    return render(request, 'display/webviewA.html', {'data':data })
def is_youtube_url(url):

    #https://www.youtube.com/embed/CGMCEw5Cfjo
   youtube_regex = r"^https?://(?:www\.)?youtube\.com/(?:embed/|v/|watch\?v=|playlist\?list=)(?P<video_id>[a-zA-Z0-9-_]{11})"
   match = re.search(youtube_regex, url)
    
   return bool(match)


def submit_operation(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        
    if is_youtube_url(url):
        isyoutube=True
    else:
        isyoutube=False    

           
        # ال URL ليس خاص بيوتيوب
        # قم بتنفيذ الإجراء المناسب هنا
    text = request.POST.get('title')
    choosenum = request.POST.get('CHOOSE')
        
        
    choosenum = int(choosenum)
        #display=Display.objects.get(url=url,text=text)
    try:
            display = Display.objects.get(url=url, text=text)
    except :
            display = Display(url=url, text=text,isyoutube=isyoutube)
            display.save()

       # Import the UserProfile model
    user_profile = UserProfile.objects.get(user=request.user)
    
    #print(display.index)
    display_data = Display_Data.objects.create(displays=display,choosenum=choosenum)
    display_data.users.add(user_profile)
    

        
        #display_data.users.add(request.user)  # Add user to Display_Data

        # ... (Redirect user)
    return redirect(request.META.get('HTTP_REFERER'))
def displaymyoperations(request):
    # استرداد بيانات المستخدم الحالي
    current_user = request.user
    print("helllo")
    print(current_user)
    userprofile=UserProfile.objects.get(user=current_user)
    # استعلام بيانات العروض التي قام المستخدم بتقييمها
    display_data = Display_Data.objects.filter(users=userprofile).order_by('-puplish_date')

    #display_data = Display_Data.objects.filter(users=userprofile)
    # تحويل قيمة التقييم إلى نص وصفي
    for display_datum in display_data:
        if display_datum.choosenum == 1:
            display_datum.choosenum_text = "نجاح"
        elif display_datum.choosenum == 2:
            display_datum.choosenum_text = "فشل"
        elif display_datum.choosenum == 3:
            display_datum.choosenum_text = "بحاجة إلى مال"
        elif display_datum.choosenum == 4:
            display_datum.choosenum_text = "بحاجة إلى أدوات"
        else:
            display_datum.choosenum_text = "مؤجل"

   
    # تحضير سياق العرض (context)
    context = {
        'display_data': display_data,
         
    }
    print("hello")
    print (context)

    # عرض القالب (template) مع البيانات
    return render(request, 'display/displaymyoperations.html', context)
def displaymydelayoperations(request):
    # استرداد بيانات المستخدم الحالي
    current_user = request.user
    print("helllo")
    print(current_user)
    userprofile=UserProfile.objects.get(user=current_user)
    # استعلام بيانات العروض التي قام المستخدم بتقييمها
    display_data = Display_Data.objects.filter(users=userprofile,choosenum=5).order_by('-puplish_date')

    #display_data = Display_Data.objects.filter(users=userprofile)
    # تحويل قيمة التقييم إلى نص وصفي
    for display_datum in display_data:
        if display_datum.choosenum == 1:
            display_datum.choosenum_text = "نجاح"
        elif display_datum.choosenum == 2:
            display_datum.choosenum_text = "فشل"
        elif display_datum.choosenum == 3:
            display_datum.choosenum_text = "بحاجة إلى مال"
        elif display_datum.choosenum == 4:
            display_datum.choosenum_text = "بحاجة إلى أدوات"
        else:
            display_datum.choosenum_text = "مؤجل"

   
    # تحضير سياق العرض (context)
    context = {
        'display_data': display_data,
         
    }
    print("hello")
    print (context)

    # عرض القالب (template) مع البيانات
    return render(request, 'display/displaymydelayoperations.html', context)


