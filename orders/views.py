from django.shortcuts import redirect,render


from carts.models import CartItem
from .forms import OrderForm,Order

import datetime
# Create your views here.

def payments(request):
    return render(request,'orders/payments.html')

def place_order(request,total=0,quantity=0):
    current_user = request.user
    print(current_user)

    # If The Cart Count is <= 0,then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <=0:
        return  redirect('products')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (18 * total)/100
    grand_total = total + tax    
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Storing All The Billing Information inside Order Table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate Order Number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,dt,mt)
            current_date = d.strftime('%Y%m%d') #This will be todays Date Eg:- 20230529
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            
            order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            context = {
                'order' : order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
            }
            return render(request,'orders/payments.html',context)
    else:
        return redirect('checkout')
            

            
             

            
            
            