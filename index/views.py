from unicodedata import category
from django.conf import settings
from .forms import  EditAccount,FeedbackForm,CheckoutForm
from django.shortcuts import get_object_or_404, render,redirect
from django.views.generic import ListView, DetailView, TemplateView
from .models import *
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from django.contrib import messages
import environ, math, random, requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse, HttpResponse, request
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from  Homepage.models  import *
from  Aboutpage.models  import *
import json
# from .utils import  cartData
from django.core.mail import mail_admins,send_mail

env = environ.Env()
environ.Env.read_env()

# from solar.settings import PAYSTACK_PUBLIC_KEY


# Create your views here.

def products(request):
    context = {
        'items': Product.objects.all()
    }
    return render(request, "products.html", context)

def getCategoryItems(request, slug):
    # category1 = get_object_or_404(Category, slug=slug)    
    # items = Category.objects.filter(category=category1)
    items = get_object_or_404(Category, slug=slug)
    if items.DoesNotExist():
        items = Product.objects.filter(category=items)
    else: 
         return redirect("index:404")      
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

    




def  BlogView(request):
    blog_list = Blog.objects.all()
    paginator = Paginator(blog_list, 20)
    page = request.GET.get('page')

    try:
        blog = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        blog = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        blog = paginator.page(paginator.num_pages)
    
    context = {
        'blog':blog,
        'page':page,
       
    }
    return render(request, 'blog.html', context)

def BlogDetails(request, slug):
    recents = Blog.objects.all().order_by('-id')[:5]
    details = get_object_or_404(Blog, slug=slug)
    context = {'recents':recents, 'post':details}
    return render(request, 'single.html', context)

   


def store(request, slug):
    products = Product.objects.filter(slug=slug)
    if products.exists():
        products = Product.objects.get(slug=slug)
    else:
        return redirect("index:404")
    context = {'products':products}
    return render(request, 'product.html', context)


def Error404(request):

    return render(request, '404.html')       

@login_required(login_url='/login/')
def wish_details(request):
    wish = Wishlist.objects.filter(user=request.user)
    context = {'wish':wish}
    return render(request, 'wishlist.html', context)    

@login_required(login_url='/login/')
def WishlistView(request, id):
        wish_list = Product.objects.get(id=id)
        Wishlist.objects.create(product=wish_list, user=request.user)  
        return redirect('index:wish')

@login_required(login_url='/login/')
def wishlist_increment(request, slug):
    qr = Wishlist.objects.get(user=request.user, id=slug)
    qr.quantity = qr.quantity + 1
    qr.save()
    return redirect('index:wish')

@login_required(login_url='/login/')
def wishlist_decrement(request, slug):
    qr = Wishlist.objects.get(user=request.user, id=slug)
    if qr.quantity >=1:
        qr.quantity = qr.quantity - 1
        qr.save()
    return redirect('index:wish')

@login_required(login_url='/login/')
def wish_delete(request, slug):
    qs = Wishlist.objects.get(user=request.user, id=slug)
    qs.delete()
    return redirect('index:wish')

@login_required(login_url='/login/')
def cart(request, id):
    add = Product.objects.get(id=id)
    CartModel.objects.create(product=add, user=request.user, quantity=1)
    return redirect('index:cart')

@login_required(login_url='/login/')
def cart_increment(request, id):
    qs = CartModel.objects.get(user=request.user, id=id, order=False)
    qs.quantity = qs.quantity + 1
    qs.save()
    return redirect('index:cart')

@login_required(login_url='/login/')
def cart_decrement(request, id):
    qs = CartModel.objects.get(user=request.user, id=id, order=False)
    if qs.quantity >=1:
        qs.quantity = qs.quantity - 1
        qs.save()
    return redirect('index:cart')

@login_required(login_url='/login/')
def cart_delete(request, id):
    qs = CartModel.objects.get(user=request.user, id=id, order=False)
    qs.delete()
    return redirect('index:cart')

@login_required(login_url='/login/')
def cart_details(request):
    qs = CartModel.objects.filter(user=request.user, order=False)
    context = {'qs':qs}
    return render(request, 'cart.html', context)

