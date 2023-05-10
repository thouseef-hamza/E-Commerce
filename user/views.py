from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.views import generic
from django.urls import reverse_lazy

# Create your views here.


def logInPage(request):
    if 'username' in request.session:
        return redirect('homePage')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = authenticate(request,username=username,password=password)
        print(user)
        if user is not None:
            request.session['username'] = username
            # login(request,user)
            print('Home Page Entering.........................................................')
            messages.success(request,'You Have Been Logged In')
            return redirect('homePage') 
        else:
            print('Log In Page Entering.................................................................')
            messages.success(request,'There Was An Error Logging In, Please Try Again....')
            return redirect('loginPage')
    else:
        print('Not Worked...............................................................................')
        return render(request,'userside/login.html',{})


def signUpPage(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authentication And Login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,'You Have Been Successfully Registered')
            print('success')
            return redirect('loginPage') 
    else:
        form = SignUpForm()    
        print('failure')
        return render(request,'userside/signup.html',{'form':form})
    print('nothing')
    return render(request,'userside/signup.html',{'form':form})


def homePage(request):
    if 'username' in request.session:
        return render(request,'index.html')
    else:
        return redirect('loginPage')


def logOutPage(request):
    if 'username' in request.session: 
        logout(request)
        messages.success(request,'You Have Been Logged Out!!.................')
        return redirect('loginPage')
    else:
        return redirect('homePage')

def forget_password(request):
    return render(request,'userside/forget_password.html')

# def edit_profile(request):
#     form=ProfileForm(instance=request.user)
#     return render(request,'userside/edit_profile.html',{'form':form})

# class UserEditView(generic.CreateView):
#     form_class = Use

class UserEditView(generic.CreateView):
    form_class =  UserChangeForm
    template_name = 'userside/edit_profile.html'
    success_url = reverse_lazy('home')
    