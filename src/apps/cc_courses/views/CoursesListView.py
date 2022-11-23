
from django.views import generic
from apps.cc_courses.models import Course
from django.utils import timezone


class CoursesListView(generic.ListView):
    model = Course
    template_name = 'courses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['future_courses'] = (
            Course.objects.filter(
                activities__date_start__gte=timezone.now().date(),
                activities__publish=True,
            ).distinct()
            .order_by("title")
        )
        return context
