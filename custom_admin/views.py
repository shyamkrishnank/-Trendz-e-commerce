from django.shortcuts import render,redirect
from .models import Admin
from accounts.models import Users
from django.views.decorators.cache import never_cache
from order.models import Order
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, F


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
        order = Order.objects.all()
        total_price = sum(i.total_price for i in order)
        current_date = timezone.now().date()
        this_day = order.filter(date_created__date = current_date)
        this_day_price = sum(i.total_price for i in this_day)
        start_date_current_week = current_date - timedelta(days=current_date.weekday())
        end_date_current_week = start_date_current_week + timedelta(days=6)
        this_week = order.filter(date_created__range=[start_date_current_week, end_date_current_week])
        this_week_price = sum(i.total_price for i in this_week)
        current_year = timezone.now().year
        this_year = order.filter(date_created__year = current_year)
        this_year_price = sum(i.total_price for i in this_year)
        report = {
            'thisDay':this_day,
            'thisYear':this_year,
            'thisWeek':this_week,
            'dayPrice':this_day_price,
            'weekPrice':this_week_price,
            'yearPrice':this_year_price,
            'order':order,
            'totalPrice':total_price
        }
        return render(request,'custom_admin/home.html',{'report':report})
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


