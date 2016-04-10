from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from decimal import Decimal

import datetime
import json
import logging

from LeaveManagementAppQA.cal.models import LEAVE_EVENTS
from LeaveManagementAppQA.accounts.models import Employee
from django.contrib.auth.models import User


logger = logging.getLogger(__name__)

@login_required()
def leave_requests(request):

    c = {'username':request.user}
    c.update(csrf(request))

    return render_to_response('request_leave_page.html', c)

@login_required()
def get_personal_requests(request):

    return render_to_response('user_requests.html', {'username':request.user})

@login_required()
def get_team_requests(request):

    return render_to_response('team_requests.html' , {'username':request.user})

# Get all Leave Requests to approve for currently looged in user
@login_required()
def get_team_leave_requests(request):
    leave_request_dictionary = {}
    leave_request_records = []

    #gets username of logged in user
    user_username = request.user

    pending_state = "Pending"

    managed_user_firstname = "firstname"
    managed_user_lastname = "lastname"

    #gets employees that the user manages
    set_of_managed_users = Employee.objects.filter(manager__exact=user_username)

    # If leave events are in a pending state, add them to the dictionary and send them back to the user
    for managed_user in set_of_managed_users:
        managed_user_id = managed_user.user_id

        logger.error("Found this: " + str(User.objects.get(pk=managed_user_id)))

        current_user = User.objects.get(pk=managed_user_id)

        managed_user_firstname = str(current_user.first_name)
        managed_user_lastname = str(current_user.last_name)

        logger.error("Getting here")

        all_leave_events =  LEAVE_EVENTS.objects.filter(creator_id=current_user).filter(status=pending_state)

        logger.error("Getting here 2")

        for leave_event in all_leave_events:
            leave_request_dictionary = {'start_date': str(leave_event.start_date),
                                        'end_date': str(leave_event.end_date),
                                        'start_time': str(leave_event.start_time),
                                        'end_time': str(leave_event.end_time),
                                        'title': str(leave_event.title),
                                        'reason': str(leave_event.body),
                                        'status': str(leave_event.status),
                                        'name': str(managed_user_firstname + " " + managed_user_lastname),
                                       'leave_id': str(leave_event.id),
                                       }

            leave_request_records.append(leave_request_dictionary)

    if request.is_ajax():
        data = json.dumps(leave_request_records)
        return HttpResponse(data, content_type="application/json")
    else:
        raise Http404

# Get nearest approved Leave Request for all users in the same team as the currently logged in user
@login_required()
def get_all_team_leave_requests(request):
    leave_request_dictionary = {}
    leave_request_records = []

    same_organisation_and_same_team_user_objects = []

    current_user_nearest_leave_event_start_date = ""
    current_user_nearest_leave_event_end_date = ""
    current_user_nearest_leave_event_start_time = ""
    current_user_nearest_leave_event_end_time = ""
    current_user_nearest_leave_event_title = ""
    current_user_nearest_leave_event_body = ""
    current_user_nearest_leave_event_status = ""

    #gets username of logged in user
    user_id = request.user.id
    username =request.user

    approved_state = "Approved"

    team_user_firstname = "firstname"
    team_user_lastname = "lastname"

    todays_date = datetime.datetime.now().date()
    #get employees team and organisation name

    current_employee = Employee.objects.get(user=user_id)

    current_user_team = current_employee.team_name
    current_user_organisation = current_employee.organisation

    #get employees that are on the same team and same organisation as the user

    set_of_team_employees = Employee.objects.filter(team_name=current_user_team).filter(organisation=current_user_organisation).exclude(user=username)

    for employee in set_of_team_employees:
        same_organisation_and_same_team_user_objects.append(employee)

    # get all leave events for the matched employees
    for matched_employee in same_organisation_and_same_team_user_objects:

        # get first and surnames of the users

        user_object = User.objects.get(pk=(matched_employee.user_id))

        team_user_firstname = user_object.first_name
        team_user_lastname = user_object.last_name

        # get all leave events and determine which one is happening closest to the current date

        dummy_date = datetime.date(2900, 3, 11)

        current_nearest_leave_event_id = 0
        current_nearest_leave_event_start_date = dummy_date
        current_nearest_leave_event_start_time = ""

        all_leave_events = LEAVE_EVENTS.objects.filter(creator_id=user_object).filter(status=approved_state)

        for leave_event in all_leave_events:

            # get start date,start time
            # store these
            # if current leave event is less that start date start time, store ID of leave event

            if (leave_event.start_date >= todays_date):
                if (leave_event.start_date <= current_nearest_leave_event_start_date) or (current_nearest_leave_event_start_date == dummy_date):

                    current_nearest_leave_event_start_date = leave_event.start_date
                    current_nearest_leave_event_id = leave_event.id

                    if (current_nearest_leave_event_start_time != "Beginning of Day") and (str(leave_event.start_time) == "Beginning of Day"):
                        current_nearest_leave_event_start_time = str(leave_event.start_time)

        # outside of all leave events, get details of that leave event
        logger.error("This is the content of the current nearest leave id " + str(current_nearest_leave_event_id))

        if current_nearest_leave_event_id != 0:

            current_user_nearest_leave_event = LEAVE_EVENTS.objects.get(id=current_nearest_leave_event_id)
            current_user_nearest_leave_event.start_date

            current_user_nearest_leave_event_start_date = current_user_nearest_leave_event.start_date
            current_user_nearest_leave_event_end_date = current_user_nearest_leave_event.end_date
            current_user_nearest_leave_event_start_time = current_user_nearest_leave_event.start_time
            current_user_nearest_leave_event_end_time = current_user_nearest_leave_event.end_time
            current_user_nearest_leave_event_title = current_user_nearest_leave_event.title
            current_user_nearest_leave_event_body = current_user_nearest_leave_event.body
            current_user_nearest_leave_event_status = current_user_nearest_leave_event.status

        else:
            current_user_nearest_leave_event_start_date = ""
            current_user_nearest_leave_event_end_date = ""
            current_user_nearest_leave_event_start_time = ""
            current_user_nearest_leave_event_end_time = ""
            current_user_nearest_leave_event_title = ""
            current_user_nearest_leave_event_body = ""
            current_user_nearest_leave_event_status = ""


        leave_request_dictionary = {'start_date': str(current_user_nearest_leave_event_start_date),
                                    'end_date': str(current_user_nearest_leave_event_end_date),
                                    'start_time': str(current_user_nearest_leave_event_start_time),
                                    'end_time': str(current_user_nearest_leave_event_end_time),
                                    'title': str(current_user_nearest_leave_event_title),
                                    'reason': str(current_user_nearest_leave_event_body),
                                    'status': str(current_user_nearest_leave_event_status),
                                    'name': str(team_user_firstname + " " + team_user_lastname),
                                    }

        leave_request_records.append(leave_request_dictionary)



    if request.is_ajax():
        data = json.dumps(leave_request_records)
        return HttpResponse(data, content_type="application/json")
    else:
        raise Http404


