from django import template
from index.models import CartModel,Wishlist

register = template.Library()

@register.filter()
def cart_item_count(user):
    if user.is_authenticated:
        qs = CartModel.objects.filter(user=user,order=False)
        if qs.exists():
            return qs.count() 
    return 0    

@register.filter()
def wish_count(user):
    if user.is_authenticated:
        lister = Wishlist.objects.filter(user=user)
        if lister.exists():
            return lister.count()
    return 0     