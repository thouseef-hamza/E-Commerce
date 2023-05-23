from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
import re
from django.views import generic
from .models import Account

class SignUpForm(UserCreationForm): 
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-content','placeholder':'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-content','placeholder':'Last Name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'forms-content','placeholder':'Username'}))
    email = forms.EmailField(max_length=50,widget=forms.TextInput(attrs={'class':'form-content','placeholder':'Enter Your Email'}))
    password1 = forms.CharField(min_length=4,max_length=16,widget=forms.PasswordInput(attrs={'class':'form-content','placeholder':'Enter Your Password'}))
    password2 = forms.CharField(min_length=4,max_length=16,widget=forms.PasswordInput(attrs={'class':'form-content','placeholder':'Confirm Your Password'}))
    
    class Meta:
        model=Account
        fields = ('first_name','last_name','username','email','password1','password2')
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Account.objects.filter(username=username).exists():
            if Account.objects.get(username=username).is_active == False:
                return username
            raise forms.ValidationError('This username is already taken.')
        # elif not re.match('^(?=.{8,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$',username):
        #     raise forms.ValidationError('Username Must Contains Alphabetics and Numerics')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Account.objects.filter(email=email).exists():
            if Account.objects.get(email=email).is_active == False:
                return email
            raise forms.ValidationError('This email is already taken.')
        return email
        
    def __init__(self, *args, **kwargs):
            super(SignUpForm, self).__init__(*args, **kwargs)
            
            self.fields['first_name'].widget.attrs['placeholder'] = 'First Name' 
            self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name' 
            self.fields['username'].widget.attrs['placeholder'] = 'Username' 
            self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email' 
            
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-content'



        