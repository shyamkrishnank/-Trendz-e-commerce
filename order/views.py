from django.shortcuts import render,redirect
from accounts.models import Users,Address
from .models import Order,OrderDetail
from cart.models import Cart,CartItems

def adminOrders(request):
    order = Order.objects.all()
    return render(request,'order/adminorder.html',{'order':order})

def adminOrderDetail(request,id):
    order = Order.objects.get(id = id)
    choices = OrderDetail.order_choices
    return render(request,'order/adminorderdetail.html',{'order':order,'choices':choices})

def status_change(request,id):
    if request.method == 'POST':
        status = request.POST.get('orderstatus')
        order = OrderDetail.objects.get(id = id)
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
        order.save()
        cart = Cart.objects.get(user = user)
        cartitems = cart.cartitems.all()
        for items in cartitems:
            OrderDetail.objects.create(order = order,products= items.products,quantity = items.quantity) 
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
    
