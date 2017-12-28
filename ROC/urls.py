from django.conf.urls import url
from ROC.views import base_views, admin_views, course_comment_views, user_center_views, timetable_views
from django.conf.urls.static import static
from ROC_project import settings

urlpatterns = [
    # base
    url(r'^$', base_views.index, name='index'),
    url(r'^login$', base_views.login, name='login'),
    url(r'^authenticate$', base_views.authenticate, name='authenticate'),
    url(r'^signup$', base_views.signup, name='signup'),
    url(r'^signup_submit$', base_views.signup_submit, name='signup_submit'),
    url(r'^logout$', base_views.logout, name='logout'),

    # user center
    url(r'user_info$', user_center_views.user_info, name='user_info'),
    url(r'user_info/submit$', user_center_views.user_info_submit, name='user_info_submit'),
    url(r'user_courses$', user_center_views.user_courses, name='user_courses'),
    url(r'user_comments$', user_center_views.user_comments, name='user_comments'),

    # course comment
    url(r'^course_all', course_comment_views.course_all, name='course_all'),
    url(r'^course_search', course_comment_views.course_search, name='course_search'),
    url(r'^course_detail', course_comment_views.course_detail, name='course_detail'),
    url(r'^create_comment', course_comment_views.create_comment, name='create_comment'),
    url(r'^star_course', course_comment_views.star_course, name='star_course'),

    # timetable
    url(r'^choose_course$', timetable_views.choose_course, name='choose_course'),
    url(r'^choose_course_search$', timetable_views.choose_course_search, name='choose_course_search'),
    url(r'^choose_course_detail', timetable_views.choose_course_detail, name='choose_course_detail'),
    url(r'^timetable_result$', timetable_views.timetable_result, name='timetable_result'),

    # admin
    url('^add_courses$', admin_views.add_courses, name='add_courses'),
    url('^add_courses_submit$', admin_views.add_courses_submit, name='add_courses_submit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)