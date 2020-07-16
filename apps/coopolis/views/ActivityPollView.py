#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic import CreateView

from cc_courses.models import Activity
from coopolis.models import ActivityPoll
from coopolis.forms import ActivityPollForm


class ActivityPollView(CreateView):
    model = ActivityPoll
    form_class = ActivityPollForm
    template_name = 'activity_poll.html'
    activity_obj = None

    def get_success_url(self):
        return reverse('my_activities')

    def get(self, request, *args, **kwargs):
        self.activity_obj = self.get_activity_object()
        ret = super(ActivityPollView, self).get(request, *args, **kwargs)
        if not self.access_granted():
            return HttpResponseRedirect(reverse('my_activities'))
        return ret

    def post(self, request, *args, **kwargs):
        self.activity_obj = self.get_activity_object()

        if not self.access_granted():
            return HttpResponseRedirect(reverse('my_activities'))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        new_poll = form.save(commit=False)
        new_poll.activity = self.activity_obj
        new_poll.user = self.request.user
        new_poll.save()
        messages.success(self.request,
                         f"Enquesta de valoració per {self.activity_obj} enviada correctament. Moltes gràcies!")
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        ctx = super(ActivityPollView, self).get_context_data(**kwargs)
        ctx['activity'] = self.activity_obj
        ctx['already_answered'] = False
        ctx['fieldsets'] = ctx['form'].get_grouped_fields()
        # Amb getattr(object, attribute_name) hauria de poder accedir als form.field_name)

        if self.activity_obj.polls.filter(user=self.request.user).count():
            ctx['already_answered'] = True
        return ctx

    def access_granted(self):
        if not self.activity_obj.poll_access_allowed():
            raise Http404(f"L'Activity {self.activity_obj} no té l'enquesta de valoració oberta en aquests moments.")

        if self.activity_obj.confirmed_enrollments.filter(user=self.request.user).count() < 1:
            raise Http404(
                f"No pots accedir a l'enquesta de valoració de la sessió {self.activity_obj} "
                f"perquè no hi estàs inscrit/a.")

        return True

    def get_activity_object(self):
        pk = self.kwargs.get('pk')
        try:
            obj = Activity.objects.get(id=pk)
        except Activity.DoesNotExist:
            raise Http404(f"No existeix cap Activity amb la id {pk}.")
        return obj

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # print(form.fields)
        return form
