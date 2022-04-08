from django import forms
from django.forms.widgets import EmailInput, FileInput, PasswordInput, TextInput, Textarea
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,get_user_model
from index.models import CustomUser

User = get_user_model()
class Loginform(forms.Form):
    username = forms.CharField()
    password = forms.CharField( widget=forms.PasswordInput)
    
    
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active")
        return super(Loginform, self).clean(*args, **kwargs)  






class RegistertionForm(forms.Form):
    username = forms.CharField(widget=TextInput(
        attrs={ 'class': 'validate form-control', 
         'placeholder': 'Full Name', 'type': 'text',
          'id': 'Full name'}),
           min_length=2, max_length=150
        )

    email = forms.CharField(widget=EmailInput(
        attrs={'class': 'validate form-control', 
         'type': 'email', 'placeholder': 'Enter your email address',
          'id': 'email'
        }))
    password = forms.CharField(widget=PasswordInput(
        attrs={'class': 'validate form-control', 
        'type': 'password', 'placeholder': 'Password', 
        'id': 'password'
        }))
    Confirm_password = forms.CharField(widget=PasswordInput(
        attrs={'class': 'validate form-control', 
         'type': 'password', 'placeholder': 'Confirm-password',
         'id': 'password2'
        }))
    
    
    
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        qs = User.objects.filter(username=username)
        if qs.count():
            raise forms.ValidationError("Name already exists")
        return username
    
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  forms.ValidationError("Email already exists")
        return email
    

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError("Password don't match")

        return password2
    
    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            # full_name =self.cleaned_data['full_name'],
            # number=self.cleaned_data['number'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            # description=self.cleaned_data['description'],
        )
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'fullname', 
            'phonenumber', 
            ]
        
        

    

 
    
    
    
    