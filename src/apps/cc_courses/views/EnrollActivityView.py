from django.views import generic
from django.shortcuts import reverse

from apps.cc_courses.models import Activity, ActivityEnrolled


class EnrollActivityView(generic.RedirectView):

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous or not request.POST:
            self.url = reverse('loginsignup')
        else:
            activity = Activity.objects.get(id=request.POST['activity_id'])
            enrollment = ActivityEnrolled(
                user=request.user,
                activity=activity,
                user_comments=request.POST['user_comments'],
            )
            self.url = activity.course.absolute_url
            enrollment.save()
            if enrollment.waiting_list:
                enrollment.send_waiting_list_email()
            else:
                enrollment.send_confirmation_email()

        return super().get(request, *args, **kwargs)
