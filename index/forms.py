from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Contact, CustomUser, ShippingAddress

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'email', 'street_address', 'apartment_address',
         'phone', 'country', 'city','state','zipcode']
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder': 'Full Name',
    }))
    # last_name = forms.CharField(widget=forms.TextInput(attrs={
    #     'class':'form-control',
    #     'type':'text',
    #     'placeholder': '',
    # }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder': 'Email address',
    }))
    country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
            'class':'form-control',
        }))
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '1234 main st'
    })) 
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 
      'form-control', 'placeholder': 'Apartment or suit'}))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    zipcode = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))  
    state = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control',
    })) 
    phone = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control',
    }))


class FeedbackForm(forms.ModelForm):
    
    class Meta:
        model = Contact
        fields = '__all__'

class EditAccount(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            # 'fullname',
            'phonenumber',
            'email',
            # 'username'
        ]



   