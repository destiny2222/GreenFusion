from os import name
from django.urls import path
from . import views
from acc_user.views import logout_View,LoginView,RegisterView,profileView,dashboard_view,other_user_profile

app_name = 'index'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView, name="about"),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('login/', LoginView, name='login'),
    path('logout/', logout_View, name='logout'),
    path('profile', profileView, name='profile' ),
    path('register/', RegisterView, name='register'),
    path('dashboard/', dashboard_view, name='dashboard' ),
    path('other_user/<slug>/', other_user_profile, name='other_user'),

    path('search', views.search, name="search"),
    path('product/<slug:slug>/', views.store, name="product"),
    path('addcart/<int:id>/', views.cart, name="addcart"),
    path('cart/', views.cart_details, name="cart"),
    path('pluscart/<int:id>/', views.cart_increment , name="pluscart"),
    path('minucart/<int:id>/', views.cart_decrement , name="removecart"),
    path('deletecart/<int:id>/', views.cart_delete , name="deletecart"),
    
    # wishlist urls
    path('wish/', views.wish_details, name="wish"),
    path('addwish/<int:id>/', views.WishlistView, name="addwish"),
    path('pluswish/<slug>/', views.wishlist_increment , name="pluswish"),
    path('minuwish/<slug>/', views.wishlist_decrement , name="removewish"),
    path('deletewish/<int:slug>/', views.wish_delete , name="deletewish"),
    
    path('blog/', views.BlogView, name='blog'),
    path('contact/', views.ContactView, name='contact'),
    path('blogdetails/<slug:slug>', views.BlogDetails, name='blogdetails'),
    path('checkout/', views.checkout, name="checkout"),
    path('category/<slug:slug>', views.getCategoryItems, name='itemcategory'),
    path('project/', views.projectView.as_view(), name='project')
]