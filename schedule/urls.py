from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list

from schedule.feeds import UpcomingEventsFeed, CalendarICalendar
from schedule.models import Calendar
from schedule.feeds import UpcomingEventsFeed
from schedule.feeds import CalendarICalendar
from schedule.periods import Decade, Year, Month, Week, Day

urlpatterns = patterns('')

# Calendar URLs
urlpatterns += patterns('',
    url(r'^calendar/$', object_list, name="schedule",
        kwargs={
            'queryset': Calendar.objects.all(),
            'template_name': 'schedule/calendar_list.html'}),

    url(r'^calendar/decade/(?P<calendar_slug>[-\w]+)/$',
        'schedule.views.calendar_by_periods', name="decade_calendar",
        kwargs={
            'periods': [Decade],
            'template_name': 'schedule/calendar_decade.html'}),

    url(r'^calendar/year/(?P<calendar_slug>[-\w]+)/$',
        'schedule.views.calendar_by_periods', name="year_calendar",
        kwargs={
            'periods': [Year],
            'template_name': 'schedule/calendar_year.html'}),

    url(r'^calendar/tri_month/(?P<calendar_slug>[-\w]+)/$',
        'schedule.views.calendar_by_periods', name="tri_month_calendar",
        kwargs={
            'periods': [Month],
            'template_name': 'schedule/calendar_tri_month.html'}),

    url(r'^calendar/compact_month/(?P<calendar_slug>[-\w]+)/$',
        'schedule.views.calendar_by_periods', name="compact_calendar",
        kwargs={
            'periods': [Month],
            'template_name': 'schedule/calendar_compact_month.html'}),

    url(r'^calendar/month/(?P<calendar_slug>[-\w]+)/$',
        'schedule.views.calendar_by_periods', name="month_calendar",
        kwargs={
            'periods': [Month],
            'template_name': 'schedule/calendar_month.html'}),

    url(r'^calendar/week/(?P<calendar_slug>[-\w]+)/$',
        'schedule.views.calendar_by_periods', name="week_calendar",
        kwargs={
            'periods': [Week],
            'template_name': 'schedule/calendar_week.html'}),

    url(r'^calendar/daily/(?P<calendar_slug>[-\w]+)/$',
        'schedule.views.calendar_by_periods', name="day_calendar",
        kwargs={
            'periods': [Day],
            'template_name': 'schedule/calendar_day.html'}),

    url(r'^calendar/(?P<calendar_slug>[-\w]+)/$',
        'schedule.views.calendar', name="calendar_home"),
)

url(r'^calendar/(?P<calendar_slug>[-\w]+)/$',
    'schedule.views.calendar',
    name = "calendar_home",
    ),

# Event URLs
urlpatterns += patterns('',
    url(r'^event/create/(?P<calendar_slug>[-\w]+)/$',
        'schedule.views.create_or_edit_event',
        name='calendar_create_event'),

    url(r'^event/edit/(?P<calendar_slug>[-\w]+)/(?P<event_id>\d+)/$',
        'schedule.views.create_or_edit_event',
        name='edit_event'),

    url(r'^event/(?P<event_id>\d+)/$',
        'schedule.views.event',
        name="event"),

    url(r'^event/delete/(?P<event_id>\d+)/$',
        'schedule.views.delete_event',
        name="delete_event"),
)

# Persisted occurrence URLs
urlpatterns += patterns('',
    url(r'^occurrence/(?P<event_id>\d+)/(?P<occurrence_id>\d+)/$',
        'schedule.views.occurrence', name="occurrence"),

    url(r'^occurrence/cancel/(?P<event_id>\d+)/(?P<occurrence_id>\d+)/$',
        'schedule.views.cancel_occurrence', name="cancel_occurrence"),

    url(r'^occurrence/edit/(?P<event_id>\d+)/(?P<occurrence_id>\d+)/$',
        'schedule.views.edit_occurrence', name="edit_occurrence"),
)

# Unpersisted occurrence URLs
DATE_URL = (r"(?P<event_id>\d+)/"
            r"(?P<year>\d+)/"
            r"(?P<month>\d+)/"
            r"(?P<day>\d+)/"
            r"(?P<hour>\d+)/"
            r"(?P<minute>\d+)/"
            r"(?P<second>\d+)/$")

urlpatterns += patterns('',
    url(r'^occurrence/' + DATE_URL,
        'schedule.views.occurrence',
        name="occurrence_by_date"),

    url(r'^occurrence/cancel/' + DATE_URL,
        'schedule.views.cancel_occurrence',
        name="cancel_occurrence_by_date"),

    url(r'^occurrence/edit/' + DATE_URL,
        'schedule.views.edit_occurrence',
        name="edit_occurrence_by_date"),
)

# Feed URLs
urlpatterns += patterns('',
    url(r'^feed/calendar/(.*)/$',
        'django.contrib.syndication.views.feed',
        {"feed_dict": {"upcoming": UpcomingEventsFeed}}),

    url(r'^ical/calendar/(.*)/$', CalendarICalendar()),
)

# AJAX API
urlpatterns += patterns('',
    url(r'^ajax/occurrence/edit_by_code/$',
        'schedule.views.ajax_edit_occurrence_by_code',
        name="ajax_edit_occurrence_by_code"),

    url(r'^ajax/calendar/week/json/(?P<calendar_slug>[-\w]+)/$',
        'schedule.views.calendar_by_periods_json',
        name="week_calendar_json",
        kwargs={'periods': [Week]}),

    url(r'^ajax/edit_event/(?P<calendar_slug>[-\w]+)/$',
        'schedule.views.ajax_edit_event',
        name="ajax_edit_event"),

    url(r'^event_json/$',
        'schedule.views.event_json',
        name="event_json"),

    url(r'^$', object_list,
        {'queryset': Calendar.objects.all()},
        name='schedule'),
)
