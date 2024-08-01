from django.shortcuts import render, redirect
from SearchEngine.search import google
from django.contrib.auth.models import User
from display.models import Display,Display_Data
from django.contrib import messages
from SearchEngine.search import google,yahoo,duck,ecosia, bing, givewater

def homepage(request):
    user_count=User.objects.count()
    sites_count=Display.objects.count()
    sucuss_count=Display_Data.objects.filter(choosenum=1).count()
    
    failed_count=Display_Data.objects.filter(choosenum=2).count()
    needtomoney_count=Display_Data.objects.filter(choosenum=3).count()
    needtotools_count=Display_Data.objects.filter(choosenum=4).count()
    delayed_count=Display_Data.objects.filter(choosenum=5).count()
    context={
        "user_count":user_count,
        "sites_count":sites_count,
        "sucuss_count":sucuss_count,
        "failed_count":failed_count,
        "needtomoney_count":needtomoney_count,
        "needtotools_count":needtotools_count,
        "delayed_count":delayed_count,


    }
    return render(request,'index.html',{'context':context})

def searchpage(request):
    if not request.user.is_authenticated:
        messages.error(request,"يجب عليك ان تسجل الدخول قبل البحث")
        return render(request,"index.html")

    else:    
        return render(request,'home.html')
def results(request):
    if request.method == "POST":
        result = request.POST.get('search')
        google_link,google_text,google_image= google(result)
        google_data = zip(google_link,google_text,google_image )
        yahoo_link,yahoo_text = yahoo(result)
        yahoo_data = zip(yahoo_link,yahoo_text)
        duck_link,duck_text,duck_image  = duck(result)
        duck_data = zip(duck_link,duck_text,duck_image)
        ecosia_link,ecosia_text = ecosia(result)
        ecosia_data = zip(ecosia_link,ecosia_text)
        bing_link,bing_text = bing(result)
        bing_data = zip(bing_link,bing_text)
        givewater_link,givewater_text = givewater(result)
        givewater_data = zip(givewater_link,givewater_text)




        if result == '':
            return redirect('Home')
        else:
            
            
            #return render(request,'results.html',{'google': google_data})
            return render(request,'results.html',{'google': google_data, 'yahoo': yahoo_data, 'duck': duck_data, 'ecosia': ecosia_data,'bing': bing_data, 'givewater': givewater_data})
