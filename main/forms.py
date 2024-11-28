from typing import Any
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Request, UserProfile, Offer
from django_countries.fields import CountryField
from django.contrib.auth.forms import PasswordResetForm


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'uk-input', 'placeholder': 'Enter your email address'}))

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['producer', 'created']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'uk-input'})

        
        # Customize specific fields
        self.fields['description'].widget.attrs.update({'rows': 4, 'style': 'height: 100px;'})
        self.fields['category'].widget.attrs.update({'size': 5, 'style': 'height: auto;'})
        self.fields['image'].widget.attrs.update({'class': 'img-input'})
        

class UserEditForm(forms.ModelForm):

    # country = forms.CountryField(required=False)
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'profile_image', 'phone_number', 'address', 'company_name', 'country']
        widgets = {
            'user_type': forms.RadioSelect()            
        }

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'uk-input'})

        self.fields['profile_image'].widget.attrs.update({'class': 'img-input'})

class CustomUserCreationForm(UserCreationForm):

    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES)
    country = CountryField(blank_label='Select country').formfield() 

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'user_type', 'country']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last name'
        }
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'uk-input'})


class RequestOfferForm(ModelForm):
    class Meta:
        model = Request
        fields = ['quantity', 'additional_notes']

    def __init__(self, *args, **kwargs):
        super(RequestOfferForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'uk-input'})

class SendOfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ['unit_price', 'total_price', 'delivery_timeline', 'additional_notes']

    def __init__(self, *args, **kwargs):
        super(SendOfferForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'uk-input'})

class OfferEditForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['unit_price', 'total_price', 'delivery_timeline', 'additional_notes']

    def __init__(self, *args, **kwargs):
        super(OfferEditForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'uk-input'})
# class SendInvoiceForm(ModelForm):
#     class Meta:
#         model = Invoice
#         fields = []

#     def __init__(self, *args, **kwargs):
#         super(SendInvoiceForm, self).__init__(*args, **kwargs)

#         for name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'uk-input'})
