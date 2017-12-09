from django.shortcuts import render, redirect


def user_info(request):
    return render(request, 'user_center/user_info.html')