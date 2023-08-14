from django.shortcuts import render,redirect
from accounts.models import *
from .models import *
from category.models import *
from django.contrib import messages
from django.utils import timezone
# Create your views here.

def adminOffer(request):
    category = Category.objects.all()
    try:
        offer = Offer.objects.all()
    except:
        offer = None
    return render(request,'offer/offer.html',{'category':category,'offer':offer})

def addOffer(request):
    if request.method == 'POST':
        offer_id = request.POST.get('offerid')
        if offer_id:
            offer = Offer.objects.get(offer_num = offer_id)
            offer.name = request.POST.get('name')
            offer.discount = request.POST.get('discount')
            offer.start_date = request.POST.get('start_date')
            offer.end_date = request.POST.get('end_date')
            offer.discription = request.POST.get('description')
            offer.save()
            cat = request.POST.getlist('catRelate')
            offer.categoryEligible.all().delete()
            for i in cat:
               offer_cat = OfferCategory.objects.create(offer = offer,category = Category.objects.get(id = i))
               offer_cat.save()
            return redirect('adminoffer')
        else:
            name = request.POST.get('name')
            cat = request.POST.getlist('catRelate')
            discount = request.POST.get('discount')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            discription = request.POST.get('discription')
            offer = Offer.objects.create(name = name,discount = discount, start_date = start_date,end_date = end_date,discription = discription)
            offer.save()
            print(cat)
            for i in cat:
                offer_cat = OfferCategory.objects.create(offer = offer,category = Category.objects.get(id = i))
                offer_cat.save()
            return redirect('adminoffer')
               
def offerStatus(request,id):
    offer = Offer.objects.get(id = id)
    if offer.is_active:
        offer.is_active = 0
        offer.save()
        category = offer.categoryEligible.all()
        for i in category:
            products = i.category.products.all()
            for j in products:
                j.price = j.original_price 
                j.save()
        return redirect('adminoffer')

    else:
        def is_today_between(start_date, end_date):
            today = timezone.now().date()
            return start_date <= today <= end_date
        
        if is_today_between(offer.start_date,offer.end_date):    
            if Offer.objects.filter(is_active = 1).exists():
                messages.warning(request, 'You can only activate one offer at a time!')
                return redirect('adminoffer')
        else:
            messages.warning(request, 'You can only activate an offer when the offer within start and end date')
            return redirect('adminoffer')
        offer.is_active = 1
        offer.save()
        category = offer.categoryEligible.all()
        for i in category:
            products = i.category.products.all()
            for j in products:
                value = float(j.original_price)  * (offer.discount/100)
                j.price = float(j.original_price) - float(value)
                j.save()
        return redirect('adminoffer')
    
    


