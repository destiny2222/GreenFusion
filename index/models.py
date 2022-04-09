from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
# Create your models here.

# user = get_user_model()

class CustomUser(AbstractUser):
    # fullname = models.CharField(max_length=50, default='')
    # first_name = models.CharField(max_length=50, default='')
    # last_name = models.CharField(max_length=50, default='')
    # username = models.CharField(max_length=20,unique=True)
    phonenumber = models.CharField(max_length=15, default='', blank=True, null=True)

    def _str_(self):
        return self.fullname

class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.FileField()
    def __str__(self):
        return self.name      

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False,null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class CartModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)    
    quantity = models.IntegerField()
    price = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order = models.BooleanField(default=False)

    def __str__(self):
        return self.user


class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # created = models.DateTimeField(auto_now_add=True)
    # quantity = models.SmallIntegerField(default=1)


    def __str__(self):
        return self.product          

class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
        
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return self.product
            


class ShippingAddress(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=60)
    # last_name = models.CharField(max_length=60)
    address = models.CharField(max_length=200, null=False)
    address2 = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    country = CountryField(multiple=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    email = models.EmailField()
    phone = models.CharField(max_length=11, null=False)
    default = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.customer

    class Meta:
        ordering = ('-customer', )

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())    


class Blog(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=100)
    post_date = models.DateTimeField(blank=True, null=True)
    body = RichTextField()    
    picture = models.FileField()    


    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    number = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()        

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=200)
    # body = RichTextField()
    image = models.FileField()

    def __str__(self):
        return self.name