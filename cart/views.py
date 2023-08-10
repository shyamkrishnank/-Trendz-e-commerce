from django.shortcuts import render,redirect
from .models import *
from django.db.models import Q
from accounts.models import *
from django.contrib.auth.models import User
import razorpay
from django.conf import settings
from products.models import Varient
from coupon.models import Coupon
from django.http import JsonResponse


# Create your views here.

def cart(request):
    user = Users.objects.get(username = request.session['user_exists'])
    try:
        user_cart = Cart.objects.get(user = user)
        cart1 = user_cart.cartitems.all()
        if 'cartid' not in request.session:
            request.session['cartid'] = user_cart.id
        total = 0
    except:
         user_cart = None
         cart1 = None 
    return render(request,'cart/cart.html',{'cart':cart1,'main_cart':user_cart,'user_exists':user.username,})



def add_cart(request,id):
    user = Users.objects.get(username = request.session['user_exists'] )
    product = Products.objects.get(id = id)
    try:
        cart = Cart.objects.get(user = user )
        if CartItems.objects.filter(cart = cart,products = product).exists():
            id = product.category.id
            return redirect('products',id)
    except:
        cart = Cart.objects.create(user = user)
        cart.save()
    if product.stocks > 0:
        product.stocks -= 1
        product.save()
        varient = product.varient.first()
        print(varient.varient)
        cart_item = CartItems.objects.create(cart = cart,products = product,quantity = 1,varient = varient.varient)
        cart_item.save()
        id = product.category.id
        return redirect('products',id)
    id = product.category.id
    return redirect('products',id)

def add_cart1(request,id):
    if request.method =='POST':
        varient =  request.POST.get('varient')
    user = Users.objects.get(username = request.session['user_exists'] )
    product = Products.objects.get(id = id)
    try:
        cart = Cart.objects.get(user = user )
        if CartItems.objects.filter(cart = cart,products = product).exists():
            return redirect('product_detail',id)
    except:
        cart = Cart.objects.create(user = user)
        cart.save()
    if product.stocks > 0:
        product.stocks -=1
        product.save()
        cart_item = CartItems.objects.create(cart = cart,products = product,quantity = 1,varient = varient )
        cart_item.save()
        return redirect('product_detail', id)
    return redirect('product_detail', id)

def remove_cartitem(request,id):
    cartitem = CartItems.objects.get(id = id)
    cartitem.products.stocks += 1
    cartitem.products.save()
    cartitem.delete()
    return redirect('cart')

def quantity_increment(request,id):
    cartitems = CartItems.objects.get(id = id)
    if cartitems.products.stocks <=1:
        return JsonResponse('Out of Stock',status = 400,safe=False )
    if cartitems.quantity == 6:
        return redirect('cart')
    cartitems.products.stocks -= 1
    cartitems.products.save()
    cartitems.quantity += 1
    cartitems.save()
    return redirect ('cart')

def quantity_decrement(request,id):
    cartitems = CartItems.objects.get(id = id)
    if cartitems.quantity == 1:
        return redirect ('cart')
    cartitems.products.stocks += 1
    cartitems.products.save()
    cartitems.quantity -= 1
    cartitems.save()
    return redirect ('cart')

def checkout(request):
    user = Users.objects.get(username = request.session['user_exists'])
    try:
        related_address = Address.objects.filter(Q(user = user) & Q(current = False) & Q(active = True))
        try:
            main_address = Address.objects.get(Q(user = user) & Q(current = True) )   
        except:
           main_address = None
    except:
        related_address - None
    wallet_amount = Wallet.objects.get(user = user).amount
    cart = Cart.objects.get(user = user)

    if cart.last_price == 0:
         cart.last_price = cart.total_price

    client = razorpay.Client(auth=(settings.RAZOR_KEY, settings.KEY_SECRET))
    payment = client.order.create({'amount':float(cart.last_price*100),'currency':'INR', 'payment_capture':1})
    coupons = Coupon.objects.filter(min_rate__lte=cart.total_price , max_rate__gte=cart.total_price,is_active = True)
    cartitems = cart.cartitems.all() 
    return render(request, 'cart/checkout.html',{'main_address':main_address,'wallet':wallet_amount,'related_address':related_address,'coupons':coupons,'cart':cart,'cartitems':cartitems,'payment':payment})
def add_checkout_address(request):
    user_exists = None
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
        return redirect('checkout')
    return render(request,'cart/add_address.html',{'user_exists':user_exists})




    