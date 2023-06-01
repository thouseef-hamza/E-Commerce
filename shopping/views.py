from products.models import Product 
from category.models import Category
from django.shortcuts import render
from django.views.decorators.cache import never_cache

# Create Your Views Here

def homePage(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories
    }
    return render(request, "home.html",context)