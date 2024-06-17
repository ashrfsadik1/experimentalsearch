from django.shortcuts import render , redirect,reverse
from urllib.parse import unquote,urlparse

from .models import Display,Display_Data,SearchTxt
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Count
from accounts.models import UserProfile
import re


# Create your views here.
class mydata:
    def __init__(self, full_url, title,searchtxt, countArry, Darry):
        self.full_url = full_url
        self.title = title
        self.searchtxt=searchtxt
        self.countArry = countArry
        self.Darry = Darry
        
 


          


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


def get_evaluation_history(url_to_check):
    try:
        # محاولة استرداد سجل بناءً على الرابط المعطى
        display_obj = Display.objects.get(url=url_to_check)
        
        # الحصول على جميع التقييمات المرتبطة بالـ Display المعطى بترتيب زمني تنازلي
        evaluations = Display_Data.objects.filter(displays=display_obj).order_by('-puplish_date')
        
        # إنشاء قائمة من التقييمات بترتيب زمني من الأحدث إلى الأقدم
        evaluation_history = [{'choosenum': eval.choosenum} for eval in evaluations]
        print("hello")
        print (evaluation_history)
            
        return evaluation_history
    except Display.DoesNotExist:
        # إذا لم يتم العثور على الرابط في قاعدة البيانات، نعيد قائمة فارغة
        return []




    
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
def display_video(request, url,searchtxt):
    
    # تشكيل الـ URL الكامل لإطار الفيديو على YouTube
    full_url = f"https://www.youtube.com/embed/{url}"
    embed_url = f"https://www.youtube.com/watch?v={url}" #للاستخلاص من خلال الامر soup
    soup = BeautifulSoup(requests.get(embed_url).content, "html.parser")
    title = soup.title.text
    print("hi")
    print("title")
    # استخدم نموذج "display_data"
    countArry=check_url_exists_and_evluate(full_url)
    Darry=check_url_exists_and_date(full_url)
    #evih=get_evaluation_history(embed_url)
    searchtxt=searchtxt
    data = mydata(full_url, title,searchtxt, countArry, Darry)

# استخدم "Count" لحساب عدد السجلات
        

# طباعة النتيجة

                 

        # مرر الـ embed_url وعنوان الفيديو إلى القالب
    return render(request, 'display/videoA.html', {'data':data})
    #return render(request, 'display/videoA.html', {'embed_url': embed_url , 'title': title,'carry_0': countArry[0], 'carry_1': countArry[1], 'carry_2': countArry[2], 'carry_3': countArry[3], 'carry_4': countArry[4],'d0':Darry[0],'d1':Darry[1],'d2':Darry[2],'d3':Darry[3],'d4':Darry[4]})
    

def display_web(request, url,searchtxt):
    # تشكيل الـ URL الكامل لإطار الفيديو على YouTube
    full_url = unquote(url)

    # استخراج عنوان الموقع من URL
    soup = BeautifulSoup(requests.get(full_url).content, "html.parser")
    title = soup.title.text
    countArry=check_url_exists_and_evluate( full_url)
    Darry=check_url_exists_and_date( full_url)
    print ( full_url)
    print(title)
    
    searchtxt=searchtxt
    data = mydata(full_url, title,searchtxt, countArry, Darry)
    return render(request, 'display/webviewA.html', {'data':data })
def is_youtube_url(url):

    #https://www.youtube.com/embed/CGMCEw5Cfjo
   youtube_regex = r"^https?://(?:www\.)?youtube\.com/(?:embed/|v/|watch\?v=|playlist\?list=)(?P<video_id>[a-zA-Z0-9-_]{11})"
   match = re.search(youtube_regex, url)
    
   return bool(match)





# def makeavalueforurl(request,url,choosenum):
     

def submit_operation(request):
    
    if request.method == 'POST':
        stxt=request.POST.get('searchtxt')
        try :
            searchtxt=SearchTxt.objects.get(text=stxt)
        except:
            searchtxt=SearchTxt(text=stxt)
            searchtxt.save()   
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
    # displaydegree=makeavalueforurl(request,url,choosenum)
        #display=Display.objects.get(url=url,text=text)
    try:
            display = Display.objects.get(searchtxt=searchtxt,url=url, text=text)
            
           
    except :
            display = Display(searchtxt=searchtxt,url=url, text=text,isyoutube=isyoutube)
            display.save()

       # Import the UserProfile model
    user_profile = UserProfile.objects.get(user=request.user)
    

    
    
    
    #print(display.index)
    #searchtxt=SearchTxt.objects.create(text=stxt)

    display_data = Display_Data.objects.create(displays=display,choosenum=choosenum)
    display_data.users.add(user_profile)
    # user=User.objects.get(username=request.user)
    # user_degree=UserDegree.objects.get(user)
    #savedisplaydegreeatbegining(request,display,choosenum)

        
        #display_data.users.add(request.user)  # Add user to Display_Data

        # ... (Redirect user)
    return redirect(request.META.get('HTTP_REFERER'))
def displaymyoperations(request):
    # استرداد بيانات المستخدم الحالي
    current_user = request.user
    
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


