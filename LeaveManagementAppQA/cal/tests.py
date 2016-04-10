from django.test import TestCase

from django.test.utils import setup_test_environment
from django.contrib import auth
import random
import datetime
from dateutil.relativedelta import relativedelta
import json

from LeaveManagementAppQA.cal.models import LEAVE_EVENTS
from LeaveManagementAppQA.accounts.models import Employee
from LeaveManagementAppQA.cal.models import ORGANISATIONS
from LeaveManagementAppQA.cal.models import TEAMS
from django.contrib.auth.models import User


class CalendarTesting(TestCase):
    def setUp(self):
        #create auth user objects

        manager_object = User.objects.create_superuser('john', 'lennon@thebeatles.com', 'johnpassword')
        user_object = User.objects.create_user('bob', 'bob@thebeatles.com', 'bobpassword')

        #create organisations

        organisation_object = ORGANISATIONS(
            updated_at = datetime.datetime.today(),
            organisation_name = "test_organisation"
            )

        organisation_object.save()

        #create teams

        team_object = TEAMS(
            updated_at = datetime.datetime.today(),
            team_name = "test_team",
            organisation_name = organisation_object
            )

        team_object.save()

        #create employee representations of these user objects

        manager_employee = Employee(
            user = manager_object,
            manager = manager_object,
            organisation = organisation_object,
            leave_entitlement = "25.00",
            leave_remaining = "25.00",
            team_name = team_object,
            )

        manager_employee.save()

        user_employee = Employee(
            user = user_object,
            manager = manager_object,
            organisation = organisation_object,
            leave_entitlement = "25.00",
            leave_remaining = "25.00",
            team_name = team_object,
            )

        user_employee.save()

        self.client.get('/account/login/', follow=True)

        user_to_test = User.objects.get(username="john")

        self.client.post('/account/auth/', {'username': user_to_test.username, 'password': 'johnpassword'}, follow=True)

    def test_team_leave_page_loads(self):

        response = self.client.get('/calendar', follow=True)

        assert (response.status_code == 200)

    def test_no_leave_events_load_when_user_has_not_requested_leave(self):

        response = self.client.get('/calendar', follow=True)

        response = self.client.get('/calendar/getevents/', follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        if response.content == "[]":
            assert True
        else:
            assert False

    def test_all_leave_events_load_correctly(self):

        user_object = User.objects.get(username="john")

        value_to_test = '"body": "This is the reason for leave ABCD"'

        todays_date = datetime.datetime.today().date()
        todays_date_plus_five = todays_date + datetime.timedelta(days=5)

        leave_event = LEAVE_EVENTS(
            title = "Sick Leave",
            snippet = "This is the reason for leave",
            body = "This is the reason for leave ABCD",
            start_date = todays_date,
            end_date = todays_date_plus_five,
            start_time = "Beginning of Day",
            end_time = "End of Day",
            status = "Approved",
            creator_id = user_object,
            remind = False
            )

        leave_event.save()

        response = self.client.get('/calendar', follow=True)

        response = self.client.get('/calendar/getevents/', follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        response_array = eval(response.content)[0]

        assert str(response_array["start_date"]) == str(todays_date)
