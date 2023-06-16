# Django
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
# Local Django
from .forms import SignUpForm,UserForm,UserProfileForm
from .models import Account,UserProfile
from carts.models import Cart,CartItem
from carts.views import _cart_id
from orders.models import Order

# 
import requests

# Email Verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required


# Create your views here.
@never_cache
def logInPage(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request)) 
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    for item in cart_item:
                        item.user=user
                        item.save()
            except:
                pass     
            auth.login(request, user) 
            url = request.META.get('HTTP_REFERER') #------> http://127.0.0.1:8081/accounts/login/?next=/cart/checkout/
            try:
                query = requests.utils.urlparse(url).query #-----------> next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage=params['next']
                    return redirect(nextPage)
            except:
                return redirect("homePage")
        else:
            messages.error(request, "Invalid Login Credentials")
            return redirect("loginPage")
    else:
        return render(request, "accounts/login.html")

@never_cache
def signUpPage(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            existing_user = Account.objects.get(email=email, is_active=False)
            existing_user.delete()
        except Account.DoesNotExist:
            pass
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Authentication And Login
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            
            user.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = "Please Activate Your Account"
            message = render_to_string(
                "accounts/account_verification_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # login(request,user)
            # messages.success(request, "Thank You For Registering With Us, We Have Sent You An Email \n Please Verify!")
            return redirect("/accounts/login?command=verification&email=" + email)
    else:
        form = SignUpForm()
    context = {
        'form':form
    }
    return render(request, "accounts/signup.html", context)


@login_required(login_url="loginPage")
def logOutPage(request):
    auth.logout(request)
    # messages.success(request, "You Have Been Logged Out!!.................")
    return redirect("homePage")


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulation! Your Account is Activated")
        return redirect("loginPage")
    else:
        messages.success(request, "Invalid Activation Link")
        return redirect("signUpPage")


def forgotPassword(request):
    if request.method == "POST":
        email = request.POST["email"]
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset Password Email
            current_site = get_current_site(request)
            mail_subject = "Please Activate Your Account"
            message = render_to_string(
                "accounts/reset_password_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, "Password Reset has been Sent To Your Email")
            return redirect("loginPage")
        else:
            messages.success(request, "Account Does not exist")
            return redirect("forgotPassword")
    return render(request, "accounts/forgotPassword.html")


def resetPassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Please Reset Your Password")
        return redirect("resetPassword")
    else:
        messages.error(request, "This Link Has Been Expired")
        return redirect("loginPage")


def resetPassword(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            uid = request.session.get("uid")
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password Reset Successful")
            return redirect("loginPage")
        else:
            messages.error(request, "Password Do Not Match")
            return redirect("resetPassword")
    else:
        return render(request, "accounts/resetPassword.html")

@login_required(login_url='loginPage')
def dashboard(request):
    # user_profile = get_object_or_404(UserProfile,user=request.user)
    try:
        user_profile = UserProfile.objects.filter(user=request.user).get()
    except UserProfile.DoesNotExist:
        user_profile = None
    orders = Order.objects.order_by('-created_at').filter(user_id = request.user.id,is_ordered=True)
    orders_count = orders.count()
    context={
        'user_profile':user_profile,
        'orders_count':orders_count,
    }
    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='loginPage')
def edit_profile(request):
    user_profile = get_object_or_404(UserProfile,user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance=request.user)
        profile_form = UserProfileForm(request.POST,request.FILES,instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your Profile Has Been Updated')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    context = {
        'user_form' : user_form ,
        'profile_form' : profile_form,
        'user_profile':user_profile,
    }
    return render(request,'accounts/edit_profile.html',context)

@login_required(login_url='loginPage')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        user = Account.objects.get(username__exact=request.user.username)
        
        if new_password == confirm_password:
            success=user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password Update Successfully')
                return redirect('change_password')
            else:
                messages.error(request,'Please Enter Valid Current Password')
                return redirect('change_password')
        else:
            messages.error(request,"Password Didn't Matched")
    return render(request,'accounts/change_password.html')

@login_required(login_url='loginPage')
def my_orders(request):
    orders = Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    print(orders)
    context = {
        'orders' : orders
    }
    return render(request,'accounts/my_orders.html',context) 