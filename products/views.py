from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category
 
# Create your views here.

def products(request,category_slug=None):
    categories = None
    products = None
    
    if category_slug is not None:
        categories = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=categories,is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True) #need changes
        product_count = products.count()  #need changes
    context = {
        'products' : products,
        'product_count' : product_count,
    }
    return render(request,'products/products.html',context)

def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        raise e
    context = {
        'single_product' : single_product
    }
    return render(request,'products/product_detail.html',context)

