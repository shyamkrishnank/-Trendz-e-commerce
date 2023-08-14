from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import render,redirect
from accounts.models import *
from coupon.models import Coupon,CouponUser
from .models import Order,OrderDetail,Returned
from cart.models import Cart
from django.utils import timezone
from django.views.decorators.cache import never_cache
from decimal import Decimal
from xhtml2pdf import pisa


def adminOrders(request):
    order = Order.objects.all().order_by('-date_created')
    return render(request,'order/adminorder.html',{'order':order})

@never_cache
def filter(request):
    if request.method == 'POST':
        search = request.POST.get('order_id')
        status = request.POST.get('order_status')
        if status:
            orders = Order.objects.filter(orderitems__order_status = status).distinct()
        else:
            orders = Order.objects.all()
        if search:
            element = orders.filter(order_num = search)
        else:
            element = orders
        return render(request,'order/adminorder.html',{'order':element,'select':status,'place':search})

def adminOrderDetail(request,id):
    order = Order.objects.get(id = id)
    choices = OrderDetail.order_choices
    return render(request,'order/adminorderdetail.html',{'order':order,'choices':choices})

def status_change(request,id):
    if request.method == 'POST':
        status = request.POST.get('orderstatus')
        order = OrderDetail.objects.get(id = id)
        if status == 'Order Delivered':
            order.date_delivered = timezone.now()
        if status == 'Order Returned':
            amount = Decimal(order.total_price)
            wallet = Wallet.objects.get(user = order.order.user)
            wallet.amount += amount
            wallet.save()
            return_ = order.returned.first()
            return_.date_returned = timezone.now()
            return_.save()
        order.order_status = status
        order.save()
        return redirect('adminorderdetails',order.order.id)
    return redirect('adminorderdetails',order.order.id)

def order(request):
    user = Users.objects.get(username = request.session['user_exists'])
    if request.method == 'POST':
        user = user
        address = Address.objects.get(id = request.POST.get('address_radio'))
        order = Order.objects.create(user = user,address = address)
        payment = request.POST.get('payment_method')
        cart = Cart.objects.get(user = user)
        print(payment)
        if payment == 'wallet':
            order.payment_type ='FROM WALLET'
            wallet = Wallet.objects.get(user = user)
            wallet.amount -= Decimal(str(cart.total_price))
            wallet.save()
        elif payment == 'onlinepayment':
            order.payment_type = 'ONLINE PAYMENT'
        else:
            pass
        order.payed_amount = cart.last_price
        order.save()
        cartitems = cart.cartitems.all()
        for items in cartitems:
            OrderDetail.objects.create(order = order,products = items.products,products_price = items.products.price,quantity = items.quantity,varient = items.varient) 
            items.products.save()  
        if 'coupon' in request.session: 
            coupon = Coupon.objects.get(id = request.session['coupon'])
            del request.session['coupon']
            CouponUser.objects.create(coupons = coupon , user = user)   
        cart.delete()   
        return redirect('ordersuccess',order.order_num)   
        
def ordersuccess(request,id):
    user = request.session['user_exists']
    return render(request,'order/ordersuccess.html',{'order_id':id,'user_exists':user})

def orderpage(request):
    user = Users.objects.get(username = request.session['user_exists'])
    order_details = Order.objects.filter(user = user).order_by('-date_created')
    return render(request,'order/orderpage.html', {'order':order_details,'name':'Orders','user_exists':user.username})

def orderdetails(request,id):
    order = Order.objects.get(id = id)
    user_exists = request.session['user_exists']
    return render(request,'order/orderdetail.html',{'order':order,'user_exists':user_exists})

def order_cancel(request,id):
    order = OrderDetail.objects.get(id = id)
    main_id = Order.objects.get(orderitems = order).id
    order.order_status = 'Order Cancelled'
    order.save()
    return redirect('orderdetails',main_id)

def return_reason(request,id):
    order = OrderDetail.objects.get(id = id)
    return render(request,'order/return/returnconf.html',{'order':order})

def return_confirmation(request):
    if request.method == 'POST':
        order = OrderDetail.objects.get(id = request.POST.get('order_id'))
        reason = request.POST.get('reason')
        discription = request.POST.get('details')
        r_obj = Returned.objects.create(order = order,reason = reason,details = discription)
        r_obj.save()
        order.order_status = 'Order Pending'
        order.save()
        r_id = r_obj.return_num
        return render(request,'order/return/returnconfirm.html',{'r_id':r_id})

def report(request):
    orders = OrderDetail.objects.all().order_by('-order__date_created')
    earliest_date = OrderDetail.objects.earliest('order__date_created').order.date_created
    fromdate = earliest_date.strftime('%Y-%m-%d')
    todate = timezone.now().strftime('%Y-%m-%d')
    return render(request,'order/report/report.html',{'orders':orders,'fromdate':fromdate,'todate':todate})

def report_filter(request):
    date_format = '%Y-%m-%d'
    fromdate = request.POST.get('fromDate')
    todate = request.POST.get('toDate')
    todated = datetime.strptime(todate, date_format) + timedelta(days=1)
    orders = OrderDetail.objects.filter(order__date_created__range=(fromdate,todated)).order_by('-order__date_created')
    return render(request,'order/report/report.html',{'orders':orders,'fromdate':fromdate,'todate':todate})

def report_download(request):
    date_format = '%Y-%m-%d'
    fromdate = request.POST.get('fromDate')
    todate = request.POST.get('toDate')
    todated = datetime.strptime(todate, date_format) + timedelta(days=1)
    orders = OrderDetail.objects.filter(order__date_created__range=(fromdate,todated)).order_by('order__date_created')
    template = 'order/report/reportPDF.html'
    context = {'data': orders,'fromdate':fromdate,'todate':todate}  # Replace with your actual context data
    html_string = render(request, template, context).content

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Report.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF generation error')

    return response
    # return render(request,'order/report/reportPDF.html',{'data':orders,'fromdate':fromdate,'todate':todate})

def invoice(request,id):
    order = Order.objects.get(id = id)
    context = {'order':order}
    template = 'order/invoice/invoice.html'
    html_string = render(request, template,context).content
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF generation error')
    return response

    return render(request,'order/invoice/invoice.html')

        

   
    

