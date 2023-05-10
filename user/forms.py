from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms
import re
from django.views import generic

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-content','placeholder':'First Name'}))
    last_name = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-content','placeholder':'Last Name'}))
    username = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'forms-content','placeholder':'Enter Your Username'}))
    email = forms.EmailField(label='',max_length=50,widget=forms.TextInput(attrs={'class':'form-content','placeholder':'Enter Your Email'}))
    password1 = forms.CharField(label='',min_length=4,max_length=16,widget=forms.PasswordInput(attrs={'class':'form-content','placeholder':'Enter Your Password'}))
    password2 = forms.CharField(label='',min_length=4,max_length=16,widget=forms.PasswordInput(attrs={'class':'form-content','placeholder':'Confirm Your Password'}))
    
    class Meta:
        model=User
        fields = ('first_name','last_name','username','email','password1','password2')
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        elif not re.match('^[A-Za-z0-9_]$',username):
            raise forms.ValidationError('Username Must Contains Alphabetics and Numerics')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already taken.')
        return email
        
    def __init__(self, *args, **kwargs):
            super(SignUpForm, self).__init__(*args, **kwargs)

            self.fields['username'].widget.attrs['class'] = 'form-content'
            self.fields['username'].widget.attrs['placeholder'] = 'User Name'
            self.fields['username'].label = ''
            self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

            self.fields['password1'].widget.attrs['class'] = 'form-content'
            self.fields['password1'].widget.attrs['placeholder'] = 'Password'
            self.fields['password1'].label = ''
            self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

            self.fields['password2'].widget.attrs['class'] = 'form-content'
            self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
            self.fields['password2'].label = ''
            self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	


# class ProfileForm(UserChangeForm):
    
    
#         model = User
#         fields = ('firstname','lastname','username','email','address','phonenumber')
    
            


    