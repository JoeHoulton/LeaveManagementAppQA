from django.test import TestCase

from django.test.utils import setup_test_environment
from django.contrib import auth

from LeaveManagementAppQA.cal.models import LEAVE_EVENTS
from LeaveManagementAppQA.accounts.models import Employee
from django.contrib.auth.models import User

class DashboardTesting(TestCase):

    def login_user(self):

        user_to_test = User.objects.filter(pk=1)[0]

        self.client.login(username=user_to_test.username, password=user_to_test.password)


    def test_dashboard_page_loads(self):

        response = self.client.get('dashboard/')

        assert response.statuscode == 200


    def test_dashboard_leave_entitlement_appears(self):

        user_id_of_logged_in_user = self.client.session['_auth_user_id']

        leave_entitlement_of_logged_in_user = Employee.objects.get(user=user_id_of_logged_in_user).leave_entitlement

        response = self.client.get('dashboard/')

        self.assertContains(response, '<h3 align="center" id="leave_entitlement">' + leave_entitlement_of_logged_in_user + ' days</h3>')


    def test_dashboard_leave_remaining_appears(self):

        user_id_of_logged_in_user = self.client.session['_auth_user_id']

        leave_remaining_of_logged_in_user = Employee.objects.get(user=user_id_of_logged_in_user).leave_remaining

        response = self.client.get('dashboard/')

        self.assertContains(response, ('<h3 align="center" id="leave_entitlement">' + leave_remaining_of_logged_in_user + ' days</h3>'))


    def test_dashboard_requests_to_approve_appears(self):

        user_id_of_logged_in_user = self.client.session['_auth_user_id']

        leave_remaining_of_logged_in_user = Employee.objects.get(user=user_id_of_logged_in_user).leave_remaining

        response = self.client.get('dashboard/')

        self.assertContains(response, ('<h3 align="center" id="leave_entitlement">' + leave_remaining_of_logged_in_user + ' days</h3>'))


    def test_dashboard_pending_requests_appears(self):

        user_id_of_logged_in_user = self.client.session['_auth_user_id']

        leave_remaining_of_logged_in_user = Employee.objects.get(user=user_id_of_logged_in_user).leave_remaining

        response = self.client.get('dashboard/')

        self.assertContains(response, ('<h3 align="center" id="leave_entitlement">' + leave_remaining_of_logged_in_user + ' days</h3>'))


    def test_dashboard_approved_requests_appears(self):

        user_id_of_logged_in_user = self.client.session['_auth_user_id']

        leave_remaining_of_logged_in_user = Employee.objects.get(user=user_id_of_logged_in_user).leave_remaining

        response = self.client.get('dashboard/')

        self.assertContains(response, ('<h3 align="center" id="leave_entitlement">' + leave_remaining_of_logged_in_user + ' days</h3>'))


    def test_dashboard_correctly_formed_leave_request_accepted(self):

        leave_type = "Annual Leave"
        start_date = "18/01/2016"
        end_date = "04/02/2016"
        start_date_start_time = "Begining of Day"
        end_date_start_time = "End of Day"
        leave_reason = "This is the current reason for the leave request that should be accepted"
        approval_type = "Manager"

        response = self.client.post('dashboard/submitrequest/', {'leaveType': leave_type, 'start_date': start_date, 'end_date': end_date, 'startDateStartTime': start_date_start_time,
                                                                 'endDateEndTime':end_date_start_time, 'leaveReason': leave_reason, 'optradio': approval_type})

        self.assertEquals(response.context['leave_type'], leave_type)

    def test_dashboard_incorrectly_formed_leave_request_rejected(self):

        leave_type = "Annual Leave"
        start_date = "95/01/2016"
        end_date = "95/02/2016"
        start_date_start_time = "Begining of Day"
        end_date_start_time = "End of Day"
        leave_reason = "This is the current reason for the leave request that should not be accepted"
        approval_type = "Manager"

        response = self.client.post('dashboard/submitrequest/', {'leaveType': leave_type, 'start_date': start_date, 'end_date': end_date, 'startDateStartTime': start_date_start_time,
                                                                 'endDateEndTime':end_date_start_time, 'leaveReason': leave_reason, 'optradio': approval_type})

        self.assertEquals(response.context['leave_type'], False)




