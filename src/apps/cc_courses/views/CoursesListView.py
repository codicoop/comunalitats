
from django.views import generic
from apps.cc_courses.models import Course, Activity
from django.utils import timezone


class CoursesListView(generic.ListView):
    model = Course
    template_name = 'courses.html'
    # queryset = Course.objects.filter(date_start__gte=timezone.now().date())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['future_courses'] = Course.published.filter(
            activities__date_start__gte=timezone.now().date()).distinct()
        # context['future_courses'] = context['course_list']
        return context
