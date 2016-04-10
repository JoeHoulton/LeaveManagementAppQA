from django.test import TestCase

from django.test.utils import setup_test_environment
from django.contrib import auth

import random
import datetime
from dateutil.relativedelta import relativedelta
import json
import simplejson

from LeaveManagementAppQA.cal.models import LEAVE_EVENTS
from LeaveManagementAppQA.accounts.models import Employee
from LeaveManagementAppQA.cal.models import ORGANISATIONS
from LeaveManagementAppQA.cal.models import TEAMS
from django.contrib.auth.models import User

class DashboardTesting(TestCase):

    manager_object = ""
    user_object = ""

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

    def test_dashboard_page_loads(self):

        response = self.client.get('/account/login/', follow=True)

        user_to_test = User.objects.get(username="john")

        self.client.post('/account/auth/', {'username': user_to_test.username, 'password': 'johnpassword'}, follow=True)

        response = self.client.get('/dashboard/', follow=True)

        assert response.status_code == 200


    def test_dashboard_leave_entitlement_appears(self):

        leave_entitlement_value = '"leave_entitlement\\": 25'

        user_object = User.objects.get(username="john")

        self.client.post('/account/auth/', {'username': user_object.username, 'password': 'johnpassword'}, follow=True)

        response = self.client.get('/dashboard/', follow=True)

        response = self.client.get('/account/leavedetails/', follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        leave_information_response = str(response.content)

        if leave_entitlement_value in leave_information_response:
            assert True
        else:
            assert False


    def test_dashboard_leave_remaining_appears(self):

        leave_remaining_value = '"leave_remaining\\": 25'

        user_object = User.objects.get(username="john")

        self.client.post('/account/auth/', {'username': user_object.username, 'password': 'johnpassword'}, follow=True)

        response = self.client.get('/dashboard/', follow=True)

        response = self.client.get('/account/leavedetails/', follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        leave_remaining_response = str(response.content)

        if leave_remaining_value in leave_remaining_response:
            assert True
        else:
            assert False


    def test_dashboard_requests_to_approve_appears(self):

        leave_remaining_value = '"requests_to_approve_count": 0'

        user_object = User.objects.get(username="john")

        self.client.post('/account/auth/', {'username': user_object.username, 'password': 'johnpassword'}, follow=True)

        response = self.client.get('/dashboard/', follow=True)

        response = self.client.get('/dashboard/getrequeststoapprove/', follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        leave_remaining_response = str(response.content)

        if leave_remaining_value in leave_remaining_response:
            assert True
        else:
            assert False

    def test_dashboard_pending_requests_appears(self):

        leave_remaining_value = '"pending_leave_event_count": 0'

        user_object = User.objects.get(username="john")

        self.client.post('/account/auth/', {'username': user_object.username, 'password': 'johnpassword'}, follow=True)

        response = self.client.get('/dashboard/', follow=True)

        response = self.client.get('/dashboard/getpersonalevents/', follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        leave_remaining_response = str(response.content)

        if leave_remaining_value in leave_remaining_response:
            assert True
        else:
            assert False

    def test_dashboard_approved_requests_appears(self):

        leave_remaining_value = '"approved_leave_event_count": 0'

        user_object = User.objects.get(username="john")

        self.client.post('/account/auth/', {'username': user_object.username, 'password': 'johnpassword'}, follow=True)

        response = self.client.get('/dashboard/', follow=True)

        response = self.client.get('/dashboard/getpersonalevents/', follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        leave_remaining_response = str(response.content)

        if leave_remaining_value in leave_remaining_response:
            assert True
        else:
            assert False

    def test_bradford_factor_appears(self):

        bradford_factor_value = '"bradford_factor": 10'

        user_object = User.objects.get(username="john")

        self.client.post('/account/auth/', {'username': user_object.username, 'password': 'johnpassword'}, follow=True)

        todays_date = datetime.datetime.today().date()
        todays_date_plus_ten = todays_date + datetime.timedelta(days=10)

        leave_event = LEAVE_EVENTS(
            title = "Sick Leave",
            snippet = "This is the reason for leave",
            body = "This is the reason for leave ABCD",
            start_date = todays_date,
            end_date = todays_date_plus_ten,
            start_time = "Beginning of Day",
            end_time = "End of Day",
            status = "Approved",
            creator_id = user_object,
            remind = False
            )

        leave_event.save()

        response = self.client.get('/dashboard/', follow=True)

        response = self.client.get('/dashboard/getbradfordfactor/', follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        bradford_factor_response = response.content

        if bradford_factor_value in bradford_factor_response:
            assert True
        else:
            assert False


    def test_dashboard_correctly_formed_leave_request_accepted(self):

        user_object = User.objects.get(username="john")

        self.client.post('/account/auth/', {'username': user_object.username, 'password': 'johnpassword'}, follow=True)

        response = self.client.get('/dashboard/', follow=True)

        leave_type = "Annual Leave"
        start_date = "18/01/2016"
        end_date = "04/02/2016"
        start_date_start_time = "Begining of Day"
        end_date_start_time = "End of Day"
        leave_reason = "This is the current reason for the leave request that should be accepted"

        response = self.client.post('/dashboard/submitrequest/', {'leaveType': leave_type, 'start_date': start_date,
                                                                  'end_date': end_date, 'start_date_start_time': start_date_start_time,
                                                                  'end_date_start_time':end_date_start_time, 'leave_reason': leave_reason})

        response_json = eval(response.content)[0]

        assert ((str(response_json) == "successful"))

    def test_dashboard_incorrectly_formed_leave_request_rejected(self):

        user_object = User.objects.get(username="john")

        self.client.post('/account/auth/', {'username': user_object.username, 'password': 'johnpassword'}, follow=True)

        response = self.client.get('/dashboard/', follow=True)

        leave_type = "Annual Leave"
        start_date = "18/01/2016"
        end_date = "16/01/2016"
        start_date_start_time = "Begining of Day"
        end_date_start_time = "End of Day"
        leave_reason = "This is the current reason for the leave request that should not be accepted"
        approval_type = "Manager"

        response = self.client.post('/dashboard/submitrequest/', {'leaveType': leave_type, 'start_date': start_date, 'end_date': end_date, 'start_date_start_time': start_date_start_time,
                                                                 'end_date_start_time':end_date_start_time, 'leave_reason': leave_reason, 'approval_type': approval_type})

        assert ((str(response.content) != leave_reason))




