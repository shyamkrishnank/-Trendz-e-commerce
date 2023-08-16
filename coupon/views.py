from django.utils import timezone
from decimal import Decimal
from django.shortcuts import render,redirect
from .models import Coupon
from django.contrib import messages
from cart.models import Cart
from accounts.models import Users
# Create your views here.
def applyCoupon(request,id):
    if request.method == 'POST':
        if 'message' in request.session:
            del request.session['message']
        coupon_code = request.POST.get('coupon')
        try: 
            cart = Cart.objects.get(id = id)
            coupon = Coupon.objects.get(coupon_code = coupon_code,min_rate__lte=cart.total_price , max_rate__gte=cart.total_price,is_active = True)
            if coupon.couponuser.filter(user = Users.objects.get(username = request.session['user_exists'])).exists():
               request.session['message'] = 'You have already used this coupon!'
               cart.is_coupon = False
               cart.save()
               return redirect('checkout')
            else:
                
                discount_percentage = Decimal(coupon.discount) / 100
                discount_amount = cart.total_price * discount_percentage
                new_last_price = float(cart.total_price - discount_amount)
                cart.last_price = Decimal(new_last_price)
                cart.is_coupon = True
                request.session['coupon'] = coupon.id
                cart.save()      
        except:
            cart.is_coupon = False
            cart.save()
            request.session['message'] = 'Invalid Coupon Code!'
        return redirect('checkout')

def adminCoupon(request):
    coupons = Coupon.objects.all()
    return render(request,'coupon/adminCoupon.html',{'coupons':coupons})

def addCoupon(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        discount = request.POST.get('discount')
        min = request.POST.get('min')
        max = request.POST.get('max')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')
        coupon = Coupon.objects.create(name = name, coupon_code = code, discount = discount, start_date = start_date,end_date = end_date, min_rate = min, max_rate = max)
        coupon.save()
        return redirect('adminCoupon')

def couponStatus(request,id):
    coupon = Coupon.objects.get(id = id)
    if coupon.is_active:
        coupon.is_active = False
        coupon.save()
    else:
        def is_today_between(start_date, end_date):
            today = timezone.now().date()
            return start_date <= today <= end_date
          
        if is_today_between(coupon.start_date,coupon.end_date):
              coupon.is_active = True
              coupon.save()
        else:
            messages.warning(request, 'You can only activate an offer when the offer within start and end date')

    return redirect('adminCoupon')

def editCoupon(request,id):
    coupon = Coupon.objects.get(id = id)
    coupon.name = request.POST.get('name')
    coupon.coupon_code = request.POST.get('code')
    coupon.discount = request.POST.get('discount')
    coupon.min_rate  = request.POST.get('min')
    coupon.max_rate  = request.POST.get('max')
    coupon.start_date = request.POST.get('startDate')
    coupon.end_date = request.POST.get('endDate')
    coupon.save()
    return redirect('adminCoupon')



    



