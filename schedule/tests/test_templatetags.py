import datetime
import pytz
from django.test import TestCase
from schedule.templatetags.scheduletags import querystring_for_date


class TestTemplateTags(TestCase):
    def test_querystring_for_datetime(self):
        date = datetime.datetime(2008, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
        query_string = querystring_for_date(date)
        expected_qs = "?year=2008&amp;month=1&amp;day=1&amp;hour=0&amp;minute=0&amp;second=0"
        self.assertEqual(query_string, expected_qs)
