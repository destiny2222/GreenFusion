from django.contrib import admin
from .models import *
class BlogAdmin(admin.ModelAdmin):
    	exclude = ['slug']
class CategoryAdmin(admin.ModelAdmin):
    	exclude = ['slug']		
class ProductAdmin(admin.ModelAdmin):
    	exclude = ['slug']		
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
# admin.site.register(ShippingAddress)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Project, ProductAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Wishlist)