from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Contact, CustomUser, ShippingAddress


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'email', 'address', 'address2', 'phone', 'country', 'city','state','zipcode']
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'type':'text',
        'id': 'full_name',
        'placeholder': 'Full Name',
    }))
    # last_name = forms.CharField(widget=forms.TextInput(attrs={
    #     'class':'form-control',
    #     'type':'text',
    #     'placeholder': '',
    # }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'type':'email',
        'placeholder': '',
    }))
    country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
            'class':'form-control',
            'id': 'country',
            'name': 'country',
        }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Address 1',
        'id': 'address_1'
    })) 
    address2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Address 2',
        'id': 'address_2'
    })) 
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    zipcode = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'zipcode',
    }))  
    state = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control',
         'id': 'state',
    })) 
    phone = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control'
    }))


class FeedbackForm(forms.ModelForm):
    
    class Meta:
        model = Contact
        fields = '__all__'

class EditAccount(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'fullname',
            'phonenumber',
            'email',
            # 'username'
        ]



   