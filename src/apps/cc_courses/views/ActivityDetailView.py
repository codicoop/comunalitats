from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView
from apps.cc_courses.models import Activity


class ActivityDetailView(DetailView):
    model = Activity
    template_name = 'activity.html'
    # Es va afegir el camp uuid però la PK segueix sent ID. El nou camp uuid és
    # per generar enllaços a la fitxa i a l'enquesta, però internament les
    # relacions estan construides sobre el camp ID. No es va fer una migració
    # del camp, de manera que el nou camp uuid a tots els efectes és equivalent
    # a un camp slug.
    slug_field = "uuid"

    def get(self, request, *args, **kwargs):
        ret = super(ActivityDetailView, self).get(request, *args, **kwargs)
        if (
            (
                self.object.instructions
                or self.object.videocall_url
                or len(self.object.resources.all())
            )
            and (
                self.object.user_is_confirmed(request.user)
                or request.user.is_staff
            )
        ):
            return ret
        return HttpResponseRedirect(reverse('my_activities'))
