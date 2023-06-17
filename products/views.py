from django.shortcuts import render,get_object_or_404,redirect
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from products.models import Product
from django.core.paginator import Paginator
from django.db.models import Q
from .models import ReviewRating,Wishlist
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from accounts.models import UserProfile
# Create your views here.

def products(request,category_slug=None):
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=categories,is_available=True)
        paginator = Paginator(products,16)   
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        
    else:
        products = Product.objects.all().filter(is_available=True) #need changes
        product_count = products.count()  #need changes
    context = {
        'products' : paged_products,
        'product_count' : product_count,
    }
    return render(request,'products/products.html',context)

@never_cache
def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        
    except Exception as e:
        raise e
    user_profile =  None
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user,product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None    
    else:
        orderproduct = None
    
    reviews = ReviewRating.objects.filter(product_id = single_product.id,status=True)
    
    context = {
        'single_product' : single_product,
        'in_cart' : in_cart,
        'orderproduct' : orderproduct,
        'reviews':reviews,
        'user_profile':user_profile,
    }
    return render(request,'products/product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products' : products, 
        'product_count' : product_count,
    }
    return render(request,'products/products.html',context)
 
def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            form = ReviewForm(request.POST,instance=reviews)
            form.save()
            messages.success(request,'Thank You! Your Review Have Been Updated')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request,'Thank You! Your Review Have Been Submitted')
                return redirect(url)
            
# def add_wishlist(request):
#     pid=request.GET['product']
#     product = Product.objects.get(pk=pid)
#     data={}
#     checkwishlist = Wishlist.objects.filter(product=product,user=request.user).count()
#     if checkwishlist > 0:
#         pass
    
#     wishlist = Wishlist.objects.create(
#         product=product,
#         user=request.user
#     )
#     return JsonResponse({'bool':True})
    
            
                