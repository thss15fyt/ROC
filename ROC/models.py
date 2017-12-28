# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ROC_project import settings

# Create your models here.


class UserInfo(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=64)
    avatar_url = models.CharField(max_length=256, default=settings.get_url('static/img/default_avatar.jpg'))

    user_type = models.IntegerField(default=1)
    NORMAL = 1
    ADMIN = 2


class Apartment(models.Model):
    name = models.CharField(max_length=64)


class Course(models.Model):
    # info
    name = models.CharField(max_length=128)
    teacher = models.CharField(max_length=64)
    apartment = models.ForeignKey(Apartment)
    course_id = models.CharField(max_length=32)
    credit = models.PositiveIntegerField()
    undergraduate_capacity = models.PositiveIntegerField()
    postgraduate_capacity = models.PositiveIntegerField()
    explain = models.CharField(max_length=256)
    feature = models.CharField(max_length=256)  # TODO: split feature into models
    grade = models.CharField(max_length=64)
    second_choose_flag = models.BooleanField()  # 是否二级选课
    retake_flag = models.BooleanField()     # 重修是否占容量
    choose_restrict_flag = models.BooleanField()    # 是否选课时限制
    group = models.CharField(max_length=64)     # 本科文化素质课组

    # foreign key
    star_user = models.ManyToManyField(User, related_name='star_courses')

    status = models.IntegerField(default=1)
    PUBLISHED = 1
    DELETED = -1


class Class(models.Model):
    course = models.ForeignKey(Course)
    class_id = models.CharField(max_length=32)
    time = models.CharField(max_length=256)


class CourseComment(models.Model):
    course = models.ForeignKey(Course)
    content = models.TextField()
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(default=timezone.now)
    anonymous = models.BooleanField(default=False)
    status = models.IntegerField(default=1)
    PUBLISHED = 1
    DELETED = -1
