from products.models import Product 
from category.models import Category
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from products.models import ReviewRating
# Create Your Views Here

def homePage(request):
    categories = Category.objects.all()
    
    products = Product.objects.all().filter(is_available=True)
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id,status=True)
    context = {
        'categories' : categories,
        'reviews' : reviews,
    }
    return render(request, "home.html",context)