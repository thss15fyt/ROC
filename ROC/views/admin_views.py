# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from ROC.models import *
from ROC.views.utils import item_paginator


@login_required
def add_courses(request):
    if request.user.userinfo.user_type != UserInfo.ADMIN:
        return redirect('course_all')
    return render(request, 'admin/add_courses.html')


@login_required
def add_courses_submit(request):
    if request.user.userinfo.user_type != UserInfo.ADMIN:
        return redirect('course_all')

    file = request.FILES.get('courses_file')
    for line in file:
        info_line = line.decode('utf-8')
        info = info_line.split('$')
        for i in range(len(info)):
            if info[i] == '#':
                info[i] = ''

        # get or create apartment
        try:
            apartment = Apartment.objects.get(name=info[0])
        except ObjectDoesNotExist:
            apartment = Apartment.objects.create(name=info[0])
            # print("Create apartment: %s" % (info[0]))

        # add class to course or create course
        try:
            course = Course.objects.get(course_id=info[1], name=info[3], teacher=info[5])
        except ObjectDoesNotExist:
            course = Course.objects.create(
                name=info[3],
                teacher=info[5],
                apartment=apartment,
                course_id=info[1],
                credit=int(info[4]),
                undergraduate_capacity=int(info[6]),
                postgraduate_capacity=int(info[7]),
                explain=info[9],
                feature=info[10],
                grade=info[11],
                second_choose_flag=(info[12] == '是'),
                retake_flag=(info[14] == '是'),
                choose_restrict_flag=(info[15] == '是'),
                group=info[16],
            )
            # print("Create course: %s" % (info[3]))

        # create class if not exist
        try:
            Class.objects.get(course=course, time=info[8])
        except ObjectDoesNotExist:
            Class.objects.create(
                course=course,
                class_id=info[2],
                time=info[8],
            )

    return render(request, 'admin/add_courses.html')


@login_required
def manage_courses(request):
    if request.user.userinfo.user_type != UserInfo.ADMIN:
        return redirect('course_all')

    course_all = Course.objects.exclude(status=Course.DELETED).all()
    courses = item_paginator(request, course_all)

    return render(request, 'admin/manage_courses.html',
                  {'courses': courses})


@login_required
@require_POST
def remove_course(request):
    if request.user.userinfo.user_type != UserInfo.ADMIN:
        return redirect('course_all')

    course = get_object_or_404(Course, id=request.GET.get('id'))
    course.status = Course.DELETED
    course.save()

    return redirect('manage_courses')