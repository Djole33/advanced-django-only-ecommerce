from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name="index"),
   path('home/', views.index, name="index"),
   path('shop/', views.shop, name="shop"),
   path('detail/<int:pk>/', views.detail, name="detail"),
   path('category/<str:name>/', views.category_page, name="category_page"),
   path('cart/', views.cart, name="cart"),
   path('add_cart/<int:pk>/', views.add_cart, name="add_cart"),
   path('delete_cart/<int:pk>/', views.delete_cart, name="delete_cart"),
   path('checkout/', views.checkout, name="checkout"),
   path('contact/', views.contact, name="contact"),
   path('register_user/', views.register_user, name="register_user"),
   path('login_user/', views.login_user, name="login_user"),
   path('logout_user/', views.logout_user, name="logout_user"),
]
