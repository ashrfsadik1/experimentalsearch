from django.shortcuts import render

# Create your views here.
from http.client import responses
from urllib import request
from urllib.request import Request
#from urllib import request
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from .models import  UserProfile,UserUrl

from django.forms import modelformset_factory
import re

# Create your views here.

def signin(request):
    if request.method =='POST' and 'btnlogin' in request.POST:
        username=request.POST['user']
        password=request.POST['pass']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            if 'rememberme' not in request.POST:
                request.session.set_expiry(0) 
                
            auth.login(request,user) 
           #messages.success(request,'You are now logged in')
        else:
            messages.error(request,'Username or Password invalid')    
            
       
        return redirect('signin')
    else:
        return render(request,'accounts/signin.html')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request) 
    return redirect('Home')
        
        
    
def signup(request):
    if request.method =='POST' and 'btnsignup' in request.POST:
         #variables for fiwld
        userphoto=None
        
        fname=None
        lname=None
        email=None
        username=None
        nikename=None
        url=None
        password=None
        terms=None
        is_added=None
        form = UserProfile(request.FILES, request.POST)  
#get vlues from form
        if 'userphoto'in request.FILES:userphoto=request.FILES['userphoto']
        else: messages.error(request,'انت لم تدخل صورتك')
        if 'fname' in request.POST: fname =request.POST['fname']
        else: messages.error(request,'انت لم تدخل الاسم الاول')
        
        if 'lname' in request.POST:lname=request.POST['lname']
        else: messages.error(request,'انت لم تدخل الاسم الاخير')
        if 'email' in request.POST:email=request.POST['email']
        else: messages.error(request,'خطاء فى الايميل')
        if 'user' in request.POST:username=request.POST['user']
        else: messages.error(request,'خطاء فى اسم المستخدم')
        if 'nikename' in request.POST:nikename=request.POST['nikename']
        else: messages.error(request,'خطاء فى الاسم المستعار')
        if 'url'in request.POST:url=request.POST['url']
        if 'pass' in request.POST:password=request.POST['pass']
        else: messages.error(request,'خطاء فى كلمة السر')
        if 'terms' in request.POST:terms=request.POST['terms']
        #check the values
        if  fname and lname and nikename  and  email and password:
            if terms=='on':
                #check if username is taken
                if User.objects.filter(username=username).exists():
                     messages.error(request,'اسم المستخدم موجود من قبل')
                else:
                    #check if email is taken
                    if User.objects.filter(email=email).exists():
                        messages.error(request,'البريد الالكترونى مستخدم من قبل')    
                    else :
                        patt="^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"  
                        if re.match(patt,email):
                            #add user
                            user=User.objects.create_user (first_name=fname,last_name=lname,email=email,username=username,password=password)
                            user.save()
                            #add user profile
                            userprofile=UserProfile(user=user,userphoto=userphoto,user_nickname=nikename)
                            userprofile.save()
                            if url is not None :
                                userurl=UserUrl(user=user,url=url)
                                userurl.save()

                                

                            #clear fields
                            userphoto=None
                            
                            fname=''
                            lname=''
                            email=''
                            username=''
                            nikename=''
                            url=''
                            password=''
                            terms=None
                            
                            #success messages
                            messages.success(request,'تم انشاء حسابك')
                            is_added=True
                            
                        else:
                            messages.error(request,'الايميل غير صحيح')
            else:
                messages.error(request,'لابد ان توافق على شروط الاستخدام')
        else:
            messages.error(request,'تأكد من الحقول الفارغة')
        
        return render(request,'accounts/signup.html',{
            'userphoto':userphoto,
            'fname':fname,
            'lname':lname,
            'email':email,
            'user':username,
            'pass':password,       
            'is_added':is_added,           })
    else:
        return render (request,'accounts/signup.html')
    
def profile(request):
    if request.method =='POST'and 'btnsave' in request.POST:
        if request.user is not None and request.user.id!=None:
            userprofile=UserProfile.objects.get(user=request.user)
            if request.POST['fname'] and request.POST['lname'] and request.POST['email'] and request.POST['user'] and request.POST['pass'] :
                
                request.user.first_name=request.POST['fname']
                request.user.last_name=request.POST['lname']
                form = UserProfile(request.FILES, request.POST)  
                userprofile.userphoto=request.FILES['userphoto']
                if not request.POST['pass'].startswith('pbkdf2_sha256$'):
                    request.user.set_password(request.POST['pass'])
                request.user.save() 
                userprofile.save() 
                auth.login(request,request.user)
                messages.success(request,'تم حفظ بياناتك')
                             
                
            else:
                messages.error(request,'Chek your Values and Elements') 
                
             
        return redirect ('profile')
             
        
    else:
        #if request.user.is_anonymous: return redirect('index')
        
        if request.user is not None:
            context=None
            if not request.user.is_anonymous:
                userprofile=UserProfile.objects.get(user=request.user)
                
                
                context={
                    'fname':request.user.first_name,
                    'lname':request.user.last_name,
                    'userphoto':userprofile.userphoto,
                    'email':request.user.email,
                    'user':request.user.username,
                    'pass':request.user.password
                    
                    
                } 
            return render (request,'accounts/profile.html',context)
        else:
            return redirect('profile')
        
                    
                  
