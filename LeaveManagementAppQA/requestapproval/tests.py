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

from LeaveManagementAppQA.requestapproval import views


class RequestApprovalTesting(TestCase):

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

        response = self.client.get('/account/login/', follow=True)

        user_to_test = User.objects.get(username="john")

        self.client.post('/account/auth/', {'username': user_to_test.username, 'password': 'johnpassword'}, follow=True)

    def test_request_leave_page_loads(self):

        response = self.client.get('/leaverequests', follow=True)

        assert (response.status_code == 200)

    def test_user_requests_page_loads(self):

        response = self.client.get('/userrequests', follow=True)

        assert (response.status_code == 200)

    def test_team_leave_page_loads(self):

        response = self.client.get('/teamrequests', follow=True)

        assert (response.status_code == 200)

    def test_team_leave_information_correctly_loads(self):

        user_to_test = User.objects.get(username="bob")

        todays_date = datetime.datetime.today().date()

        value_to_test = "'start_date'" + ": u'" + str(todays_date) + "'"

        leave_event = LEAVE_EVENTS(
            title = "Annual Leave",
            snippet = "This is the reason for leave",
            body = "This is the reason for leave ABCD",
            start_date = todays_date,
            end_date = (datetime.datetime.today().date() + relativedelta(day=6)),
            start_time = "Lunchtime",
            end_time = "Lunchtime",
            status = "Approved",
            creator_id = user_to_test,
            remind = False
            )

        leave_event.save()

        response = self.client.get('/teamrequests', follow=True)

        response = self.client.get('/leaverequests/getallteamleaverequests/', follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        leave_data_response = json.loads(str(response.content))

        if value_to_test in str(leave_data_response):
            assert True
        else:
            assert False

    def test_user_can_cancel_request(self):

        user_to_test = User.objects.get(username="john")
        approval_status = "Cancelled"

        self.client.post('/account/auth/', {'username': user_to_test.username, 'password': 'johnpassword'}, follow=True)

        todays_date = datetime.datetime.today().date()

        leave_event = LEAVE_EVENTS(
            title = "Annual Leave",
            snippet = "This is the reason for leave",
            body = "This is the reason for leave ABCD",
            start_date = todays_date,
            end_date = (datetime.datetime.today().date() + relativedelta(day=6)),
            start_time = "Lunchtime",
            end_time = "Lunchtime",
            status = "Pending",
            creator_id = user_to_test,
            remind = False
            )

        leave_event.save()

        # response = self.client.post('/event/approvedlocal', {'leave_id': int(leave_event.id), 'name': "approved_button"}, follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        json_data = simplejson.dumps({'leave_id': 1,})

        response = self.client.post('/event/cancelled',json_data, follow=True,content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        #cancelled_leave_event_status = LEAVE_EVENTS.objects.get(pk=int(leave_event_id)).status
        #approval_response = json.loads(response.content)

        #approval_response = str(approval_response[0])]

        leave_event = LEAVE_EVENTS.objects.get(id=leave_event.id)

        assert self.assertEqual(response.status_code, leave_event.status)

    def test_days_of_leave_event_calculates_correctly(self):

        user_to_test = User.objects.get(username="bob")
        number_of_days_of_leave_event = 10

        todays_date = datetime.datetime.today().date()
        todays_date_plus_ten = todays_date + datetime.timedelta(days=10)

        leave_event = LEAVE_EVENTS(
            title = "Annual Leave",
            snippet = "This is the reason for leave",
            body = "This is the reason for leave ABCD",
            start_date = todays_date,
            end_date = todays_date_plus_ten,
            start_time = "Beginning of Day",
            end_time = "End of Day",
            status = "Approved",
            creator_id = user_to_test,
            remind = False
            )

        leave_event.save()

        calculated_value = views.calculate_days_of_leave_event(leave_event)

        assert (calculated_value == number_of_days_of_leave_event)

    def test_days_of_leave_event_calculates_correctly_when_days_are_not_full(self):

        user_to_test = User.objects.get(username="bob")
        number_of_days_of_leave_event = 8.5

        todays_date = datetime.datetime.today().date()
        todays_date_plus_time_delta = todays_date + datetime.timedelta(days=number_of_days_of_leave_event)

        leave_event = LEAVE_EVENTS(
            title = "Annual Leave",
            snippet = "This is the reason for leave",
            body = "This is the reason for leave ABCD",
            start_date = todays_date,
            end_date = todays_date_plus_time_delta,
            start_time = "Lunchtime",
            end_time = "Lunchtime",
            status = "Approved",
            creator_id = user_to_test,
            remind = False
            )

        leave_event.save()

        calculated_value = views.calculate_days_of_leave_event(leave_event)

        assert (calculated_value == number_of_days_of_leave_event)

    def test_user_can_have_leave_approved_by_manager_locally(self):

        user_object = User.objects.get(username="bob")
        manager_object = User.objects.get(username="john")

        approved_status = "approved"

        leave_event = LEAVE_EVENTS(
                    title = "Annual Leave",
                    snippet = "This is the reason for leave",
                    body = "This is the reason for leave ABCD",
                    start_date = datetime.datetime.today().date(),
                    end_date = (datetime.datetime.today().date() + relativedelta(day=6)),
                    start_time = "Lunchtime",
                    end_time = "Lunchtime",
                    status = "Pending",
                    creator_id = user_object,
                    remind = False
                    )

        leave_event.save()

        #create leave event for user
        #getid of leave event

        # log in as manager

        response = self.client.post('/account/auth/', {'username': "bob", 'password': 'bobpassword'}, follow=True)

        # request

        response = self.client.post('/event/approvedlocal', {'leave_id': int(leave_event.id), 'name': "approved_button"}, follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        approval_response = json.loads(response.content)

        approval_response = str(approval_response[0])

        assert (approval_response == approved_status)

    def test_user_can_have_leave_declined_by_manager_locally(self):

        user_object = User.objects.get(username="bob")
        manager_object = User.objects.get(username="john")

        declined_status = "approved"

        leave_event = LEAVE_EVENTS(
                    title = "Annual Leave",
                    snippet = "This is the reason for leave",
                    body = "This is the reason for leave ABCD",
                    start_date = datetime.datetime.today().date(),
                    end_date = (datetime.datetime.today().date() + relativedelta(day=6)),
                    start_time = "Lunchtime",
                    end_time = "Lunchtime",
                    status = "Pending",
                    creator_id = user_object,
                    remind = False
                    )

        leave_event.save()

        #create leave event for user
        #getid of leave event

        # log in as manager

        response = self.client.post('/account/auth/', {'username': "bob", 'password': 'bobpassword'}, follow=True)

        # request

        response = self.client.post('/event/approvedlocal', {'leave_id': int(leave_event.id), 'name': "declined_button"}, follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        approval_response = json.loads(response.content)

        approval_response = str(approval_response[0])

        assert (approval_response == declined_status)

    def test_user_can_have_leave_approved_or_declined_by_manager(self):

        user_object = User.objects.get(username="bob")
        manager_object = User.objects.get(username="john")

        approved_status = "approved"

        leave_event = LEAVE_EVENTS(
                    title = "Annual Leave",
                    snippet = "This is the reason for leave",
                    body = "This is the reason for leave ABCD",
                    start_date = datetime.datetime.today().date(),
                    end_date = (datetime.datetime.today().date() + relativedelta(day=6)),
                    start_time = "Lunchtime",
                    end_time = "Lunchtime",
                    status = "Pending",
                    creator_id = user_object,
                    remind = False
                    )

        leave_event.save()

        #create leave event for user
        #getid of leave event

        # log in as manager

        response = self.client.post('/account/auth/', {'username': "bob", 'password': 'bobpassword'}, follow=True)

        # request

        response = self.client.post('/event/approvedlocal', {'leave_id': int(leave_event.id), 'name': "approved_button"}, follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        approval_response = json.loads(response.content)

        approval_response = str(approval_response[0])

        assert (approval_response == approved_status)


    def test_approving_leave_correctly_decrements_leave_remaining(self):

        user_object = User.objects.get(username="bob")
        manager_object = User.objects.get(username="john")

        self.client.post('/account/auth/', {'username': "bob", 'password': 'bobpassword'}, follow=True)

        employee_object_updated_leave_remaining_before = Employee.objects.get(user=user_object).leave_remaining

        days_of_leave_request = 10

        leave_type = "Annual Leave",
        leave_reason = "This is the reason for leave",
        start_date = datetime.datetime.today().date(),
        end_date = (datetime.datetime.today().date() + datetime.timedelta(days=days_of_leave_request)),
        start_time = "Beginning of Day",
        end_time = "End of Day",

        self.client.post('/dashboard/submitrequest/', {'leaveType': leave_type, 'start_date': start_date,
                                                       'end_date': end_date, 'start_date_start_time': start_time,
                                                       'end_date_start_time':end_time, 'leave_reason': leave_reason})

        self.client.post('/account/auth/', {'username': "john", 'password': 'johnpassword'}, follow=True)

        self.client.get('/leaverequests', follow=True)

        response = self.client.get('/leaverequests/getleaverequests/',follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        response_array = eval(response.content)[0]

        leave_event_to_approve_id = int(response_array["leave_id"])

        self.client.post('/event/approved', {'leave_id': int(leave_event_to_approve_id), 'approved_button': "Approve Leave"}, follow=True)

        employee_object_updated_leave_remaining_after = Employee.objects.get(user=user_object).leave_remaining

        assert (employee_object_updated_leave_remaining_after == employee_object_updated_leave_remaining_before - days_of_leave_request)

    def test_declining_leave_doesnt_decrement_leave_remaining(self):

        user_object = User.objects.get(username="bob")
        manager_object = User.objects.get(username="john")

        employee_object_updated_leave_remaining_before = Employee.objects.get(user=user_object).leave_remaining

        days_of_leave_request = 5

        leave_event = LEAVE_EVENTS(
                    title = "Annual Leave",
                    snippet = "This is the reason for leave",
                    body = "This is the reason for leave ABCD",
                    start_date = datetime.datetime.today().date(),
                    end_date = (datetime.datetime.today().date() + datetime.timedelta(days=days_of_leave_request)),
                    start_time = "Lunchtime",
                    end_time = "Lunchtime",
                    status = "Pending",
                    creator_id = user_object,
                    remind = False
                    )

        leave_event.save()

        self.client.post('/account/auth/', {'username': "bob", 'password': 'bobpassword'}, follow=True)

        self.client.get('/event/approved', {'leave_id': int(leave_event.id), 'declined_button': "Decline Leave"}, follow=True)

        employee_object_updated_leave_remaining_after = Employee.objects.get(user=user_object).leave_remaining

        assert (employee_object_updated_leave_remaining_after != employee_object_updated_leave_remaining_before - days_of_leave_request)

    def test_user_requests_page_loads_leave_successfully_when_no_leave_present(self):

        response = self.client.get('/userrequests', follow=True)

        response = self.client.get('/userrequests/getuserrequests/',follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        if response.content == "[]":
            assert True
        else:
            assert False

    def test_user_requests_page_loads_leave_successfully_when_leave_present(self):

        response = self.client.get('/userrequests', follow=True)

        value_to_test = '"body": "his is the reason for leave ABCD"'

        user_object = User.objects.get(username="john")

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

        response = self.client.get('/userrequests/getuserrequests/',follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        response_json = eval(response.content)[0]

        assert (str(response_json["start_date"]) == str(todays_date))

    def test_approve_leave_page_loads_leave_successfully_when_no_leave_present(self):

        response = self.client.get('/leaverequests', follow=True)

        response = self.client.get('/leaverequests/getleaverequests/',follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        if response.content == "[]":
            assert True
        else:
            assert False

    def test_approve_leave_page_loads_leave_successfully_when_leave_to_approve_present(self):

        response = self.client.get('/leaverequests', follow=True)

        value_to_test = '"body": "his is the reason for leave ABCD"'

        user_object = User.objects.get(username="bob")
        manager_object = User.objects.get(username="john")

        todays_date = datetime.datetime.today().date()
        todays_date_plus_five = todays_date + datetime.timedelta(days=5)

        leave_event = LEAVE_EVENTS(
            title = "Annual Leave",
            snippet = "This is the reason for leave",
            body = "This is the reason for leave ABCD",
            start_date = todays_date,
            end_date = todays_date_plus_five,
            start_time = "Beginning of Day",
            end_time = "End of Day",
            status = "Pending",
            creator_id = user_object,
            remind = False
            )

        leave_event.save()

        response = self.client.post('/account/auth/', {'username': "john", 'password': 'johnpassword'}, follow=True)

        response = self.client.get('/leaverequests/getleaverequests/',follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        response_array = eval(response.content)[0]

        assert (str(response_array["start_date"]) == str(todays_date))


    def test_approve_leave_page_does_not_load_leave_for_requesting_user(self):

        response = self.client.get('/leaverequests', follow=True)

        user_object = User.objects.get(username="bob")
        manager_object = User.objects.get(username="john")

        todays_date = datetime.datetime.today().date()
        todays_date_plus_five = todays_date + datetime.timedelta(days=5)

        leave_event = LEAVE_EVENTS(
            title = "Annual Leave",
            snippet = "This is the reason for leave",
            body = "This is the reason for leave ABCD",
            start_date = todays_date,
            end_date = todays_date_plus_five,
            start_time = "Beginning of Day",
            end_time = "End of Day",
            status = "Pending",
            creator_id = user_object,
            remind = False
            )

        leave_event.save()

        response = self.client.post('/account/auth/', {'username': "bob", 'password': 'bobpassword'}, follow=True)

        response = self.client.get('/leaverequests/getleaverequests/',follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        if response.content == "[]":
            assert True
        else:
            assert False

    def test_team_leave_page_loads_successfully_when_no_leave_present(self):

        response = self.client.get('/teamrequests', follow=True)

        response = self.client.get('/leaverequests/getallteamleaverequests/',follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        response_array = eval(response.content)[0]

        assert (str(response_array["start_date"]) == "")





