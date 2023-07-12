from django.shortcuts import render,redirect
from .models import Category

# Create your views here.
def category(request):
    category = Category.objects.all()
    return render(request,'category/category.html',{'category':category})

def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        Category.objects.create(name = name, image = image)
        return redirect('category')
    
def delete_category(request,id):
    category = Category.objects.get(id = id)
    category.delete()
    return redirect('category')

def edit_category(request,id):
    category = Category.objects.get(id = id)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.image = request.FILES.get('image')
        category.save()
        return redirect('category')




