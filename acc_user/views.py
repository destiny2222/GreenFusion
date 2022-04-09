from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate, login,logout
from .forms import  *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User

from solar import settings
from django.conf import settings
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.utils.translation import gettext_lazy as _




User = get_user_model()

def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(username, password)
        if user != None:
            login(request, user)
            # messages.success(request, 'successful login')
            return redirect('index:home')
        else:
            messages.error(request, 'There is an error loging in.')
            return redirect('index:login')
    return render(request, 'login.html')


def RegisterView(request):
    form = RegistertionForm()
    if request.method == "POST":
        form = RegistertionForm(request.POST or None)
        if form.is_valid():
            form.save()
            # profile.objects.create(user=form)
            # user = form.cleaned_data.get('first_name')
            messages.success(request, "Successful create an account.")
            return redirect("index:login")
        else:
            messages.error(request,  form.errors)
            # messages.error(request, "Unsuccessful password_reset. Invalid information.")      
    return render(request, 'signup.html', {"form": form})

@login_required(login_url='index:login') 
def logout_View(request):
	logout(request)

	return redirect('index:login')


@login_required(login_url='index:login')    
def dashboard_view(request):
    qs= User.objects.all()[1:]
    context = {'tar':qs}
    return render(request, 'dashboard/index.html', context)

@login_required(login_url='index:login')
def profileView(request):
        form = ProfileUpdateForm()
        if request.method == 'POST':
            form = ProfileUpdateForm(data=request.POST or None,instance=request.user, files=request.FILES )
           
            if form.is_valid():
                form.save()
                messages.success(request,'your profile is set')
                return redirect('index:profile')
            else:
                messages.error(request,  form.errors)
                # form = ProfileUpdateForm(instance=request.user) 
        return render(request, 'dashboard/edit_student.html',{'form':form}) 

@login_required(login_url='index:login')
def other_user_profile(request, slug):
    other_user = get_object_or_404(User, id=slug)
    user_profile = User.objects.get(id=slug)
     
    context = {
         'user_profile': user_profile,
         'other_user':other_user,
     }
    return render(request, 'dashboard/profile.html', context)




