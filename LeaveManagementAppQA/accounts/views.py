from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import views


from django.http import Http404, HttpResponse
import json

import logging

from django.template import RequestContext

from LeaveManagementAppQA.accounts.models import Employee
from LeaveManagementAppQA.cal.models import ADDRESSES
from LeaveManagementAppQA.cal.models import LEAVE_EVENTS
from LeaveManagementAppQA.cal.models import ORGANISATIONS
from LeaveManagementAppQA.cal.models import TEAMS

logger = logging.getLogger(__name__)


# Login Page
# Ensure any parameters passed as "next" page are stored and passed to template.
def login(request):
    c = {}
    c.update(csrf(request))

    next_parameter = request.GET.get('next','')

    if next_parameter != '':
        next_dictionary = {'next_parameter':request.GET.get('next','')}
        c.update(next_dictionary)

    logger.error("Request Next parameter: " + str(request.GET.get('next','')))

    return render_to_response('login.html', c)

# Authenticate User
# Redirect to next parameter if one is provided
def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    next_parameter = request.POST.get('next','')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        if next_parameter != '':
            response = HttpResponseRedirect(next_parameter)
        else:
            response = HttpResponseRedirect('/dashboard')
    else:
        response = HttpResponseRedirect('/account/invalid')

    return response

def loggedin(request):
    return render_to_response('loggedin.html',
                              {'full_name': request.user.username})

def invalid_login(request):
    return render_to_response('invalid_login.html')

def logout(request):
    auth.logout(request)

    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)


@login_required()
def index(request):
    return render_to_response('profile.html',
                              {"first_name":request.user.first_name,
                               "last_name":request.user.last_name,
                               "username":request.user,
                               "email":request.user.email
                              })


# Get addresses of currently logged in user and return in JSON format
def get_addresses_ajax(request):
    address_dictionary = {}
    address_records = []

    id_of_logged_in_user = request.user

    set_of_addresses = ADDRESSES.objects.filter(user_id=id_of_logged_in_user)

    for address in set_of_addresses:
        address_dictionary = {
            "address_id":address.id,
            "address_name":address.address_name,
            "house_name":address.house_name,
            "address_1":address.address_1,
            "address_2":address.address_2,
            "city":address.city,
            "county":address.county,
            "postcode":address.postcode,
        }

        address_records.append(address_dictionary)

    address_records = simplejson.dumps(address_records)

    if request.is_ajax():
        data = json.dumps(address_records)
        return HttpResponse(data, content_type="application/json")
    else:
        raise Http404

# Get Leave Entitlement and Leave Remaining values and return as a JSON format.
def get_leave_information_ajax(request):
    leave_information_dictionary = {}
    leave_information_records = []

    user_object = request.user

    employee = Employee.objects.get(user=user_object)

    leave_information_dictionary = {
        "leave_entitlement":employee.leave_entitlement,
        "leave_remaining":employee.leave_remaining,
    }

    leave_information_records.append(leave_information_dictionary)

    leave_information_records = simplejson.dumps(leave_information_records)

    if request.is_ajax():
        data = json.dumps(leave_information_records)
        return HttpResponse(data, content_type="application/json")
    else:
        raise Http404

# Get addresses of currently logged in user and return in JSON format
def get_user_organisation_and_team(request):
    leave_information_dictionary = {}
    leave_information_records = []

    user_object = request.user

    employee = Employee.objects.get(user=user_object)

    logger.error("Employee: " + str(employee.team_name.id))

    team_name = TEAMS.objects.get(id=employee.team_name.id).team_name
    organisation_name = ORGANISATIONS.objects.get(id=employee.organisation.id).organisation_name

    logger.error("TEAM NAME FOR USER: " + str(team_name))
    logger.error("Organisation NAME FOR USER: " + str(organisation_name))

    leave_information_dictionary = {
        "team_name": str(team_name),
        "organisation_name": str(organisation_name),
    }

    leave_information_records.append(leave_information_dictionary)

    leave_information_records = simplejson.dumps(leave_information_records)

    if request.is_ajax():
        data = json.dumps(leave_information_records)
        return HttpResponse(data, content_type="application/json")
    else:
        raise Http404

# Set address according to the values the user has entered into the form
@csrf_exempt
def edit_address(request):
    leave_information_records = ["updated"]

    address_id = request.POST.get('address_id', '')
    house_name = request.POST.get('house_name', '')
    address_1 = request.POST.get('address_1', '')
    address_2 = request.POST.get('address_2', '')
    city = request.POST.get('city', '')
    county = request.POST.get('county', '')
    postcode = request.POST.get('postcode', '')

    current_address_object = ADDRESSES.objects.get(id=address_id)

    current_address_object.house_name = house_name
    current_address_object.address_1 = address_1
    current_address_object.address_2 = address_2
    current_address_object.city = city
    current_address_object.county = county
    current_address_object.postcode = postcode

    current_address_object.save()

    logger.error("Current Address Object: " + str(current_address_object.id))

    logger.error("Address ID: " + str(address_id))
    logger.error("House Name: " + str(house_name))
    logger.error("Address 1: " + str(address_1))
    logger.error("Address 2: " + str(address_2))
    logger.error("City: " + str(city))
    logger.error("County: " + str(county))
    logger.error("Postcode: " + str(postcode))

    leave_information_records = simplejson.dumps(leave_information_records)

    if request.is_ajax():
        data = json.dumps(leave_information_records)
        return HttpResponse(data, content_type="application/json")
    else:
        raise Http404

# Implementing Django build in change password functionality
def change_password(request):
    template_response = views.password_change(request)
    return template_response
