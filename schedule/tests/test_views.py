import os
import datetime

from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from schedule.templatetags.scheduletags import querystring_for_date
from schedule.views import check_next_url, coerce_date_dict

c = Client()


class TestViewUtils(TestCase):

    def test_check_next_url(self):
        url = "http://thauber.com"
        self.assertTrue(check_next_url(url) is None)
        url = "/hello/world/"
        self.assertEqual(url, check_next_url(url))

    def test_coerce_date_dict(self):
        date_dict = coerce_date_dict({
            'year': '2008', 'month': '4', 'day': '2',
            'hour': '4', 'minute': '4', 'second': '4'
        })
        expected = {
            'year': 2008, 'month': 4, 'day': 2,
            'hour': 4, 'minute': 4, 'second': 4
        }
        self.assertEqual(date_dict, expected)

    def test_coerce_date_dict_partial(self):
        date_dict = coerce_date_dict({'year': '2008', 'month': '4', 'day': '2'})
        expected = {'year': 2008, 'month': 4, 'day': 2, 'hour': 0, 'minute': 0, 'second': 0}
        self.assertEqual(date_dict, expected)

    def test_coerce_date_dict_empty(self):
        date_dict = coerce_date_dict({})
        expected = {}
        self.assertEqual(date_dict, expected)

    def test_coerce_date_dict_missing_values(self):
        date_dict = coerce_date_dict({'year': '2008', 'month': '4', 'hours': '3'}),
        expected = {'year': 2008, 'month': 4, 'day': 1, 'hour': 0, 'minute': 0, 'second': 0}
        self.assertEqual(date_dict, expected)


class TestUrls(TestCase):
    fixtures = ['schedule.json']
    highest_event_id = 7

    def test_calendar_view(self):
        url = reverse("year_calendar", kwargs={"calendar_slug": 'example'})
        self.response = c.get(url, {})
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.context[0]["calendar"].name,
                         "Example Calendar")

    def test_calendar_month_view(self):
        url = reverse("month_calendar", kwargs={"calendar_slug": 'example'})
        data = {'year': 2000, 'month': 11}
        self.response = c.get(url, data)
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.context[0]["calendar"].name, "Example Calendar")
        month = self.response.context[0]["periods"]['month']
        self.assertEqual((month.start, month.end),
                         (datetime.datetime(2000, 11, 1, 0, 0), datetime.datetime(2000, 12, 1, 0, 0)))

    def test_event_creation_anonymous_user(self):
        url = reverse("calendar_create_event", kwargs={"calendar_slug": 'example'})
        self.response = c.get(url, {})
        self.assertEqual(self.response.status_code, 302)

    def test_event_creation_authenticated_user(self):
        c.login(username="admin", password="admin")
        url = reverse("calendar_create_event", kwargs={"calendar_slug": 'example'})
        self.response = c.get(url, {})
        self.assertEqual(self.response.status_code, 200)

        url = reverse("calendar_create_event", kwargs={"calendar_slug": 'example'})
        data = {
            'description': 'description',
            'title': 'title',
            'end_recurring_period_0': '2008-10-30',
            'end_recurring_period_1': '10:22:00',
            'end_recurring_period_2': 'AM',
            'end_0': '2008-10-30',
            'end_1': '10:22:00',
            'end_2': 'AM',
            'start_0': '2008-10-30',
            'start_1': '09:21:57',
            'start_2': 'AM',
        }
        self.response = c.post(url, data)
        self.assertEqual(self.response.status_code, 302)

        highest_event_id = self.highest_event_id
        highest_event_id += 1

        url = reverse("event", kwargs={"event_id": highest_event_id})
        self.response = c.get(url, {})
        self.assertEqual(self.response.status_code, 200)
        c.logout()

    def test_view_event(self):
        self.response = c.get(reverse("event", kwargs={"event_id": 1}), {})
        self.assertEqual(self.response.status_code, 200)

    def test_delete_event_anonymous_user(self):
        # Only logged-in users should be able to delete, so we're redirected
        self.response = c.get(reverse("delete_event", kwargs={"event_id": 1}), {})
        self.assertEqual(self.response.status_code, 302)

    def test_delete_event_authenticated_user(self):
        c.login(username="admin", password="admin")

        # Load the deletion page
        self.response = c.get(reverse("delete_event", kwargs={"event_id": 1}), {})
        self.assertEqual(self.response.status_code, 200)

        # Delete the event
        self.response = c.post(reverse("delete_event", kwargs={"event_id": 1}), {})
        self.assertEqual(self.response.status_code, 302)

        # Since the event is now deleted, we get a 404
        self.response = c.get(reverse("delete_event", kwargs={"event_id": 1}), {})
        self.assertEqual(self.response.status_code, 404)
        c.logout()
