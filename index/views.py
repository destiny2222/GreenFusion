from django.conf import settings
from importlib_metadata import email
from .forms import CheckoutForm, EditAccount,FeedbackForm
from django.shortcuts import get_object_or_404, render,redirect
from django.views.generic import ListView, DetailView, TemplateView
from .models import *
from django.contrib import messages
import environ, math, random, requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, request
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from  Homepage.models  import *
from  Aboutpage.models  import *
import json
# from .utils import  cartData
from django.core.mail import mail_admins,send_mail

env = environ.Env()
environ.Env.read_env()


# Create your views here.

def products(request):
    context = {
        'items': Product.objects.all()
    }
    return render(request, "products.html", context)

def getCategoryItems(request, id):
    category1 = get_object_or_404(Category, id=id)
    items = Product.objects.filter(category=category1)
    context = {'items':items}
    return render(request, 'product.html', context)

class HomeView(ListView):
    model = Product
    paginate_by = 10
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['book_list'] = Blog.objects.all()
        context['slide'] = SilderSection.objects.all()
        context['aboutus'] = AboutSection.objects.all()
        return context


def AboutView(request):
    about = About.objects.all()
    context = {'about':about}
    return render(request,  'about.html', context)

    

class BlogView(ListView):
    model = Blog
    template_name = "blog.html"

class BlogDetails(DetailView):
    model = Blog
    template_name = "single.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['recents'] = Blog.objects.all().order_by('-id')[:5]
        return context    


def store(request, slug):
    products = Product.objects.get(id=slug)
    context = {'products':products}
    return render(request, 'product.html', context)



@login_required(login_url='/accounts/login/')
def wish_details(request):
    wish = Wishlist.objects.filter(user=request.user)
       
    context = {'wish':wish}
    return render(request, 'wishlist.html', context)    

@login_required(login_url='/accounts/login/')
def WishlistView(request, id):
        wish_list = Product.objects.get(id=id)
        Wishlist.objects.create(product=wish_list, user=request.user)  
        return redirect('index:wish')

@login_required(login_url='/accounts/login/')
def wishlist_increment(request, slug):
    qr = Wishlist.objects.get(user=request.user, id=slug)
    qr.quantity = qr.quantity + 1
    qr.save()
    return redirect('index:wish')

@login_required(login_url='/accounts/login/')
def wishlist_decrement(request, slug):
    qr = Wishlist.objects.get(user=request.user, id=slug)
    if qr.quantity >=1:
        qr.quantity = qr.quantity - 1
        qr.save()
    return redirect('index:wish')

@login_required(login_url='/accounts/login/')
def wish_delete(request, slug):
    qs = Wishlist.objects.get(user=request.user, id=slug)
    qs.delete()
    return redirect('index:wish')

@login_required(login_url='/accounts/login/')
def cart(request, id):
    add = Product.objects.get(id=id)
    CartModel.objects.create(product=add, user=request.user, quantity=1)
    return redirect('index:cart')

@login_required(login_url='/accounts/login/')
def cart_increment(request, id):
    qs = CartModel.objects.get(user=request.user, id=id, order=False)
    qs.quantity = qs.quantity + 1
    qs.save()
    return redirect('index:cart')

@login_required(login_url='/accounts/login/')
def cart_decrement(request, id):
    qs = CartModel.objects.get(user=request.user, id=id, order=False)
    if qs.quantity >=1:
        qs.quantity = qs.quantity - 1
        qs.save()
    return redirect('index:cart')

@login_required(login_url='/accounts/login/')
def cart_delete(request, id):
    qs = CartModel.objects.get(user=request.user, id=id, order=False)
    qs.delete()
    return redirect('index:cart')

@login_required(login_url='/accounts/login/')
def cart_details(request):
    qs = CartModel.objects.filter(user=request.user, order=False)
    context = {'qs':qs}
    return render(request, 'cart.html', context)

