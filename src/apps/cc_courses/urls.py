from django.urls import path
from .views import CourseDetailView, EnrollActivityView, MyCoursesListView, OptoutActivityView, ActivityDetailView
from django.contrib.auth.decorators import login_required

from ..coopolis.views import CoopolisCoursesListView

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
    path('program/', CoopolisCoursesListView.as_view(), name='courses'),
    path('enroll/', EnrollActivityView.as_view(), name='enroll_course'),
    path(
        'activities/<id>/activity_optout',
        OptoutActivityView.as_view(),
        name='activity_optout'
    ),
    path(
        'activities/<uuid:slug>/instructions',
        login_required(ActivityDetailView.as_view()),
        name='activity'
    ),
]
