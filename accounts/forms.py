# Django
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
# Local Django
from .models import Account,UserProfile
import re

def validate_username(username):
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9_]*$'
    if not re.match(pattern, username):
        raise ValidationError(
            ("Username must start with an alphabetical or numeric character and should not contain special characters."),
            code='invalid_username'
        )
    if not re.search(r'\d', username):
        raise ValidationError("Username must contain at least one digit.")


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "First Name"}
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Last Name"}
        )
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username"}
        )
    )
    email = forms.EmailField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter Your Email"}
        ),
    )
    password1 = forms.CharField(
        min_length=8,
        max_length=16,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter Your Password"}
        ),
    )
    password2 = forms.CharField(
        min_length=8,
        max_length=16,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm Your Password"}
        ),
    )

    class Meta:
        model = Account
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        validate_username(username)
        return username

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-content"
    
    

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name','last_name')
        
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].widget.attrs["placeholder"] = "First Name"
        self.fields['last_name'].widget.attrs["placeholder"] = "Last Name"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control bg-dark text-white"
            self.fields[field].widget.attrs["style"] = "border-color: #A32CC4"
        
class UserProfileForm(forms.ModelForm):
    
    profile_picture = forms.ImageField(required=False,error_messages={'invalid':('Image Files Only')},widget = forms.FileInput)
    
    class Meta:
        model = UserProfile
        fields = ('address_line_1','address_line_2','phone_number','city','state','country','profile_picture')
        
        def clean_phone_number(self):
            phone_number = self.cleaned_data['phone_number']
            if not str(phone_number).isdigit():
                raise ValidationError("Phone number must contain only digits")
            return phone_number
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['address_line_1'].widget.attrs["placeholder"] = "Address Line 1"
        self.fields['address_line_2'].widget.attrs["placeholder"] = "Address Line 2"
        self.fields['phone_number'].widget.attrs["placeholder"] = "Phone Number"
        self.fields['city'].widget.attrs["placeholder"] = "City"
        self.fields['state'].widget.attrs["placeholder"] = "State"
        self.fields['country'].widget.attrs["placeholder"] = "Country"
        
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control bg-dark text-white"
            self.fields[field].widget.attrs["style"] = "border-color: #A32CC4"