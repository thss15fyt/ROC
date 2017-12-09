from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from ROC.models import *
from ROC.views.utils import item_paginator


def course_all(request):
    courses_all = Course.objects.all()
    courses = item_paginator(request, courses_all)

    return render(request, 'course_comment/course_all.html', {'courses': courses})


def course_search(request):
    keyword = request.GET.get('keyword')
    courses_result = Course.objects.filter(name__contains=keyword)
    courses = item_paginator(request, courses_result)

    return render(request, 'course_comment/course_search.html',
                  {'courses': courses, 'keyword': keyword})


def course_detail(request):
    course_id = request.GET.get('id')
    course = get_object_or_404(Course, pk=course_id)
    comments = course.coursecomment_set.all()
    return render(request, 'course_comment/course_detail.html',
                  {'course': course, 'comments': comments})


@login_required
@require_POST
def create_comment(request):
    course_id = request.GET.get('id')
    course = get_object_or_404(Course, pk=course_id)
    comment_content = request.POST.get('comment')
    if len(comment_content) > 0:
        CourseComment.objects.create(course=course, content=comment_content, author=request.user)

    return redirect('%s?id=%s' % (reverse('course_detail'), course_id))
