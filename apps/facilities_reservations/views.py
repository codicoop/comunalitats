from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime


class ReservationsCalendarView(TemplateView):
    template_name = "fullcalendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AjaxCalendarFeed(View):
    def get(self, request, *args, **kwargs):
        # FullCalendar passes ISO8601 formatted date strings
        try:
            start = parse_datetime(request.GET['start'])
        except:
            print('Retornar error, he de mirar com es fa. Potser només retornant null ja està.')
            return
        try:
            end = parse_datetime(request.GET['end'])
        except:
            print('Retornar error, he de mirar com es fa. Potser només retornant null ja està.')
            return

        event_start = parse_datetime(f'2019-09-{start.day}T10:00:00')
        event_end = parse_datetime(f'2019-09-{start.day}T13:00:00')
        # Here we will query the events where dates in between start and end…
        events = [
            {
                start: event_start,
                end: event_end
            },
            {
                start: event_start,
                end: event_end
            },
        ]

        data = []
        for event in events:
            print('event: '+str(event))
            data.append(
                {
                    'title': "Títol de la formació d'aquest dia, al clicar ens pot portar a la fitxa, p.ex.",
                    'start': date_to_tull_calendar_format(event.start),
                    'end': date_to_tull_calendar_format(event.end),
                    'url': 'http://codi.coop',
                    'color': 'red'
                }
            )
        print(data)
        return JsonResponse(data, safe=False)


def date_to_tull_calendar_format(date_obj):
    return date_obj.strftime("%Y-%m-%dT%H:%M:%S")
