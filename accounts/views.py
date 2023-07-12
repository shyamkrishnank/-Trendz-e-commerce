from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from . models import Users
import random
from twilio.rest import Client
from django.contrib.auth.models import User
from category.models import Category
from products.models import Products,ProductImage

# Create your views here.

def home(request):
    category = Category.objects.all()
    if 'user_exists' in request.session:
        user_exists = request.session['user_exists']
        return render(request,'accounts/home.html',{'category':category,'user_exists':user_exists})
    return render(request,'accounts/home.html',{'category':category})



def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
    else:
        message = 'Invalid email or password!'
        return render(request, 'accounts/login.html', {'message': message})
except Users.DoesNotExist:
    message = 'Invalid email or password!'
    return render(request, 'accounts/login.html', {'message': message})
return render(request, 'accounts/login.html')



def send_otp(otp):
     account_sid = 'AC5c34d6f5c796b304a27df7f621117763'
     auth_token = '26544a6f6b0e97fd8e4361ac5fe65f76'
     client = Client(account_sid, auth_token)

     message = client.messages.create(
        body='Your otp is '+otp,
        from_='+18145266799',
        to='+917994420545'
     )
     print(message.sid)

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        user = Users.objects.filter(email = email).exists()
        if user:
            message = 'Email already exits!'
            return render(request,'accounts/signup.html',{'message':message})
        user = Users.objects.filter(phone = phone)
        if user:
            message = 'Phone number already exits!'
            return render(request,'accounts/signup.html',{'message':message})
        if password == cpassword:
            otp = str(random.randint(1000, 9999))
            # send_otp(otp)
            print("-----------------------")
            print(otp)
            print("-----------------------")
            request.session['user_details']={
                'username':username,
                 'email': email,
                 'phone': phone,
                 'password':password,
                 'otp':otp
            }
            return redirect('otp_validate')
        else:
            message = 'Enter correct password!'
            return render(request,'accounts/signup.html',{'message':message})
           
    return render(request,'accounts/signup.html')

def otp_validate(request):
    if request.method == 'POST':
        enter_otp = request.POST.get('otp')
        user_detail = request.session['user_details']
        if user_detail['otp'] == enter_otp:
             in_user = User.objects.create_user(username = user_detail['username'],password = user_detail['password'])
             user = Users.objects.create(user=in_user,username = user_detail['username'],email = user_detail['email'],phone = user_detail['phone'])
             request.session.flush()
             return redirect('user_login') 
        else:
            message = 'Wrong OTP entered!'
            return render(request,'accounts/otp.html',{'message':message})
    return render(request,'accounts/otp.html')

def products(request,id):
    category = Category.objects.all()
    products = Products.objects.filter(category = Category.objects.get(id = id))
    count = products.count()
    return render(request,'accounts/products.html',{'products':products,'count':count,'category':category})

def product_detail(request,id):
    main_product = Products.objects.get(id = id)
    related_products = Products.objects.exclude(id = id )
    return render(request,'accounts/product_details.html',{'main_product':main_product,'related_products':related_products})

def logout(request):
    del request.session['user_exists']
    return redirect('user_login')

    
