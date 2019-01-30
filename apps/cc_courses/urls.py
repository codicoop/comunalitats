#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from .views import CourseDetailView, EnrollActivityView, MyCoursesListView, OptoutActivityView
from .utils import get_courses_list_view_class


urlpatterns = [
    path('activities/my_activities', MyCoursesListView.as_view(), name='my_activities'),
    path('program/<slug>', CourseDetailView.as_view(), name='course'),
    path('program/', get_courses_list_view_class().as_view(), name='courses'),
    path('<id>/enroll', EnrollActivityView.as_view(), name='enroll_course'),
    path('activities/<id>/activity_optout', OptoutActivityView.as_view(), name='activity_optout')
]
