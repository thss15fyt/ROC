from django.conf.urls import url
from ROC.views import base_views

urlpatterns = [
    # base
    url(r'^$', base_views.index, name='index'),
    url(r'^login$', base_views.login, name='login'),
    url(r'^authenticate', base_views.authenticate, name='authenticate'),
    url(r'^signup$', base_views.signup, name='signup'),
    url(r'^logout$', base_views.logout, name='logout'),

    # user center

    # course comment

    # exchange course

    # timetable

]