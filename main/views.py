from django.shortcuts import render, redirect
from django.conf import settings
from .models import Product, Category
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from .forms import SignUpForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('You have been successfully registered!'))
            return redirect('index')
        else:
            messages.error(request, ('Error registering!'))
            return redirect('register_user')
    return render(request, 'main/register_user.html', {'form': form})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, ('You have been successfully logged in!'))
            return redirect('index')
        else:
            messages.error(request, ('Error logging in!'))
            return redirect('login_user')

    return render(request, 'main/login_user.html')

def logout_user(request):
    logout(request)
    messages.success(request, ('You have been successfully logged out!'))
    return redirect('index')
