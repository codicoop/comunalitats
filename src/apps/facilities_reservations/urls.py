from django.urls import path

from .views import ReservationsCalendarView, AjaxCalendarFeed


urlpatterns = [
    path('calendar/', ReservationsCalendarView.as_view(), name='fullcalendar'),

    # AJAX API
    # We are using the default way for FullCalendar to query the events. Because of that, we
    # have to deal with a url with the old style parameters (?blah=12 and so).
    # So the path is everything before the params start, and then in the view we will have to
    # catch the parameters from the GET[].
    path('ajax/calendar/', AjaxCalendarFeed.as_view(),
         name="ajax_calendar_feed")
]
