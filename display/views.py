from django.shortcuts import render
from urllib.parse import unquote


# Create your views here.


def display_video(request, url):
    # تشكيل الـ URL الكامل لإطار الفيديو على YouTube
    embed_url = f"https://www.youtube.com/embed/{url}"
    
    # مرر الـ embed_url إلى القالب
    return render(request, 'display/videoA.html', {'embed_url': embed_url})
        
def display_web(request, url):
    # تشكيل الـ URL الكامل لإطار الفيديو على YouTube
    full_url = unquote(url)    
    
    # مرر الـ embed_url إلى القالب
    return render(request, 'display/webviewA.html', {'embed_url': full_url})