@login_required(login_url='/login/')
def checkout(request):
    cartcheck = CartModel.objects.filter(user=request.user, order=False)
    amount = '0'
    for i in cartcheck:
        print(float(amount) + (float(i.product.price) * float(i.quantity) ))
        amount = float(amount) + (float(i.product.price) * float(i.quantity) )
        if request.method == 'POST':
            form = CheckoutForm(request.POST)
            if form.is_valid():
                full_name = form.cleaned_data.get['full_name']
                email = form.cleaned_data.get['email']
                country = form.cleaned_data.get['country']
                city = form.cleaned_data.get['city']
                zipcode =form.cleaned_data.get['zipcode']
                phone =form.cleaned_data.get['phone']
                street_address = form.cleaned_data.get['street_address']
                apartment_address = form.cleaned_data.get['apartment_address']
                save_info = form.cleaned_data.get('save_info')
                use_default = form.cleaned_data.get('use_default')

                shippingaddress = ShippingAddress(
                    user = request.user,
                    street_address= street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zipcode=zipcode,
                    phone=phone,
                    city=city,
                    email=email,
                    # amount=amount,
                    full_name=full_name,
                )
                shippingaddress.save()
                if save_info:
                    shippingaddress.default = True
                    shippingaddress.save()

                cartcheck.address = shippingaddress
                cartcheck.save()

                if use_default:
                    shippingaddress = ShippingAddress.objects.get(
                        user=request.user, default=True)
                    cartcheck.shippingaddress = shippingaddress
                    cartcheck.save()
                return redirect(str(process_payment(full_name,email,amount,phone)))
            else:
                messages.warning(request, "Failed Checkout")
                return redirect('index:checkout')
        else:
            form = CheckoutForm()
    context = {'cartcheck':cartcheck, 'amount':amount}
    return render(request, 'checkout.html',context)

def process_payment(full_name,email,amount,phone):
    auth_token= env('SECRET_KEY')
    hed = {'Authorization': 'Bearer ' + auth_token}
    data = {
                "tx_ref":''+str(math.floor(1000000 + random.random()*9000000)),
                "amount":amount,
                "currency":"NGN",
                "redirect_url":"https://webhook.site/9d0b00ba-9a69-44fa-a43d-a82c33c36fdc",
                "payment_options":"card",
                "meta":{
                    "consumer_id":23,
                    "consumer_mac":"92a3-912ba-1192a"
                },
                "customer":{
                    "email":email,
                    "phonenumber":phone,
                    "name":full_name,
                },
                "customizations":{
                    "title":"Supa Electronics Store",
                    "description":"Best store in town",
                    "logo":"https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg"
                }
            }
    endpoint = 'https://api.flutterwave.com/v3/payments'            
    get_response = requests.post(endpoint, headers=hed, json='data') 
    # return Repons(get_response.json())
    print(get_response.json())

    # url = ' https://api.flutterwave.com/v3/payments'
    # response = requests.post(url, json=data, headers=hed)
    # response=response.json()
    # link=response['data']['link']
    # return link

@require_http_methods(['GET', 'POST'])
def payment_response(request):
    status=request.GET.get('status', None)
    tx_ref=request.GET.get('tx_ref', None)
    print(status)
    print(tx_ref)
    return HttpResponse('Finished')    

# @login_required(login_url='/login/')
# def checkout(request):
#     cartcheck = CartModel.objects.filter(user=request.user, order=False) 
#     amount = '0'
#     for i in cartcheck:
#         # print(float(amount) + (float(i.product.price) * float(i.quantity) ))
#         amount = float(amount) + (float(i.product.price) * float(i.quantity) )       
#     payment_form = CheckoutForm(request.POST) 
#     if request.method=='POST':
#         if payment_form.is_valid():
#             full_name = payment_form.cleaned_data['full_name']
#             email = payment_form.cleaned_data['email']
#             country = payment_form.cleaned_data['country']
#             address = payment_form.cleaned_data['address_1']
#             address2 = payment_form.cleaned_data['address_2']
#             city = payment_form.cleaned_data['city']
#             zipcode = payment_form.cleaned_data['zipcode']
#             phone = payment_form.cleaned_data['phone']
#             payment_form = ShippingAddress(
#                 full_name,email,
#                 country,address,
#                 address2,city,
#                 zipcode,phone
#             )
#         else:
#            payment_form.save()
#     context = {'cartcheck':cartcheck, 'amount':amount}       
#     return render(request, 'checkout.html', context, {'payment_form':payment_form})



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
