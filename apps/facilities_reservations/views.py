from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from facilities_reservations.models import Reservation, Room


class ReservationsCalendarView(TemplateView):
    template_name = "fullcalendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rooms = Room.objects.all()
        context['rooms'] = rooms
        return context


class AjaxCalendarFeed(View):
    def get(self, request, *args, **kwargs):
        data = []

        # FullCalendar passes ISO8601 formatted date strings
        try:
            start = parse_datetime(request.GET['start'])
            end = parse_datetime(request.GET['end'])
        except:
            return JsonResponse(data, safe=False)

        events = Reservation.objects.filter(start__gte=start, end__lte=end)
        for event in events:
            event_data = {
                    'title': f"{event.title} [{event.responsible}]",
                    'start': date_to_tull_calendar_format(event.start),
                    'end': date_to_tull_calendar_format(event.end),
                    'color': event.room.color
                }
            if event.url:
                event_data['url'] = event.url
            data.append(event_data)
        return JsonResponse(data, safe=False)


def date_to_tull_calendar_format(date_obj):
    aware_date = timezone.localtime(date_obj)
    return aware_date.strftime("%Y-%m-%dT%H:%M:%S")
