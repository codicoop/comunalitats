#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from .views import CourseDetailView, EnrollCourseView, MyCoursesListView
from .utils import get_courses_list_view_class


urlpatterns = [
    path('', get_courses_list_view_class().as_view(), name='courses'),
    path('my_courses', MyCoursesListView.as_view(), name='my_courses'),
    path('<slug>', CourseDetailView.as_view(), name='course'),
    path('<slug:slug>/enroll', EnrollCourseView.as_view(), name='enroll_course')
]
