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
        varient = Products.choice
        return render(request,'products/product_details.html',{'products':product,'category':category,'current':current_category,'varient':varient})

def add_product(request,id):
    if 'admin_username' in request.session:
        if request.method == 'POST':
            name = request.POST.get('name')
            category = Category.objects.get(id = id)
            price1 = request.POST.get('price')
            stock = request.POST.get('stock')
            image1 = request.FILES.get('images1')
            image2 = request.FILES.get('images2')
            image3 = request.FILES.get('images3')
            var = request.POST.get('varient')
            discription = request.POST.get('discription')
            current = Products.objects.create(name=name,category=category,price = price1, original_price = price1 , stocks=stock, discription = discription)
            for i in Products.choice:
                if i[1] == var:
                    current.varient = i[0]    
                    current.save()  
                    break            
            ProductImage.objects.create(product = current,image = image1)
            ProductImage.objects.create(product = current,image = image2)
            ProductImage.objects.create(product = current,image = image3)


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
            product.original_price = request.POST.get('price')
            product.stocks = request.POST.get('stock')
            if request.FILES.get('image'):
                images = request.FILES.get('image')
                img =ProductImage.objects.filter(product=product)
                img.delete()
                for image in images:
                    ProductImage.objects.create(product = product,image = image)
            for i in Products.choice:
                if i[1] == request.POST.get('varient'):
                    product.varient = i[0]
            product.discription = request.POST.get('discription')
            product.save()
            

            return redirect('product_details',id)




    
        


