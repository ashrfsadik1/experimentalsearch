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
from .models import  UserProfile

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
            messages.error(request,'اسم المستحدم او كلمة السر خاطئة')    
            
       
        return redirect('signin')
    else:
        return render(request,'accounts/signin.html')

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request) 
    return redirect('index')
        
        
    
def signup(request):
    if request.method =='POST' and 'btnsignup' in request.POST:
         #variables for fiwld
        userphoto=None
        usershopphoto=None 
        fname=None
        lname=None
        region=None
        neighborhood=None
        shopname=None
        shopaddress=None
        zip_number=None
        email=None
        username=None
        password=None
        terms=None
        is_added=None
        form = UserProfile(request.FILES, request.POST)  
#get vlues from form
        if 'userphoto'in request.FILES:userphoto=request.FILES['userphoto']
        else: messages.error(request,'انت لم تدخل صورتك')
        if 'usershopphoto'in request.FILES:userphoto=request.FILES['usershopphoto']
        else: messages.error(request,'انت لم تدخل صوره محلك')
        if 'fname' in request.POST: fname =request.POST['fname']
        else: messages.error(request,'انت لم تدخل الاسم الاول')
        
        if 'lname' in request.POST:lname=request.POST['lname']
        else: messages.error(request,'انت لم تدخل الاسم الاخير')
        if 'region' in request.POST:region=request.POST['region'] 
        else: messages.error(request,'انت لم تدخل المنطقة')
        if 'neighborhood' in request.POST:neighborhood=request.POST['neighborhood']
        else: messages.error(request,'انت لم تدخل الحى')
        if 'shopname' in request.POST:shopname=request.POST['shopname']
        else: messages.error(request,'انت لم تدخل اسم المحل')
        if 'shopaddress' in request.POST:shopaddress=request.POST['shopaddress']
        else: messages.error(request,'انت لم تدخل عنوان المحل ')
        if 'zip' in request.POST:zip_number=request.POST['zip']
        else: messages.error(request,'خطاء فى الرقم البريدى')
        if 'email' in request.POST:email=request.POST['email']
        else: messages.error(request,'خطاء فى الايميل')
       # if 'user' in request.POST:username=request.POST['user']
       #else: messages.error(request,'خطاء فى اسم المستخدم')
        if 'pass' in request.POST:password=request.POST['pass']
        else: messages.error(request,'خطاء فى كلمة السر')
        if 'terms' in request.POST:terms=request.POST['terms']
        #check the values
        if  fname and lname and region and neighborhood and shopname and shopaddress and zip_number and email and password:
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
                            user=User.objects.create_user (first_name=fname,last_name=lname,email=email,username=fname +'_'+shopname,password=password)
                            user.save()
                            #add user profile
                            userprofile=UserProfile(user=user,userphoto=userphoto,usershopphoto=usershopphoto,region=region,neighborhood=neighborhood,shopname=shopname,shopaddress=shopaddress,zip_number=zip_number)
                            userprofile.save()
                            #clear fields
                            userphoto=None
                            usershopphoto=None
                            fname=''
                            lname=''
                            region=''
                            neighborhood=''
                            shopname=''
                            shopaddress=''
                            zip_number=''
                            email=''
                            username=''
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
            'usershopphoto':usershopphoto,
            'fname':fname,
            'lname':lname,
            'region':region,
            'neighborhood':neighborhood,
            'shopname':shopname,
            'shopaddress':shopaddress,
            'zip':zip_number,
            'email':email,
            'user':fname+'_'+shopname,
            'pass':password,       
            'is_added':is_added,           })
    else:
        return render (request,'accounts/signup.html')
    
def profile(request):
    if request.method =='POST'and 'btnsave' in request.POST:
        if request.user is not None and request.user.id!=None:
            userprofile=UserProfile.objects.get(user=request.user)
            if request.POST['fname'] and request.POST['lname'] and request.POST['region'] and request.POST['neighborhood'] and request.POST['shopname'] and request.POST['shopaddress'] and request.POST['zip'] and request.POST['email'] and request.POST['user'] and request.POST['pass'] :
                
                request.user.first_name=request.POST['fname']
                request.user.last_name=request.POST['lname']
                form = UserProfile(request.FILES, request.POST)  
                userprofile.userphoto=request.FILES['userphoto']
                userprofile.usershopphoto=request.FILES['usershopphoto']
                userprofile.region=request.POST['region']
                userprofile.neighborhood=request.POST['neighborhood']
                userprofile.shopname=request.POST['shopname']
                userprofile.shopaddress=request.POST['shopaddress']
                userprofile.zip_number=request.POST['zip']
                #request.user.email=request.POST['email']
                #request.user.username=request.POST['user']
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
                    'usershopphoto':userprofile.usershopphoto,
                    'region':userprofile.region,
                    'neighborhood':userprofile.neighborhood,
                    'shopname':userprofile.shopname,
                    'shopaddress':userprofile.shopaddress,
                    'zip':userprofile.zip_number,
                    
                    
                    'email':request.user.email,
                    'user':request.user.username,
                    'pass':request.user.password
                    
                    
                } 
            return render (request,'accounts/profile.html',context)
        else:
            return redirect('profile')
        
def product_favorite(request,pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        pro_fav=Product.objects.get(pk=pro_id)
        if UserProfile.objects.filter(user=request.user,product_favorites=pro_fav).exists():
            messages.success(request,'هذا المنتج موجود من قبل فى المفضلة')    
        else:
            userprofile=UserProfile.objects.get(user=request.user)
            userprofile.product_favorites.add(pro_fav)
            messages.success(request,'تم اضافة المنتج الى المفضلة')  
                  
        
    else:
        messages.error(request,'لابد من تسجيل الدخول')
    return redirect('/products/' + str(pro_id))      
                    
def show_product_favorite(request):
    context=None
    if request.user.is_authenticated and not request.user.is_anonymous:
        userInfo=UserProfile.objects.get(user=request.user)
        pro = userInfo.product_favorites.all()
        context={'products':pro}
    return render(request,'products/products.html',context )   
def show_comments(request,pro_id):
    usercomments=UserComments.objects.get(productcommented=pro_id)
    comments=usercomments.objects.all()
    if comments!=None:
        context={'comment':comments}
        return render(request,'products/showcomments.html',context)
       
                     
                  
def add_comments(request):
    
    if request.POST and  request.user.is_authenticated and not request.user.is_anonymous: 
         
         if 'btnsend' in request.POST :
            usercomments=UserComments.objects.get(user=request.user)
            pro=request.get['pro_id']
            ratio=request.GET['rating']
            comment=request.GET['comment']
            usercomment=UserComments.objects.create(user=usercomments,productcommented=pro,productratio=ratio,comment=comment)
            usercomment.save()
            context={'products':pro}
            messages.success(request,'تم اضافة التعليق بنحاح')
            return render(request,'products/addcomments.html',context)
         else:
                messages.alert(request,'لم يتم الحفظ')
    else:            
        return render(request,'products/addcoments.html')    
       
       
        
        
                
            