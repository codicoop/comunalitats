#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.forms import DateTimeInput
from django.forms import DateInput
from django.forms import TimeInput


class XDSoftDateTimePickerInput(DateTimeInput):
    template_name = 'widgets/xdsoft_datetimepicker.html'


class XDSoftDatePickerInput(DateInput):
    template_name = 'widgets/xdsoft_datepicker.html'


class XDSoftTimePickerInput(TimeInput):
    template_name = 'widgets/xdsoft_timepicker.html'
