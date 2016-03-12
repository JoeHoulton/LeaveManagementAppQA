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

from django.contrib.auth import views


from django.http import Http404, HttpResponse
import json

import logging

from LeaveManagementAppQA.accounts.models import Employee
from LeaveManagementAppQA.cal.models import ADDRESSES
from LeaveManagementAppQA.cal.models import LEAVE_EVENTS

logger = logging.getLogger(__name__)

def login(request):
    c = {}
    c.update(csrf(request))


    #return HttpResponseRedirect('/dashboard')

    return render_to_response('login.html', c)

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseRedirect('/account/invalid')

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

    address_dictionary = {}
    address_records = []

    #gets username of logged in user
    user_id = request.user

    #gets employees that the user manages
    set_of_addresses = ADDRESSES.objects.filter(user_id=request.user)

    for address in set_of_addresses:
        if user_id == address.user_id:

            address_dictionary = {
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

    return render_to_response('profile.html',
                              {"first_name":request.user.first_name,
                               "last_name":request.user.last_name,
                               "username":request.user,
                               "email":request.user.email
                              })


def get_addresses_ajax(request):
    address_dictionary = {}
    address_records = []

    id_of_logged_in_user = request.user

    set_of_addresses = ADDRESSES.objects.filter(user_id=id_of_logged_in_user)

    for address in set_of_addresses:
            address_dictionary = {
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

def get_leave_information_ajax(request):
    leave_information_dictionary = {}
    leave_information_records = []

    user_id = request.user.id

    set_of_employees = Employee.objects.all()

    for employee in set_of_employees:
        if str(user_id) == str(employee.user_id):

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

def change_password(request):
    template_response = views.password_change(request)
    # Do something with `template_response`
    return template_response
