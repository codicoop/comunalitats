from django.urls import path
from .views import CourseDetailView, EnrollActivityView, MyCoursesListView, OptoutActivityView, ActivityDetailView
from .utils import get_courses_list_view_class
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        'activities/my_activities',
        login_required(MyCoursesListView.as_view()),
        name='my_activities'
    ),
    path(
        'program/<slug>',
        CourseDetailView.as_view(),
        name='course'
    ),
    path('program/', get_courses_list_view_class().as_view(), name='courses'),
    path('enroll/', EnrollActivityView.as_view(), name='enroll_course'),
    path(
        'activities/<id>/activity_optout',
        OptoutActivityView.as_view(),
        name='activity_optout'
    ),
    path(
        'activities/<pk>/instructions',
        login_required(ActivityDetailView.as_view()),
        name='activity'
    ),
]
