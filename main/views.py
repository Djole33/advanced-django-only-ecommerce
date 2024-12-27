from django.shortcuts import render
from django.conf import settings
from .models import Product, Category
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator

# Create your views here.

def base(request):
    categories = Category.objects.all()

    return render(request, 'main/base.html', {'categories': categories})

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()


    return render(request, 'main/index.html', {'products': products, 'categories': categories, 'MEDIA_URL': settings.MEDIA_URL})

def shop(request):
    products = Product.objects.all()
    paginator = Paginator(products, 2)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    next_page = products.paginator.num_pages
    page_list = []

    for page_num in range(next_page):
        page_num += 1
        page_list.append(page_num)

    return render(request, 'main/shop.html', {'products': products, 'page_list': page_list, 'MEDIA_URL': settings.MEDIA_URL})

def detail(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'main/detail.html', {'product': product, 'MEDIA_URL': settings.MEDIA_URL})

def category_page(request, name):
    category = Category.objects.get(name=name.capitalize())
    products = Product.objects.filter(category=category.id)

    paginator = Paginator(products, 1)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    next_page = products.paginator.num_pages
    page_list = []

    for page_num in range(next_page):
        page_num += 1
        page_list.append(page_num)

    return render(request, 'main/category_page.html', {'category': category, 'products': products, 'page_list': page_list, 'MEDIA_URL': settings.MEDIA_URL})

def cart(request):
    return render(request, 'main/cart.html', {'MEDIA_URL': settings.MEDIA_URL})

def checkout(request):
    return render(request, 'main/checkout.html', {'MEDIA_URL': settings.MEDIA_URL})

def contact(request):
    return render(request, 'main/contact.html', {'MEDIA_URL': settings.MEDIA_URL})
