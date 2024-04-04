from django.shortcuts import render , redirect
from urllib.parse import unquote
from .models import Display


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
def submit_operation(request):
    if request.method == 'POST':
        choose_value = request.POST.get('CHOOSE')  # احصل على القيمة المختارة
        display_id = request.POST.get('display_id')  # احصل على معرف العرض
        
        # قم بتحديث العرض المرتبط بالمعرف مع القيمة المختارة
        display = Display.objects.get(pk=display_id)
        display.choosenum = choose_value
        display.save()

    return redirect('display/videoA.html')  # قم بتوجيه المستخدم مرة أخرى إلى صفحة العرض بعد الانتهاء