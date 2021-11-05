from io import StringIO

from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View

from apps.coopolis.views import LoginSignupContainerView


class HomeView(LoginSignupContainerView):
    template_name = "home.html"


class StagesMigrationReportView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return HttpResponse('Access denied')
        with StringIO() as out:
            call_command('stage_sessions_report', stdout=out)
            report = out.getvalue()
        return HttpResponse(report)
