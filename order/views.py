from django.shortcuts import render,redirect
from accounts.models import Users,Address
from .models import Order,OrderDetail
from cart.models import Cart,CartItems
# Create your views here.
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
    user = Users.objects.get(username = request.session['user_exists'])
    return render(request,'order/ordersuccess.html',{'order_id':id})

def orderpage(request):
    user = Users.objects.get(username = request.session['user_exists'])
    order_details = Order.objects.filter(user = user).order_by('-date_created')
    return render(request,'order/orderpage.html', {'order':order_details,'name':'Orders'})

def orderdetails(request,id):
    order = Order.objects.get(id = id)
    return render(request,'order/orderdetail.html',{'order':order})