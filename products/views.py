from django.shortcuts import render,redirect
from category.models import Category
from .models import Products,ProductImage

# Create your views here.
def products(request):
    if 'admin_username' in request.session:
       category = Category.objects.all()
       return render(request,'products/products.html',{'category':category})

def product_details(request,id):
    if 'admin_username' in request.session:
        product = Products.objects.filter(category = id)
        category = Category.objects.all()
        current_category = Category.objects.get(id = id)
        return render(request,'products/product_details.html',{'products':product,'category':category,'current':current_category})

def add_product(request):
    if 'admin_username' in request.session:
        if request.method == 'POST':
            name = request.POST.get('name')
            id = request.POST.get('id')
            category = Category.objects.get(id=id)
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            images = request.FILES.getlist('images')
            discription = request.POST.get('discription')
            
            current = Products.objects.create(name=name,category=category,price = price, stocks=stock, discription = discription)
            
            for image in images:
                ProductImage.objects.create(product = current,image = image)

            return redirect('product_details',id)

def delete_product(request,id):
    if 'admin_username' in request.session:
        product = Products.objects.get(id=id)
        cat = product.category.id
        productimage = ProductImage.objects.filter(product=product)
        product.delete()
        productimage.delete()
        return redirect('product_details',cat)

def edit_product(request,id):
    if 'admin_username' in request.session:
        if request.method =='POST':
            product = Products.objects.get(id = id)
            product.name = request.POST.get('name')
            id = request.POST.get('id')
            product.category = Category.objects.get(id = id)
            product.price = request.POST.get('price')
            product.stocks = request.POST.get('stock')
            images = request.FILES.getlist('image')
            product.discription = request.POST.get('discription')
            product.save()
            img =ProductImage.objects.filter(product=product)
            img.delete()
            for image in images:
                ProductImage.objects.create(product = product,image = image)

            return redirect('product_details',id)




    
        