# Get all Leave Requests for the currently logged in user
@login_required()
def get_personal_leave_requests_ajax(request):
    leave_request_dictionary = {}
    leave_request_records = []

    user_id = request.user
    all_leave_events = LEAVE_EVENTS.objects.filter(creator_id=user_id)

    for leave_event in all_leave_events:

        leave_request_dictionary = {'start_date': str(leave_event.start_date),
                                'title':str(leave_event.title),
                                'end_date': str(leave_event.end_date),
                                'start_time': str(leave_event.start_time),
                                'end_time': str(leave_event.end_time),
                                'title': str(leave_event.title),
                                'reason': str(leave_event.body),
                                'status': str(leave_event.status),
                                'leave_id': str(leave_event.id),
                                }

        leave_request_records.append(leave_request_dictionary)

    if request.is_ajax():
        data = json.dumps(leave_request_records)
        return HttpResponse(data, content_type="application/json")
    else:
        raise Http404

# Set status for leave event
@csrf_exempt
def approve_leave_local(request):

    approved_records = ["approved"]

    approved = "Approved"
    declined = "Declined"

    approved_button_name = "approved_button"
    declined_button_name = "declined_button"

    request_leave_event_id = request.POST.get('leave_id', '')
    request_button_name = request.POST.get('name', '')

    leave_event_for_approval = LEAVE_EVENTS.objects.get(id=int(request_leave_event_id))
    requesting_employee = Employee.objects.get(user=leave_event_for_approval.creator_id)

    current_user_object = User.objects.get(username=leave_event_for_approval.creator_id)

    if request_button_name == approved_button_name:
        logger.error("Im getting the bit where leave is decremented")

        leave_event_total_days = calculate_days_of_leave_event(leave_event_for_approval)

        logger.error("Leave Event Total Days: " + str(leave_event_total_days))

        updated_leave_remaining = (requesting_employee.leave_remaining - Decimal(leave_event_total_days))

        logger.error("Leave Remaining Days: " + str(updated_leave_remaining))

        requesting_employee.leave_remaining = updated_leave_remaining

        leave_event_for_approval.status = approved
        requesting_employee.save()

        send_leave_event_approved_notification(current_user_object,leave_event_for_approval)

    elif request_button_name == declined_button_name:
        leave_event_for_approval.status = declined
        send_leave_event_declined_notification(current_user_object, leave_event_for_approval)

    leave_event_for_approval.save()

    if request.is_ajax():
        data = json.dumps(approved_records)
        return HttpResponse(data, content_type="application/json")
    else:
        raise Http404

