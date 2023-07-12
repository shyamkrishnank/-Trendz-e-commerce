from django.shortcuts import render,redirect
from .models import Admin
from accounts.models import Users
from django.views.decorators.cache import never_cache


# login------------------------>
@never_cache
def login(request):
    if 'admin_username' in request.session:
        return redirect('admin_home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            admin = Admin.objects.get(username = username, password = password)
            if admin:
                request.session['admin_username'] = username
                return redirect('admin_home')
            else:
                message = 'Admin credentials entered are wrong!'
                return render(request,'custo,_admin/login.html',{'message':message})
        except:
            message = 'Admin credentials entered are wrong!'
            return render(request,'custom_admin/login.html',{'message':message})
    return render(request,'custom_admin/login.html')

# dashboard------------------------>
@never_cache
def home(request):
    if 'admin_username' in request.session:
        return render(request,'custom_admin/home.html')
    else:
        return redirect('admin_login')


# users------------------------------------------->
@never_cache
def users(request):
    if 'admin_username' in request.session:
        users = Users.objects.all()
        return render(request,'custom_admin/users.html',{'users':users})

def delete_user(request,id):
    if 'admin_username' in request.session:
        user = Users.objects.get(id = id)
        user.delete()
        return redirect('users')
@never_cache
def user_active(request,id):
    if 'admin_username' in request.session:
        user = Users.objects.get(id = id)
        if user.user.is_active == 1:
            user.user.is_active = 0
            user.user.save()
        
        else:
            user.user.is_active = 1
            user.user.save()
        return redirect('users')
    
def admin_logout(request):
    del request.session['admin_username']
    return redirect('admin_login')


