from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime

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
        except:
            return JsonResponse(data, safe=False)
        try:
            end = parse_datetime(request.GET['end'])
        except:
            return JsonResponse(data, safe=False)

        events = Reservation.objects.all()

        for event in events:
            event_data = {
                    'title': event.title,
                    'start': date_to_tull_calendar_format(event.start),
                    'end': date_to_tull_calendar_format(event.end),
                    'url': event.url,
                    'color': event.room.color
                }
            data.append(event_data)
        return JsonResponse(data, safe=False)


def date_to_tull_calendar_format(date_obj):
    return date_obj.strftime("%Y-%m-%dT%H:%M:%S")
