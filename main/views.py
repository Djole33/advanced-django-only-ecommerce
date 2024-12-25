from django.shortcuts import render
from django.conf import settings
from .models import *
from django.shortcuts import get_object_or_404

# Create your views here.

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()


    return render(request, 'main/index.html', {'products': products, 'categories': categories, 'MEDIA_URL': settings.MEDIA_URL})

def shop(request):
    return render(request, 'main/shop.html', {'MEDIA_URL': settings.MEDIA_URL})

def detail(request):
    return render(request, 'main/detail.html', {'MEDIA_URL': settings.MEDIA_URL})

def cart(request):
    return render(request, 'main/cart.html', {'MEDIA_URL': settings.MEDIA_URL})

def checkout(request):
    return render(request, 'main/checkout.html', {'MEDIA_URL': settings.MEDIA_URL})

def contact(request):
    return render(request, 'main/contact.html', {'MEDIA_URL': settings.MEDIA_URL})
