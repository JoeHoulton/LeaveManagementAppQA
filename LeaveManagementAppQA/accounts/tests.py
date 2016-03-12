from django.test import TestCase

from django.test.utils import setup_test_environment
from django.contrib import auth
import random

from LeaveManagementAppQA.cal.models import LEAVE_EVENTS
from LeaveManagementAppQA.accounts.models import Employee
from LeaveManagementAppQA.cal.models import ORGANISATIONS
from LeaveManagementAppQA.cal.models import TEAMS
from django.contrib.auth.models import User

class AccountTesting(TestCase):

    def test_user_login_page_loads(self):

        response = self.client.get('account/login/')

        assert response.statuscode == 200

    def test_user_can_sucessfully_login(self):

        # get random user from the database

        # log them in using their username and password as you would do usually

        # assertEqual that they are now authenticated

        user_to_test = User.objects.filter(pk=2)[0]

        response = self.client.post('account/auth/', {'username': user_to_test.username, 'password': user_to_test.password})

        assert self.assertEqual(int(self.client.session['_auth_user_id']), user_to_test.pk)

    def test_user_has_a_manager(self):

        user_object = User.objects.filter(username="userfortest")[0]
        manager_object = User.objects.filter(username="managerfortest")[0]
        organisation_object = ORGANISATIONS.objects.get(organisation_name="test_organisation")
        team_object = TEAMS.objects.get(team_name="test_team_1")

        created_employee = Employee(
            user = user_object.id,
            manager = manager_object.id,
            organisation = organisation_object.id,
            leave_entitlement = "25.00",
            leave_remaining = "25.00",
            team_name = team_object.id,
            )

        created_employee.save()

        assert self.assertEqual(created_employee.manager, manager_object.id)

    def test_user_can_have_leave_approved_or_declined_by_manager(self):

        user_object = User.objects.filter(username="userfortest")[0]
        manager_object = User.objects.filter(username="managerfortest")[0]

        response = self.client.get('event/approvedlocal/', {'leave_id': 2, 'name': "approved_button"})

        created_employee = Employee(
            user = user_object.id,
            manager = manager_object.id,
            organisation = organisation_object.id,
            leave_entitlement = "25.00",
            leave_remaining = "25.00",
            team_name = team_object.id,
            )

        created_employee.save()

        assert self.assertEqual(created_employee.manager, manager_object.id)

    def test_user_can_have_leave_approved_by_manager(self):

        approved_button = 'approved_button'
        approved_value = 'Approved'

        self.client.logout()

        manager_object = User.objects.filter(username="managerfortest")[0]

        self.client.post('account/auth/', {'username': manager_object.username, 'password': manager_object.password})

        response = self.client.get('event/approvedlocal/', {'leave_id': 2, 'name': approved_button})

        approved_leave_event = LEAVE_EVENTS.objects.filter(pk=2)[0]

        assert self.assertEqual(approved_leave_event.status, approved_value)

    def test_user_can_have_leave_declined_by_manager(self):

        declined_button = 'declined_button'
        declined_value = 'Declined'

        response = self.client.get('event/approvedlocal/', {'leave_id': 3, 'name': declined_button})

        approved_leave_event = LEAVE_EVENTS.objects.filter(pk=3)[0]

        assert self.assertEqual(approved_leave_event.status, declined_value)

    def test_user_can_access_profile_page(self):

        self.client.logout()

        user_to_test = User.objects.filter(pk=2)[0]

        response = self.client.post('account/auth/', {'username': user_to_test.username, 'password': user_to_test.password})

        response = self.client.get('account/profile/')

        assert response.statuscode == 200










