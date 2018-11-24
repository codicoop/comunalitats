#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cc_courses.views import CoursesListView
from constance import config


class CoopolisCoursesListView(CoursesListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['introduction_text'] = config.INTRODUCTION_TEXT
        return context