# Set status for leave event to cancelled
@csrf_exempt
def cancel_leave(request):

    approved_records = ["Cancelled"]

    approved = "Approved"
    declined = "Declined"
    cancelled = "Cancelled"
    pending = "Pending"

    approved_button_name = "approved_button"
    declined_button_name = "declined_button"

    request_user_id = request.POST.get('leave_id', '')

    logger.error("Testing Cancelled Testing: " + str(request_user_id))

    current_leave_event_id_of_user = User.objects.get(username=request.user.username).id

    leave_event_to_cancel = LEAVE_EVENTS.objects.filter(pk=request_user_id)[0]

    current_employee = Employee.objects.get(user=current_leave_event_id_of_user)

    if leave_event_to_cancel.status == approved:

        logger.error("I GOT IN HERE DURING TESTING")

        leave_event_total_days = calculate_days_of_leave_event(leave_event_to_cancel)

        logger.error("I GOT IN HERE DURING TESTING 1")

        updated_leave_remaining = (current_employee.leave_remaining + Decimal(leave_event_total_days))

        logger.error("I GOT IN HERE DURING TESTING 2")

        current_employee.leave_remaining = updated_leave_remaining

        leave_event_to_cancel.status = cancelled

        logger.error("I GOT IN HERE DURING TESTING 3")

    elif leave_event_to_cancel.status == pending:

        leave_event_to_cancel.status = cancelled

    current_employee.save()

    leave_event_to_cancel.save()


    if request.is_ajax():
        data = json.dumps(approved_records)
        return HttpResponse(data, content_type="application/json")
    else:
        raise Http404

# Determine the number of days the leave event spans
def calculate_days_of_leave_event(leave_event):

    leave_event_start_date = str(leave_event.start_date)
    leave_event_start_time = str(leave_event.start_time)
    leave_event_end_date = str(leave_event.end_date)
    leave_event_end_time = str(leave_event.end_time)

    days_of_leave_event = ((datetime.datetime.strptime(leave_event_end_date, "%Y-%m-%d").date() - datetime.datetime.strptime(leave_event_start_date, "%Y-%m-%d").date()).days)

    logger.error("Calculated Days of Leave Event: " + str(days_of_leave_event))

    if days_of_leave_event == 0:
        days_of_leave_event = days_of_leave_event + 1

    if leave_event_start_time == "Lunchtime":
        days_of_leave_event = (days_of_leave_event - 0.5)

    if leave_event_end_time == "Lunchtime":
        days_of_leave_event = (days_of_leave_event - 0.5)

    return days_of_leave_event

def send_leave_event_approved_notification(user_object, leave_event):

    logger.error("Got in email 1:")

    plaintext = get_template('request_approved_notification.txt')
    htmly     = get_template('request_approved_notification.html')

    logger.error("Got in email 2:")

    d = Context({ 'username': user_object.username, 'first_name': user_object.first_name, 'last_name': user_object.last_name, 'leave_type':leave_event.title,
                  'start_date': str(leave_event.start_date), 'end_date': str(leave_event.end_date), 'start_time': str(leave_event.start_time), 'end_time': str(leave_event.end_time),
                  'reason': str(leave_event.body), 'ID': str(leave_event.id)})

    logger.error("Got in email 3:")

    subject = 'Leave Request Approved'
    from_email = 'LeaveCal <postmaster@sandboxb59750eb67074ec3bfcc9a8926bad0d1.mailgun.org>'
    logger.error("Before Start of message")
    to = str(user_object.email)
    logger.error("Start of message")
    text_content = plaintext.render(d)
    logger.error("Middle of message")
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    logger.error("Message has been sent")

def send_leave_event_declined_notification(user_object, leave_event):

    logger.error("Got in email 1:")

    plaintext = get_template('request_declined_notification.txt')
    htmly     = get_template('request_declined_notification.html')

    logger.error("Got in email 2:")

    d = Context({ 'username': user_object.username, 'first_name': user_object.first_name, 'last_name': user_object.last_name, 'leave_type':leave_event.title,
                  'start_date': str(leave_event.start_date), 'end_date': str(leave_event.end_date), 'start_time': str(leave_event.start_time), 'end_time': str(leave_event.end_time),
                  'reason': str(leave_event.body), 'ID': str(leave_event.id)})

    logger.error("Got in email 3:")

    subject = 'Leave Request Declined'
    from_email = 'LeaveCal <postmaster@sandboxb59750eb67074ec3bfcc9a8926bad0d1.mailgun.org>'
    logger.error("Before Start of message")
    to = str(user_object.email)
    logger.error("Start of message")
    text_content = plaintext.render(d)
    logger.error("Middle of message")
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    logger.error("Message has been sent")
