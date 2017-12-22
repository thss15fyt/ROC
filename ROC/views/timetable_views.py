from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from ROC.views.utils import item_paginator
from ROC.models import *
import json

def choose_course(request):
    course_all = Course.objects.all()
    courses = item_paginator(request, course_all)
    star_courses = request.user.star_courses.all()
    return render(request, 'timetable/course_choose.html',
                  {'courses': courses, 'star_courses': star_courses, 'choosen_courses': []})


def choose_course_detail(request):
    id = request.GET.get('id')
    course = get_object_or_404(Course, id=id)
    response_data = {}
    response_data['name'] = course.name
    response_data['teacher'] = course.teacher
    response_data['apartment'] = course.apartment.name
    return HttpResponse(content=json.dumps(response_data), content_type="application/json")
