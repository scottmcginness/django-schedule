import datetime
import os
import pytz

from django.core.urlresolvers import reverse
from django.test import TestCase

from schedule.models import Event, Rule, Occurrence, Calendar
from schedule.periods import Period, Month, Day
from schedule.utils import EventListManager


class TestEventListManager(TestCase):
    def setUp(self):
        weekly = Rule(frequency="WEEKLY")
        weekly.save()
        daily = Rule(frequency="DAILY")
        daily.save()
        cal = Calendar(name="MyCal")
        cal.save()

        self.event1 = Event(**{
            'title': 'Weekly Event',
            'start': datetime.datetime(2009, 4, 1, 8, 0, tzinfo=pytz.utc),
            'end': datetime.datetime(2009, 4, 1, 9, 0, tzinfo=pytz.utc),
            'end_recurring_period': datetime.datetime(2009, 10, 5, 0, 0, tzinfo=pytz.utc),
            'rule': weekly,
            'calendar': cal
        })
        self.event1.save()
        self.event2 = Event(**{
            'title': 'Recent Event',
            'start': datetime.datetime(2008, 1, 5, 9, 0, tzinfo=pytz.utc),
            'end': datetime.datetime(2008, 1, 5, 10, 0, tzinfo=pytz.utc),
            'end_recurring_period': datetime.datetime(2009, 5, 5, 0, 0, tzinfo=pytz.utc),
            'rule': daily,
            'calendar': cal
        })
        self.event2.save()

    def test_occurrences_after(self):
        eml = EventListManager([self.event1, self.event2])
        occurrences = eml.occurrences_after(datetime.datetime(2009, 4, 1, 0, 0, tzinfo=pytz.utc))
        self.assertEqual(occurrences.next().event, self.event1)
        self.assertEqual(occurrences.next().event, self.event2)
        self.assertEqual(occurrences.next().event, self.event2)
        self.assertEqual(occurrences.next().event, self.event2)
        self.assertEqual(occurrences.next().event, self.event2)
        self.assertEqual(occurrences.next().event, self.event2)
        self.assertEqual(occurrences.next().event, self.event2)
        self.assertEqual(occurrences.next().event, self.event2)
        self.assertEqual(occurrences.next().event, self.event1)
