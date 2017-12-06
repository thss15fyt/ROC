from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Apartment(models.Model):
    name = models.CharField(max_length=64)


class Course(models.Model):
    name = models.CharField(max_length=128)
    teacher = models.CharField(max_length=20)
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

    status = models.IntegerField(default=1)
    PUBLISHED = 1
    DELETED = -1


class Class(models.Model):
    course = models.ForeignKey(Course)
    class_id = models.CharField(max_length=32)
    time = models.CharField(max_length=256)  # TODO: split class time into models


class CourseComment(models.Model):
    course = models.ForeignKey(Course)
    content = models.TextField()
    author = models.ForeignKey(User)
    create_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)
    PUBLISHED = 1
    DELETED = -1
