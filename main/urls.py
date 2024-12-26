from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name="index"),
   path('home/', views.index, name="index"),
   path('shop/', views.shop, name="shop"),
   path('detail/<int:pk>/', views.detail, name="detail"),
   path('category/<str:name>/', views.category_page, name="category_page"),
   path('cart/', views.cart, name="cart"),
   path('checkout/', views.checkout, name="checkout"),
   path('contact/', views.contact, name="contact"),
]