@login_required(login_url='/accounts/login/')
def checkout(request):
    cartcheck = CartModel.objects.filter(user=request.user, order=False)
    amount = '0'
    for i in cartcheck:
        print(float(amount) + (float(i.product.price) * float(i.quantity) ))
        amount = float(amount) + (float(i.product.price) * float(i.quantity) )
    context = {'cartcheck':cartcheck, 'amount':amount}
    return render(request, 'checkout.html',context,{})

# def checkout(request):
#     cartcheck = CartModel.objects.filter(user=request.user, order=False)
#     if request.method=='POST':
#         full_name=request.POST['full_name']
#         address=request.POST['address']
#         address2=request.POST['address2']
#         city=request.POST['city']
#         phone=request.POST['phone']
#         state=request.POST['state']
#         zipcode=request.POST['zipcode']
#         country=request.POST['country']
#         email=request.POST['email']
#         user=ShippingAddress.objects.create(
#             full_name=full_name,address=address,
#             phone=phone,state=state,
#             address2=address2, email=email,
#             city=city,zipcode=zipcode,country=country)
#         user.save()
#         return render(request, 'payment.html',{"email":email,'phone':phone,})
#     else:
#         amount = '0'
#         for i in cartcheck:
#             print(float(amount) + (float(i.product.price) * float(i.quantity) ))
#             amount = float(amount) + (float(i.product.price) * float(i.quantity) )
#     context = {'cartcheck':cartcheck, 'amount':amount}
#     return render(request, 'checkout.html',context)



def ContactView(request):
    if request.method == 'POST':
        f = FeedbackForm(request.POST)
        if f.is_valid():
            name = f.cleaned_data['name']
            sender = f.cleaned_data['email']
            subject = "You have a new Feedback to Tutor me from {}:{}".format(name, sender) 
            message = "Subject: {}\n\nMessage: {}".format(f.cleaned_data['email'], f.cleaned_data['message'])
            mail_admins(subject, message, fail_silently=False)
            f.save()
            messages.add_message(request, messages.INFO, 'Feedback Submitted.')
            return redirect('index:contact')
    else:
        f = FeedbackForm()
    return render(request, 'contact.html', {'form': f})



class projectView(TemplateView):
    model = Project
    template_name = 'project.html'    


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['project'] = Project.objects.all()
        return context
    

# def verify_paystack_payment(request):
#     if request.method == 'POST':
#        email = request.POST.get('')
#        amount = request.POST.get('')
#        ref = request.POST.get('ref') 
#        url = "https://api.paystack.co/transaction/verify/262762380" + ref
#        payload = {
#             "email": "email@yahoo.com",
#             "amount": "10000",
#             "currency": "NGN",
#             "reference": "262762380",
#             "metadata": {
#                 "custom_fields": [
#                     {
#                         "display_name": "Mobile Number",
#                         "variable_name": "mobile_number",
#                         "value": "+2348012345678"
#                     }
#                 ]
#             }
#         }

#     files = {}

#     headers = {
#       'Authorization': 'Bearer **MY SECRET KEY**',
#       'Content-Type': 'application/json'
#     }

#     response = requests.request("GET", url, headers=headers, data= payload, files=files)
#     return JsonResponse({"data":response.text})

def dashboard(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    form = EditAccount(request.POST or None)
    if request.method == 'POST':
        form = EditAccount(data=request.POST or None,instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successful edit your account')
            return redirect('index:dashboard')
        else:
            messages.error(request, form.errors)    
    context = {'wishlist':wishlist,'form': form}        
    return render(request, 'account/dashboard.html',context)        



def search(request):
    Post = []
    searched = request.POST['searched']
    if searched:
        Post = Category.objects.filter(name__contains=searched)
        print(searched)
    content ={
        'Post':Post,
        # 'form':form,
        'searched':searched,
    }
    return render(request,  'search.html',content)    
