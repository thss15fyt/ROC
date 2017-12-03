from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
# Create your views here.


def index(request):
    return render(request, 'base/base.html')


def login(request):
    return render(request, 'base/login.html')


def authenticate(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(request, username=username, password=password)
    if not user:
        return redirect('login')
    auth.login(request, user)
    return redirect('index')


def signup(request):
    pass


@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')
