from django.shortcuts import render,redirect
from .models import *
from django.db.models import Q
from accounts.models import Users,Address
from django.contrib.auth.models import User


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
    try:
     cart = Cart.objects.get(user = user )
     if CartItems.objects.filter(cart = cart,products = Products.objects.get(id = id)).exists():
        return redirect('cart')
    except:
        cart = Cart.objects.create(user = user)
        cart.save()
    cart_item = CartItems.objects.create(cart = cart,products = Products.objects.get(id = id),quantity = 1)
    cart_item.save()
    return redirect('cart')

def remove_cartitem(request,id):
    cartitem = CartItems.objects.get(id = id)
    cartitem.delete()
    return redirect('cart')

def quantity_increment(request,id):
    cartitems = CartItems.objects.get(id = id)
    cartitems.quantity += 1
    cartitems.save()
    return redirect ('cart')

def quantity_decrement(request,id):
    cartitems = CartItems.objects.get(id = id)
    if cartitems.quantity == 1:
        return redirect ('cart')
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
    cart = Cart.objects.get(user = user)
    cartitems = cart.cartitems.all() 
    return render(request, 'cart/checkout.html',{'main_address':main_address,'related_address':related_address,'cart':cart,'cartitems':cartitems,'user_exists':user.username})

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

    