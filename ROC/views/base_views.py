from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from ROC.models import User
# Create your views here.


def index(request):
    return render(request, 'course_comment/course_list.html')


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
    return render(request, 'base/signup.html')


def signup_submit(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    try:
        User.objects.create_user(username=username, password=password, email=email)
        return redirect('login')
    except:
        return redirect('signup')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')
