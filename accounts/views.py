from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from . models import Users,Address
import random
from django.db.models import Q
from twilio.rest import Client
from django.contrib.auth.models import User
from category.models import Category
from products.models import Products,ProductImage
from order.models import OrderDetail

# Create your views here.
# -----------------------------------------------------home----------
def home(request):
    category = Category.objects.all()
    return render(request,'accounts/home.html',{'category':category})

# ---------------------------------------------------------signup/login------

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        try:
            user = Users.objects.get(email=email)
            if not  user.user.is_active:
                 message = 'User Blocked!'
                 return render(request, 'accounts/login.html', {'message': message})
            temp_user = authenticate(request, username=user.username, password=pass1)
            if temp_user:
                user_exists = user.username
                request.session['user_exists'] = user_exists
                return redirect('home')
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
            message = 'otp did not match!'
            return render(request,'accounts/signup.html',{'message':message})
           
    return render(request,'accounts/signup.html')

def logout(request):
    del request.session['user_exists']
    return redirect('user_login')


def otp_validate(request):
    if request.method == 'POST':
        enter_otp = request.POST.get('otp')
        user_detail = request.session['user_details']
        if user_detail['otp'] == enter_otp:
             in_user = User.objects.create_user(username = user_detail['username'],password = user_detail['password'])
             user = Users.objects.create(user=in_user,username = user_detail['username'],email = user_detail['email'],phone = user_detail['phone'])
             user.save()
             request.session.flush()
             return redirect('user_login') 
        else:
            message = 'Wrong OTP entered!'
            return render(request,'accounts/otp.html',{'message':message})
    return render(request,'accounts/otp.html')

# ----------------------------------------------------products/products details--------------

def shop(request):
    products = Products.objects.all()
    

def products(request,id):
    category = Category.objects.all()
    products = Products.objects.filter(category = Category.objects.get(id = id))
    count = products.count()
    return render(request,'accounts/products.html',{'products':products,'count':count,'category':category})

def product_detail(request,id):
    category = Category.objects.all()
    main_product = Products.objects.get(id = id)
    related_products = Products.objects.exclude(id = id )
    return render(request,'accounts/product_details.html',{'main_product':main_product,'related_products':related_products,'category':category})

# ------------------------------------------------------userprofile --------------------

def user_profile(request):
    user = Users.objects.get(username = request.session.get('user_exists'))
    if request.method == 'POST':
        user.username = request.POST.get('name')
        request.session['user_exists'] = user.username
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.user.username = request.POST.get('name')
        user.user.save()
        user.save()
        return redirect('user_profile')
    return render(request,'accounts/profile/accountdetails.html',{'user':user,'name':'Account'})

def change_password(request):
        user_exists = None
        if 'user_exists' in request.session:
            user_exists = request.session['user_exists']
        otp = str(random.randint(1000,9999))
        # send_otp(otp)
        request.session['otp'] = otp
        print("---------------------------------------")
        print(otp)
        print("---------------------------------------")
        return render(request,'accounts/passotp.html')

def otp_validater(request):
        if request.method == 'POST':
            entered_otp = request.POST.get('otp')
            if entered_otp == request.session['otp']:
                return redirect('passwordsetter')
            return render(request,'accounts/passotp.html',{'message':'OTP doesnot match!'})
            
def passwordsetter(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['cpassword']:
             user = User.objects.get(username = request.session['user_exists'])
             user.set_password(request.POST.get('password'))
             user.save()
             return redirect('user_profile')
        return render(request,'accounts/changepassword.html',{'message':'Enter the correct password!'})
    return render(request,'accounts/changepassword.html')

def address(request):
    main_address = None
    related_address = None
    user = Users.objects.get(username = request.session.get('user_exists'))
    try:
        related_address = Address.objects.filter(Q(user = user) & Q(current = False) & Q(active = True)).first() 
        try:
            main_address = Address.objects.get(Q(user = user) & Q(current = True) )   
        except:
           pass
    except:
            pass
    return render(request,'accounts/profile/address.html',{'user_exists':user.username,'main_address':main_address,'related_address':related_address,'name':'Address'})

def add_address(request,check):
    if 'user_exists' in request.session:
        user_exists = request.session['user_exists']
    if request.method == 'POST':
        user = User.objects.get(username = request.session['user_exists'])
        name = request.POST.get('name')
        address = request.POST.get('address')
        state = request.POST.get('state') 
        city = request.POST.get('city')
        country = request.POST.get('country')
        postalcode = request.POST.get('postalcode')
        checkbox = request.POST.get('checkbox')
        if checkbox == 'on':
            current = True
            try:
                related_address = Address.objects.get(Q(user = user) & Q(current = 'True') & Q(active = True) )
                related_address.current = False
                related_address.save()
            except:
                pass
        else:
            current = False
        add = Address.objects.create(user = user.c_user,fullname = name, address1 = address,state = state, city = city,country = country, postalcode = postalcode,current = current )
        add.save()
        return redirect('address')
    if check==1:
        return render(request, 'accounts/addaddress.html',{'check':'checked','user_exists':user_exists})
    return render(request, 'accounts/addaddress.html',{'check':'0','user_exists':user_exists})

def edit_address(request,id):
    user_exists = None
    if 'user_exists' in request.session:
        user_exists = request.session['user_exists']
    edit = Address.objects.get(id = id)
    if request.method == 'POST':
        edit.fullname = request.POST.get('name')
        edit.address1 = request.POST.get('address')
        edit.state = request.POST.get('state') 
        edit.city = request.POST.get('city')
        edit.country = request.POST.get('country')
        edit.postalcode = request.POST.get('postalcode')
        edit.save()
        return redirect('address')
    return render(request,'accounts/editaddress.html',{'address':edit,'user_exists':user_exists})

def delete_address(request,id):
    edit = Address.objects.get(id = id)
    if edit.current == True:
        edit.current = False
    edit.active = False
    edit.save()
    return redirect('address')



    