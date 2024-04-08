from django.shortcuts import render , redirect
from urllib.parse import unquote
from .models import Display,Display_Data
from bs4 import BeautifulSoup
import requests

# Create your views here.

def display_video(request, url):
    # تشكيل الـ URL الكامل لإطار الفيديو على YouTube
    embed_url = f"https://www.youtube.com/embed/{url}"

    # استخراج عنوان الفيديو من URL
    try:
        with YoutubeDL({'verbose': True}) as ydl:
            meta = ydl.extract_info(url, download=False)
            title = meta.get('title')
            print ('hello')
            print(title)
            print('hello')
    except YoutubeDLException as e:
        # Handle the exception, you can display a user-friendly message
        return render(request, 'display/videoA.html', {'error': str(e)})
       

    # مرر الـ embed_url وعنوان الفيديو إلى القالب
    return render(request, 'display/videoA.html', {'embed_url': embed_url, 'title': title})
def display_web(request, url):
    # تشكيل الـ URL الكامل لإطار الفيديو على YouTube
    full_url = unquote(url)

    # استخراج عنوان الموقع من URL
    soup = BeautifulSoup(requests.get(full_url).content, "html.parser")
    title = soup.title.text
    print("hello")
    print (title)
    print ('hello')

    # مرر الـ embed_url وعنوان الموقع إلى القالب
    return render(request, 'display/webviewA.html', {'embed_url': full_url, 'title': title})

def submit_operation(request):
 if request.method == 'POST':
        url = request.POST.get('url')
        text = request.POST.get('title')
        choosenum = request.POST.get('CHOOSE')

        display = Display.objects.create(url=url, text=text)

        display_data = Display_Data.objects.create(choosenum=choosenum)
        display_data.displays.add(display)
        display_data.user.add(request.user)
        return redirect('display/webviewA.html')  # قم بتوجيه المستخدم مرة أخرى إلى صفحة العرض بعد الانتهاء