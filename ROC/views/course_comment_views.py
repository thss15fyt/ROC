from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from ROC.models import *
from ROC.views.utils import item_paginator


def course_all(request):
    courses_all = Course.objects.exclude(status=Course.DELETED).all()
    courses = item_paginator(request, courses_all)

    return render(request, 'course_comment/course_all.html',
                  {'courses': courses})


def course_search(request):
    keyword = request.GET.get('keyword')
    courses_result = Course.objects.exclude(status=Course.DELETED).filter(name__contains=keyword)
    courses = item_paginator(request, courses_result)

    return render(request, 'course_comment/course_search.html',
                  {'courses': courses, 'keyword': keyword})


def course_detail(request):
    course_id = request.GET.get('id')
    course = get_object_or_404(Course, pk=course_id, status=Course.PUBLISHED)
    comments = course.coursecomment_set.all()
    return render(request, 'course_comment/course_detail.html',
                  {'course': course, 'comments': comments,
                   'stared': (request.user in course.star_user.all())})


@login_required
@require_POST
def create_comment(request):
    course_id = request.GET.get('id')
    course = get_object_or_404(Course, id=course_id, status=Course.PUBLISHED)
    comment_content = request.POST.get('comment')
    if len(comment_content) > 0:
        CourseComment.objects.create(course=course, content=comment_content, author=request.user,
                                     anonymous=(request.POST.get('anonymous') == 'on'))

    return redirect('%s?id=%s' % (reverse('course_detail'), course_id))


@login_required
@require_POST
def star_course(request):
    course_id = request.POST.get('id')
    star = request.POST.get('star')
    course = get_object_or_404(Course, id=course_id, status=Course.PUBLISHED)
    response_content = '0'
    if star == '1' and request.user not in course.star_user.all():
        course.star_user.add(request.user)
        response_content = '1'
    elif star == '0' and request.user in course.star_user.all():
        course.star_user.remove(request.user)
        response_content = '1'
    course.save()
    return HttpResponse(content=response_content)
