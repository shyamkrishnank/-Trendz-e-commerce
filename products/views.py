from django.shortcuts import render,redirect
from category.models import Category
from .models import Products,ProductImage,Varient
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PILImage
import io

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
        varient = Varient.choice
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
            var = request.POST.getlist('varient')
            discription = request.POST.get('discription')
            current = Products.objects.create(name=name,category=category,price = price1, original_price = price1 , stocks=stock, discription = discription)
            for i in Varient.choice:
                if i[1] in var:
                    Varient.objects.create(product = current, varient = i[0])               
            
            image_fields = [image1, image2, image3]

            for idx, image_field in enumerate(image_fields):

                if image_field:
                    pil_image = PILImage.open(image_field)

                    # Define the desired crop ratio (e.g., 2:3)
                    crop_ratio = (2, 3)

                    # Get the width and height of the original image
                    width, height = pil_image.size

                    # Set default values for new_width and new_height
                    new_width, new_height = width, height

                    # Calculate the aspect ratio of the original image
                    original_ratio = width / height

                    # Calculate the new dimensions to achieve the 2:3 aspect ratio
                    if original_ratio > crop_ratio[0] / crop_ratio[1]:
                        new_width = int(height * crop_ratio[0] / crop_ratio[1])
                    else:
                        new_height = int(width * crop_ratio[1] / crop_ratio[0])

                    # Calculate the cropping box to center the image
                    left = (width - new_width) // 2
                    top = (height - new_height) // 2
                    right = left + new_width
                    bottom = top + new_height

                    # Crop the image
                    cropped_image = pil_image.crop((left, top, right, bottom))

                    print(f"Width: {width}, Height: {height}")
                    print(f"New Width: {new_width}, New Height: {new_height}")
                    print(f"Cropping Box: left={left}, top={top}, right={right}, bottom={bottom}")

                    # Save the cropped image as a file-like object
                    cropped_image_io = io.BytesIO()
                    image_format = image_field.content_type.split('/')[-1].lower()  # Get the file extension from content type
                    cropped_image.save(cropped_image_io, format=image_format)

                    # Create a SimpleUploadedFile from the cropped image data
                    cropped_image_file = SimpleUploadedFile(
                        name=f"{image_field.name}.{image_format}",
                        content=cropped_image_io.getvalue(),
                        content_type=image_field.content_type
                    )

                    # Create a ProductImage instance and save it to the database
                    product_image = ProductImage(product=current, image=cropped_image_file)
                    product_image.save()

            return redirect('product_details', id=id)
           
                        
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
            var = request.POST.getlist('varient')
            if request.FILES.get('image'):
                images = request.FILES.get('image')
                img =ProductImage.objects.filter(product=product)
                img.delete()
                for image in images:
                    ProductImage.objects.create(product = product,image = image)
            product.discription = request.POST.get('discription')
            product.save()
            check = Varient.objects.filter(product = product)
            check.delete()
            for i in Varient.choice:
                if i[1] in var :
                    Varient.objects.create(product = product, varient = i[0])
                    
            return redirect('product_details',id)




    
        


