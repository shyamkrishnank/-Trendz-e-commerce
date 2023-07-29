from django.shortcuts import render,redirect
from accounts.models import *
from .models import *
from category.models import *
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
    else:
        offer.is_active = 1
    offer.save()
    return redirect('adminoffer')
    
    


