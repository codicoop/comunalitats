#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cc_users.views import LoginView


class CoopolisLoginView(LoginView):
    def get_success_url(self):
        url = self.request.GET.get('next')
        if url:
            return url + '?' + self.request.GET.urlencode()
        return super().get_success_url()
