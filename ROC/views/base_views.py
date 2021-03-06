from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import auth
from ROC.models import User, UserInfo
# Create your views here.


def index(request):
    return redirect('course_all')


def login(request):
    return render(request, 'base/login.html')


@require_POST
def authenticate(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(request, username=username, password=password)
    if not user:
        return redirect('login')
    auth.login(request, user)
    return redirect('course_all')


def signup(request):
    return render(request, 'base/signup.html')


@require_POST
def signup_submit(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    try:
        user = User.objects.create_user(username=username, password=password, email=email)
        UserInfo.objects.create(user=user, nickname=username)
        return redirect('login')
    except:
        return redirect('signup')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')
