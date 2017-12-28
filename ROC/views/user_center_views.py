from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from ROC_project import settings
from ROC.models import Course, CourseComment
from ROC.views.utils import item_paginator
import time

@login_required
def user_info(request):
    return render(request, 'user_center/user_info.html')


@login_required
@require_POST
def user_info_submit(request):
    user = request.user
    user.email = request.POST.get('email')
    user.userinfo.nickname = request.POST.get('nickname')

    file = request.FILES.get('avatar')
    if file:
        new_name = 'avatar' + '/' + request.user.username + time.strftime('%Y%m%d%H%M%S') + '.' + file.name.split('.')[-1]
        save_path = settings.MEDIA_ROOT + '/' + new_name
        save_file = open(save_path, 'w+b')
        if file.multiple_chunks():
            for chunk in file.chunks():
                save_file.write(chunk)
        else:
            save_file.write(file.read())
        save_file.close()
        user.userinfo.avatar_url = settings.get_url(settings.MEDIA_URL + new_name)

    user.save()
    user.userinfo.save()

    return redirect('user_info')


@login_required
def user_courses(request):
    star_course_all = request.user.star_courses.exclude(status=Course.DELETED).all()
    star_courses = item_paginator(request, star_course_all)
    return render(request, 'user_center/user_courses.html',
                  {'star_courses': star_courses})


@login_required
def user_comments(request):
    comment_all = CourseComment.objects.filter(author=request.user)
    comments = item_paginator(request, comment_all)
    return render(request, 'user_center/user_comments.html',
                  {'comments': comments, 'length': len(comments)})
