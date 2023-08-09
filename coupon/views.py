from django.shortcuts import render

# Create your views here.
def adminCoupon(request):
    return render(request,'coupon/adminCoupon.html')
