# Django
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# Local Django
from .forms import SignUpForm,UserForm,UserProfileForm
from .models import Account,UserProfile

# Email Verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.


def logInPage(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect("homePage")
        else:
            messages.error(request, "Invalid Login Credentials")
            return redirect("loginPage")
    else:
        return render(request, "accounts/login.html")


def signUpPage(request):
    if request.method == "POST":
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
            return redirect("/?command=verification&email=" + email)
    else:
        form = SignUpForm()
        return render(request, "accounts/signup.html", {"form": form})
    return render(request, "accounts/signup.html", {"form": form})


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
    return render(request,'accounts/dashboard.html')

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
    }

    
    return render(request,'accounts/edit_profile.html',context)