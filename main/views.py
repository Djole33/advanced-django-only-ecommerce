from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Product, Category, Review, Cart, CartItem
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
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        cart = 0


    return render(request, 'main/base.html', {'cart': cart, 'categories': categories})

def index(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        cart = 0

    products = Product.objects.all()
    categories = Category.objects.all()

    return render(request, 'main/index.html', {'cart': cart, 'products': products, 'categories': categories, 'MEDIA_URL': settings.MEDIA_URL})

def shop(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        cart = 0

    products = Product.objects.all()
    paginator = Paginator(products, 2)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    next_page = products.paginator.num_pages
    page_list = []

    for page_num in range(next_page):
        page_num += 1
        page_list.append(page_num)

    return render(request, 'main/shop.html', {'cart': cart, 'products': products, 'page_list': page_list, 'MEDIA_URL': settings.MEDIA_URL})

def detail(request, pk):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        cart = 0

    product = Product.objects.get(id=pk)
    reviews = Review.objects.filter(product=product.id)

    return render(request, 'main/detail.html', {'cart': cart, 'product': product, 'reviews':reviews, 'URL': settings.MEDIA_URL})

def category_page(request, name):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        cart = 0

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

    return render(request, 'main/category_page.html', {'cart': cart, 'category': category, 'products': products, 'page_list': page_list, 'MEDIA_URL': settings.MEDIA_URL})

def cart(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            total_price = sum(item.total_price() for item in cart_items)
            taxes_price = total_price + (total_price * 20) / 100

            cart.price = total_price
            cart.save()

            return render(request, 'main/cart.html', {'cart_items': cart_items, 'cart': cart, 'total_price': total_price, 'taxes_price': taxes_price, 'MEDIA_URL': settings.MEDIA_URL})

        except Cart.DoesNotExist:
            messages.error(request, "Add something to cart first.")
            return redirect('index')
        
    else:
        messages.error(request, "Log in first.")
        return redirect('index')
    
def add_cart(request, pk):
    add_product = Product.objects.get(id=pk)
    try:
        if request.user:
            cart = Cart.objects.get(user=request.user)
            if not cart.cart_items.filter(product=add_product).exists():
                cart_items = CartItem.objects.create(cart=cart, product=add_product, quantity=1)
                cart.save()
                messages.success(request, "Product added to cart successfully.")
                return redirect('cart')
            else:
                messages.error(request, "Product already in the cart.")
                return redirect('index')
        else:
            messages.error(request, "Log in first.")
            return redirect('cart')
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
        return redirect('cart')
    
def delete_cart(request, pk):
    cart_item = CartItem.objects.get(id=pk)
    if request.method == "POST":
        cart_item.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('cart')

def add_quantity(request, pk):
    cart_item = CartItem.objects.get(id=pk)

    if request.method == "POST":
        if cart_item.quantity < 10:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, "Item quantity increased successfully.")
            return redirect('cart')
        else:
            messages.error(request, "Maximum quantity reached.")
            return redirect('cart')

def decrease_quantity(request, pk):
    cart_item = CartItem.objects.get(id=pk)

    if request.method == "POST":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            messages.success(request, "Item quantity decreased successfully.")
            return redirect('cart')
        else:
            messages.error(request, "Minimal quantity reached.")
            return redirect('cart')

def checkout(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        cart = 0

    return render(request, 'main/checkout.html', {'cart': cart, 'MEDIA_URL': settings.MEDIA_URL})

def contact(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        cart = 0

    return render(request, 'main/contact.html', {'cart': cart, 'MEDIA_URL': settings.MEDIA_URL})

def register_user(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        cart = 0

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
    return render(request, 'main/register_user.html', {'cart': cart, 'form': form})

def login_user(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        cart = 0

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

    return render(request, 'main/login_user.html', {'cart': cart})

def logout_user(request):
    logout(request)
    messages.success(request, ('You have been successfully logged out!'))
    return redirect('index')
