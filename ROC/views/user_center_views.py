from django.shortcuts import render, redirect


def user_info(request):
    return render(request, 'user_center/user_info.html')


def user_courses(request):
    return render(request, 'user_center/user_courses.html')