#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from .views import CoursesListView, CourseDetailView, EnrollCourseView, MyCoursesListView


urlpatterns = [
    path('', CoursesListView.as_view(), name='courses'),
    path('/<slug>', CourseDetailView.as_view(), name='course'),
    path('my_courses', MyCoursesListView.as_view(), name='my_courses'),
    path('/<slug:slug>/enroll', EnrollCourseView.as_view(), name='enroll_course')
]
