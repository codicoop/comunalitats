#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from .views import CoursesListView, CourseDetailView, EnrollCourseView


urlpatterns = [
    path('', CoursesListView.as_view(), name='courses'),
    path('/<slug>', CourseDetailView.as_view(), name='course'),
    path('my_courses', CoursesListView.as_view(), {'mine': True}, name='my_courses'),
    path('/<slug>/enroll', EnrollCourseView.as_view(), name='enroll_course')
]
