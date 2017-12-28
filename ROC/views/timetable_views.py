from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from ROC.views.utils import item_paginator
from ROC.models import *
from ROC.views.utils import string_time_to_array, form_core
import json


def choose_course(request):
    course_all = Course.objects.all()
    courses = item_paginator(request, course_all)
    if request.user.is_authenticated:
        star_courses = request.user.star_courses.all()
    else:
        star_courses = []
    return render(request, 'timetable/course_choose.html',
                  {'courses': courses, 'star_courses': star_courses, 'choosen_courses': []})


def choose_course_search(request):
    keyword = request.GET.get('keyword')
    courses = Course.objects.filter(name__contains=keyword)
    return render(request, 'timetable/search_result.html',
                  {'courses': courses})


def choose_course_detail(request):
    id = request.GET.get('id')
    course = get_object_or_404(Course, id=id)
    response_data = {}
    response_data['name'] = course.name
    response_data['teacher'] = course.teacher
    response_data['apartment'] = course.apartment.name
    return HttpResponse(content=json.dumps(response_data), content_type="application/json")


def timetable_result(request):
    ids = request.POST.get('ids')
    id_set = ids[:-1].split(',')
    all_courses = {}
    for id in id_set:
        course = get_object_or_404(Course, id=id)
        times = []
        for simple_class in course.class_set.all():
            times.append(simple_class.time)
        all_courses[course.name] = times
    results = form_core(all_courses)
    return render(request, 'timetable/timetable_result.html',
                  {'results': results})

