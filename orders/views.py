from django.shortcuts import redirect, render
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse

from carts.models import CartItem
from .forms import OrderForm, Order
from orders.models import Payment, OrderProduct
from products.models import Product
import datetime
import json

# Create your views here.


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=body["orderID"]
    )
    # Storing Transaction Details In Payment Model
    payment = Payment(
        user=request.user,
        payment_id=body["transID"],
        payment_method=body["payment_method"],
        amount_paid=order.order_total,
        status=body["status"],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move The Cart Items To Order Product Table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        # Reduce The Qantity Of The Sold Products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear Cart
    CartItem.objects.filter(user=request.user).delete()

    # Send Order And Recieved Email To Customer
    mail_subject = "Thank You For Purchasing Our Product"
    message = render_to_string(
        "orders/order_recieved_email.html",
        {"user": request.user, "order": order},
    )
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # Send Order Number And Transaction Id Back To sendData method via Jsonresponse
    data = {
        "order_number": order.order_number,
        "transID": payment.payment_id,
    }
    return JsonResponse(data)
    return render(request, "orders/payments.html")


def place_order(request, total=0, quantity=0):
    current_user = request.user

    # If The Cart Count is <= 0,then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect("products")

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            # Storing All The Billing Information inside Order Table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data["first_name"]
            data.last_name = form.cleaned_data["last_name"]
            data.phone = form.cleaned_data["phone"]
            data.email = form.cleaned_data["email"]
            data.address_line_1 = form.cleaned_data["address_line_1"]
            data.address_line_2 = form.cleaned_data["address_line_2"]
            data.country = form.cleaned_data["country"]
            data.state = form.cleaned_data["state"]
            data.city = form.cleaned_data["city"]
            data.order_note = form.cleaned_data["order_note"]
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get("REMOTE_ADDR")
            data.save()
            # Generate Order Number
            yr = int(datetime.date.today().strftime("%Y"))
            mt = int(datetime.date.today().strftime("%m"))
            dt = int(datetime.date.today().strftime("%d"))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime(
                "%Y%m%d"
            )  # This will be todays Date Eg:- 20230529
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number
            )
            context = {
                "order": order,
                "cart_items": cart_items,
                "total": total,
                "tax": tax,
                "grand_total": grand_total,
            }
            return render(request, "orders/payments.html", context)
    else:
        return redirect("checkout")


def order_complete(request):
    order_number = request.GET.get("order_number")
    transID = request.GET.get("payment_id")

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        sub_total = 0
        for i in ordered_products:
            sub_total += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            "order": order,
            "ordered_products": ordered_products,
            "order_number": order.order_number,
            "transID": payment.payment_id,
            "payment": payment,
            "sub_total": sub_total,
        }
        return render(request, "orders/order_complete.html", context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect("home")
