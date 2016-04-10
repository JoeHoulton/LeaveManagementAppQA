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
from LeaveManagementAppQA.cal.models import ADDRESSES
from django.contrib.auth.models import User


class AccountTesting(TestCase):

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
            leave_entitlement = "25.00",
            leave_remaining = "25.00",
            team_name = team_object,
            organisation = organisation_object,
            )

        user_employee.save()

        user_to_test = User.objects.get(username="john")

        user_to_test_id = int(user_to_test.id)

        self.client.post('/account/auth/', {'username': user_to_test.username, 'password': 'johnpassword'}, follow=True)

    def test_user_login_page_loads(self):

        response = self.client.get('/account/login/', follow=True)

        assert response.status_code == 200

    def test_user_can_sucessfully_login(self):

        user_to_test = User.objects.get(username="john")

        user_to_test_id = int(user_to_test.id)

        self.client.post('/account/auth/', {'username': user_to_test.username, 'password': 'johnpassword'}, follow=True)

        assert (int(self.client.session['_auth_user_id']) == user_to_test_id)

    def test_user_has_a_manager(self):

        user_object = User.objects.get(username="bob")
        manager_object = User.objects.get(username="john")

        employee_manager = Employee.objects.get(user=user_object)

        assert (employee_manager.manager == manager_object)

    def test_user_can_access_profile_page(self):

        response = self.client.get('/account/profile/', follow=True)

        assert (response.status_code == 200)

    def test_user_addresses_appear_correctly(self):

        manager_object = User.objects.get(username="john")

        value_to_test = '"house_name": "St Swithun"'

        created_address = ADDRESSES(
            created_at = datetime.datetime.today().date(),
            updated_at = datetime.datetime.today().date(),
            address_name = "Home",
            house_name = "St Swithun",
            address_1 = "Test st swithun 1234",
            address_2 = "Test st swithun 1234",
            city = "Test st swithun 1234",
            county = "Test st swithun 1234",
            postcode = "BN17TA",
            user_id = manager_object
            )

        created_address.save()

        response = self.client.get('/account/profile/', follow=True)

        response = self.client.post('/account/addresses/', follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        address_response = json.loads(response.content)

        if value_to_test in address_response:
            assert True
        else:
            assert False

    def test_address_leave_remaining_appears(self):

        leave_remaining_value = '"leave_remaining\\": 25'

        user_object = User.objects.get(username="john")

        self.client.post('/account/auth/', {'username': user_object.username, 'password': 'johnpassword'}, follow=True)

        response = self.client.get('/account/profile/', follow=True)

        response = self.client.get('/account/leavedetails/', follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        leave_remaining_response = str(response.content)

        if leave_remaining_value in leave_remaining_response:
            assert True
        else:
            assert False

    def test_address_leave_entitlement_appears(self):

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

    def test_personal_information_is_correctly_loaded(self):

        manager_email = 'lennon@thebeatles.com'

        response = self.client.get('/account/profile/', follow=True)

        if manager_email in str(response.content):
            assert True
        else:
            assert False

    def test_team_information_is_correctly_loaded(self):

        value_to_test = '"team_name\\": \\"test_team\\"'

        user_to_test = User.objects.get(username="john")

        self.client.post('/account/auth/', {'username': user_to_test.username, 'password': 'johnpassword'}, follow=True)

        response = self.client.get('/account/profile/', follow=True)

        response = self.client.get('/account/organisationinformation/', follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        #assert self.assertEqual(response.content, "test")

        if value_to_test in str(response.content):
            assert True
        else:
            assert False

    def test_organisation_information_is_correctly_loaded(self):

        value_to_test = '"organisation_name\\": \\"test_organisation\\"'

        user_to_test = User.objects.get(username="john")

        self.client.post('/account/auth/', {'username': user_to_test.username, 'password': 'johnpassword'}, follow=True)

        response = self.client.get('/account/profile/', follow=True)

        response = self.client.get('/account/organisationinformation/', follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        #assert self.assertEqual(response.content, "test")

        if value_to_test in str(response.content):
            assert True
        else:
            assert False

    def test_addresses_can_be_changed(self):

        user_to_test = User.objects.get(username="john")

        created_address = ADDRESSES(
            created_at = datetime.datetime.today().date(),
            updated_at = datetime.datetime.today().date(),
            address_name = "Home",
            house_name = "St Swithun",
            address_1 = "Test st swithun 1234",
            address_2 = "Test st swithun 1234",
            city = "Test st swithun 1234",
            county = "Test st swithun 1234",
            postcode = "BN17TA",
            user_id = user_to_test
            )

        created_address.save()

        self.client.post('/account/auth/', {'username': user_to_test.username, 'password': 'johnpassword'}, follow=True)

        response = self.client.get('/account/profile/', follow=True)

        response = self.client.post('/account/addresses/', follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        response = self.client.get('/account/profile/', follow=True)

        address_id = 1
        house_name = "Test House Name"
        address_1 = "Address 1"
        address_2 = "Address 2"
        city = "City"
        county = "County"
        postcode = "PO17GB"

       # response = self.client.post('/account/editaddress/',{'address_id':int(address_id), 'house_name':house_name, 'address_1':address_1, 'address_2':address_2, 'city':city, 'county':county, 'postcode':postcode} , follow=True, content_type='application/json',**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        assert self.assertEqual(response.content, "test")














