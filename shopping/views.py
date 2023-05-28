from products.models import Product 
from category.models import Category
from django.shortcuts import render

# Create Your Views Here

def homePage(request):
    # products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.all()
    context = {
        'categories' : categories
    }
    return render(request, "home.html",context)