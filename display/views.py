from django.shortcuts import render , redirect,reverse
from urllib.parse import unquote
from .models import Display,Display_Data
from bs4 import BeautifulSoup
import requests

# Create your views here.

def display_video(request, url):
    # تشكيل الـ URL الكامل لإطار الفيديو على YouTube
    embed_url = f"https://www.youtube.com/embed/{url}"
    full_url = f"https://www.youtube.com/watch?v={url}"
    soup = BeautifulSoup(requests.get(full_url).content, "html.parser")
    title = soup.title.text
    

        # مرر الـ embed_url وعنوان الفيديو إلى القالب
    return render(request, 'display/videoA.html', {'embed_url': embed_url , 'title': title})

def display_web(request, url):
    # تشكيل الـ URL الكامل لإطار الفيديو على YouTube
    full_url = unquote(url)

    # استخراج عنوان الموقع من URL
    soup = BeautifulSoup(requests.get(full_url).content, "html.parser")
    title = soup.title.text
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
        return redirect('searchpage') 