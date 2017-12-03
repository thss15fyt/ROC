from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CoursePost(models.Model):
    name = models.CharField(max_length=128)
    teacher = models.CharField(max_length=20)
    apartment = models.CharField(max_length=128)


class CourseComment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User)
    create_at = models.DateTimeField(auto_now_add=True)


class ExchangePost(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    author = models.ForeignKey(User)


class ExchangeComment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User)
    create_at = models.DateTimeField(auto_now_add=True)

