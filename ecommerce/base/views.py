from django.shortcuts import render, redirect
from .models import Product , Categories
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms


# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def about_us(request):
    return render(request, 'aboutus.html')


def login_user(request):
    if request.user.is_authenticated:  # if user is logged in user gets thrown to home page.
        return redirect(home)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in...")
            return redirect('home')
        else:
            messages.success(request, "There was an error, try again...")
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')


def register_user(request):
    if request.user.is_authenticated:  # if user is logged in user gets thrown to home page.
        return redirect(home)
    form = SignUpForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have been registered...")
            return redirect('home')
        else:
            messages.success(request, "There was an error, try again...")
            return redirect('register')
    return render(request, 'register.html', {'form': form})


def product(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product.html', {'product': product})


def category(request, cname):
    cname = cname.replace('-', ' ')  # Replace '-' with ' ' and title the string.
    try:
        categories = Categories.objects.get(name=cname)  # Get the category object.
        products = Product.objects.filter(category=categories)
        return render(request, 'category.html', {'products': products, 'categories': categories})
    except :
        messages.success(request, "Sorry, that category does not exist.")
        return redirect('home')



