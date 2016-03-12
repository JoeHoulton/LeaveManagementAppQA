from django.shortcuts import render

import time
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponse
import datetime
from django.http import Http404
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import json
import logging
from dateutil.relativedelta import relativedelta

from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

from django.template.loader import get_template
from django.template import Context

from LeaveManagementAppQA.cal.models import LEAVE_EVENTS
from LeaveManagementAppQA.accounts.models import Employee
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    c = {}
    c.update(csrf(request))

    return render_to_response('dashboard.html', c)

@csrf_exempt
def leave_request_submit(request):

    approved_records = ["successful"]

    chosen_approver_type = "on"

    username = request.user

    user_id = request.user
    firstname = request.user.first_name

    leave_type = request.POST.get('leaveType','')
    start_date = request.POST.get('start_date','')
    end_date = request.POST.get('end_date','')
    start_date_start_time = request.POST.get('start_date_start_time','')
    end_date_start_time = request.POST.get('end_date_start_time','')
    leave_reason = request.POST.get('leave_reason','')
    approval_type = request.POST.get('approval_type','')
    leave_status = "Pending"

    start_date = datetime.datetime.strptime(start_date, "%d/%m/%Y").strftime("%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y").strftime("%Y-%m-%d")

    #check if user doesnt already have a leave event in that time period



    if leave_event_is_less_than_six_months_in_the_past(start_date):

        leave_event = LEAVE_EVENTS(
                        title = leave_type,
                        snippet = leave_reason,
                        body = leave_reason,
                        start_date = start_date,
                        end_date = end_date,
                        start_time = start_date_start_time,
                        end_time = end_date_start_time,
                        status = leave_status,
                        creator_id = user_id,
                        remind = False
                        )

        logger.error("Result of leave_event_is_less_days_than_user_has_remaining " +  str(leave_event_is_less_days_than_user_has_remaining(leave_event, user_id.id)))

        if user_does_not_have_another_leave_request_in_that_time_period(leave_event, user_id):

            if leave_event_is_less_days_than_user_has_remaining(leave_event, user_id.id) == True:

                leave_event.save()

                leave_event_id = leave_event.id

                send_simple_manager_notification(username, leave_type, start_date, end_date, start_date_start_time, end_date_start_time, leave_reason, leave_event_id)
                send_simple_user_notification(username, leave_type, start_date, end_date, start_date_start_time, end_date_start_time, leave_reason, leave_event_id)

            else:
                approved_records = ["unsucessful", "Leave Event requested is more days than you have remaining."]

        else:
            approved_records = ["unsucessful", "Leave Event requested is occurs at the same time as another request. It is not possible to have two leave events occuring at the same time."]

    else:
        approved_records = ["unsucessful", "Leave Event requested is more than six months in the past."]


    if request.is_ajax():
        data = json.dumps(approved_records)
        return HttpResponse(data, content_type="application/json")
    else:
        raise Http404

@login_required
def get_personal_leave_requests_ajax(request):
    leave_request_dictionary = {}
    leave_request_records = []

    pending_state = "Pending"
    approved_state = "Approved"

    pending_event_count = 0
    approved_event_count = 0

    user_id = request.user

    pending_event_count = LEAVE_EVENTS.objects.filter(creator_id=user_id).filter(status=pending_state).count()
    approved_event_count = LEAVE_EVENTS.objects.filter(creator_id=user_id).filter(status=approved_state).count()

    leave_request_dictionary = {
            'pending_leave_event_count': pending_event_count,
            'approved_leave_event_count': approved_event_count,
        }

    leave_request_records.append(leave_request_dictionary)

    if request.is_ajax():
        data = json.dumps(leave_request_records)
        return HttpResponse(data, content_type="application/json")
    else:
        raise Http404

@login_required
def get_personal_approved_leave_requests_ajax(request):
    leave_request_dictionary = {}
    leave_request_records = []

    approved_state = "Approved"

    leave_event_count = 0

    user_id = request.user.id
    all_leave_events = LEAVE_EVENTS.objects.all()

    for leave_event in all_leave_events:
        if str(leave_event.creator_id) == str(user_id):
            if leave_event.status == approved_state:
                leave_event_count = leave_event_count + 1
                leave_request_dictionary = {
                    'approved_event_count': leave_event_count,
                }


    leave_request_records.append(leave_request_dictionary)

    if request.is_ajax():
        data = json.dumps(leave_request_records)
        return HttpResponse(data, content_type="application/json")
    else:
        raise Http404

@login_required
def get_team_leave_requests(request):

    leave_request_dictionary = {}
    leave_request_records = []

    requests_to_approve_count = 0;
    pending_state = "Pending";

    #gets username of logged in user
    user_username = request.user

    pending_state = "Pending"

    current_username = ""

    #gets employees that the user manages
    set_of_managed_users = Employee.objects.filter(manager__exact=user_username)

    for managed_user in set_of_managed_users:
        managed_user_id = managed_user.user_id

        current_username = User.objects.get(pk=managed_user_id)

        requests_to_approve_count = requests_to_approve_count + LEAVE_EVENTS.objects.filter(creator_id=current_username).filter(status=pending_state).count()

    leave_request_dictionary = {'requests_to_approve_count': requests_to_approve_count,
            }

    leave_request_records.append(leave_request_dictionary)

    if request.is_ajax():
        data = json.dumps(leave_request_records)
        return HttpResponse(data, content_type="application/json")
    else:
        raise Http404

@login_required
def get_bradford_factor(request):
    bradford_factor_dictionary = {}
    bradford_factor_records = []

    approved_state = "Approved"
    sick_leave = "Sick Leave"

    number_of_sick_absences = 0
    days_of_sick_absence = 0

    bradford_factor = 0

    user_id = request.user
    all_leave_events = LEAVE_EVENTS.objects.filter(creator_id=user_id).filter(status=approved_state).filter(title=sick_leave)

    for leave_event in all_leave_events:

        number_of_sick_absences = number_of_sick_absences + 1

        leave_event_start_date = str(leave_event.start_date)
        leave_event_start_time = str(leave_event.start_time)
        leave_event_end_date = str(leave_event.end_date)
        leave_event_end_time = str(leave_event.end_time)

        days_of_sick_absence = ((datetime.datetime.strptime(leave_event_end_date, "%Y-%m-%d").date() - datetime.datetime.strptime(leave_event_start_date, "%Y-%m-%d").date()).days)

        if leave_event_start_time == "Lunchtime":
            days_of_sick_absence = (days_of_sick_absence - 0.5)

        if leave_event_end_time == "Lunchtime":
            days_of_sick_absence = (days_of_sick_absence - 0.5)


    bradford_factor = (number_of_sick_absences * number_of_sick_absences * days_of_sick_absence)

    bradford_factor_dictionary = {
        'bradford_factor': (bradford_factor),
    }


    bradford_factor_records.append(bradford_factor_dictionary)

    if request.is_ajax():
        data = json.dumps(bradford_factor_records)
        return HttpResponse(data, content_type="application/json")
    else:
        raise Http404



def send_simple_manager_notification(username, leave_type, start_date, end_date, start_date_start_time, end_date_start_time, leave_reason, leave_event_id):

    manager_email = get_manager_email(username)


    if manager_is_currently_on_holiday(username):
        managers_manager_object = get_manager(get_manager(username).username)
        manager_email = get_manager_email(managers_manager_object.username)

    else:
        manager_email = get_manager_email(username)


    plaintext = get_template('manager_notification.txt')
    htmly     = get_template('manager_notification.html')

    d = Context({ 'username': username, 'first_name': username.first_name, 'last_name': username.last_name, 'leave_type':leave_type,
                  'start_date': start_date, 'end_date': end_date, 'start_time': start_date_start_time, 'end_time': end_date_start_time,
                  'reason': leave_reason, 'ID': leave_event_id})

    subject, from_email, to = 'Leave Request From', 'LeaveCal <postmaster@sandboxb59750eb67074ec3bfcc9a8926bad0d1.mailgun.org>', manager_email
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_simple_user_notification(username_passed, leave_type, start_date, end_date, start_date_start_time, end_date_start_time, leave_reason, leave_event_id):

    user_email = (User.objects.filter(username=username_passed)[0].email)

    plaintext = get_template('user_notification.txt')
    htmly     = get_template('user_notification.html')

    d = Context({ 'username': username_passed, 'first_name': username_passed.first_name, 'last_name': username_passed.last_name, 'leave_type':leave_type,
                  'start_date': start_date, 'end_date': end_date, 'start_time': start_date_start_time, 'end_time': end_date_start_time,
                  'reason': leave_reason, 'ID': leave_event_id})

    subject, from_email, to = 'Leave Request Submitted', 'LeaveCal <postmaster@sandboxb59750eb67074ec3bfcc9a8926bad0d1.mailgun.org>', str(user_email)
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def get_manager_email(username_of_managed_user):

    id_of_current_user = User.objects.get(username=username_of_managed_user).id

    id_of_manager = Employee.objects.get(user=id_of_current_user).manager

    manager_email = (User.objects.get(username=id_of_manager).email)

    return str(manager_email)

def get_manager(username_of_managed_user):

    id_of_current_user = User.objects.get(username=username_of_managed_user).id

    id_of_manager = Employee.objects.get(user=id_of_current_user).manager

    manager_object = (User.objects.get(username=id_of_manager))

    logger.error("Manager is: " + str(manager_object))

    return manager_object


def leave_event_is_less_than_six_months_in_the_past(start_date_of_leave_event):

    six_months_in_the_past = datetime.datetime.today().date() - relativedelta(months=6)

    start_date_minus_six_months = datetime.datetime.strptime(start_date_of_leave_event, '%Y-%m-%d').date()

    logger.error("SIX MONTHS IN THE PAST: " + str(six_months_in_the_past))
    logger.error("start_date_minus_six_months " + str(six_months_in_the_past))

    if six_months_in_the_past > start_date_minus_six_months:
        return False
    else:
        return True

def leave_event_is_less_days_than_user_has_remaining(leave_event_to_calculate, current_user_id):

    number_of_days = calculate_days_of_leave_event(leave_event_to_calculate)

    leave_remaining_for_employee = Employee.objects.get(user=str(current_user_id)).leave_remaining

    logger.error("Number of days " + str(number_of_days))
    logger.error("Number of days remaining" + str(leave_remaining_for_employee))

    if number_of_days <= leave_remaining_for_employee:
        return True
    else:
        return False

def calculate_days_of_leave_event(leave_event):

    leave_event_start_date = str(leave_event.start_date)
    leave_event_start_time = str(leave_event.start_time)
    leave_event_end_date = str(leave_event.end_date)
    leave_event_end_time = str(leave_event.end_time)

    days_of_leave_event = ((datetime.datetime.strptime(leave_event_end_date, "%Y-%m-%d").date() - datetime.datetime.strptime(leave_event_start_date, "%Y-%m-%d").date()).days)

    if leave_event_start_time == "Lunchtime":
        days_of_leave_event = (days_of_leave_event - 0.5)

    if leave_event_end_time == "Lunchtime":
        days_of_leave_event = (days_of_leave_event - 0.5)

    return days_of_leave_event

def user_does_not_have_another_leave_request_in_that_time_period(leave_event_to_calculate, username):

    six_months_in_the_past = datetime.datetime.today().date() - relativedelta(months=6)
    # get all leave events for user
    # get span of dates
    # If dates are the same check span of dates not within start and end date of user, taking into account Lunchtime event

    start_date_of_leave_event = datetime.datetime.strptime(leave_event_to_calculate.start_date, '%Y-%m-%d').date()
    end_date_of_leave_event = datetime.datetime.strptime(leave_event_to_calculate.end_date, '%Y-%m-%d').date()
    start_time_of_leave_event = str(leave_event_to_calculate.start_time)
    end_time_of_leave_event = str(leave_event_to_calculate.end_time)

    logger.error("Found Start Date: " + str(start_date_of_leave_event))
    logger.error("Found End Date: " + str(end_date_of_leave_event))
    logger.error("Found Start Time: " + str(start_time_of_leave_event))
    logger.error("Found End Time: " + str(end_time_of_leave_event))

    leave_events_for_current_user = LEAVE_EVENTS.objects.filter(creator_id=username).exclude(status="Cancelled").exclude(status="Declined")

    events_dont_clash = True

    for leave_event in leave_events_for_current_user:

        logger.error("FOUND A LEAVE EVENT: " + str(leave_event.status))

        start_date_of_current_leave_event = leave_event.start_date
        end_date_of_current_leave_event = leave_event.end_date
        start_time_of_current_leave_event = str(leave_event.start_time)
        end_time_of_current_leave_event = str(leave_event.end_time)

        logger.error("Current Start date: " + str(leave_event.start_date))
        logger.error("Current End date: " + str(leave_event.end_date))

        logger.error("Do these dates match??: " + str(end_date_of_leave_event == start_date_of_current_leave_event))

        if (start_date_of_leave_event > start_date_of_current_leave_event) & (end_date_of_leave_event < end_date_of_current_leave_event):
            events_dont_clash = False

        elif (end_date_of_leave_event < end_date_of_current_leave_event):

            if (end_date_of_leave_event >= start_date_of_current_leave_event):

                if (end_date_of_leave_event == start_date_of_current_leave_event):

                    if (start_date_of_leave_event < start_date_of_current_leave_event):

                        if (start_time_of_current_leave_event == "Lunchtime") & (end_time_of_leave_event != "Lunchtime"):
                            events_dont_clash = False

        #elif (start_date_of_leave_event > start_date_of_current_leave_event):
        #    if (start_date_of_leave_event <= end_date_of_current_leave_event):
        #        events_dont_clash = False

         #   elif (start_date_of_leave_event == start_date_of_current_leave_event):
          #      if (end_time_of_leave_event != "Lunchtime") & (start_time_of_current_leave_event != "Lunchtime"):
           #         events_dont_clash = False

        elif (start_date_of_leave_event == end_date_of_current_leave_event):
            logger.error("GOT IN HERE 1")
            if (end_date_of_leave_event > end_date_of_current_leave_event):
                logger.error("GOT IN HERE 2")
                if (end_time_of_current_leave_event == "Lunchtime") & (start_time_of_leave_event != "Lunchtime"):
                    logger.error("GOT IN HERE 2.5")
                    events_dont_clash = False

        elif (start_date_of_leave_event == start_date_of_current_leave_event):
            if (end_date_of_leave_event == end_date_of_current_leave_event):
                if (start_time_of_current_leave_event == "Beginning of Day") & (end_time_of_current_leave_event == "End of Day"):
                    events_dont_clash = False
                elif (start_time_of_leave_event == "Beginning of Day") & (end_time_of_leave_event == "Lunchtime"):
                    if (start_time_of_leave_event != "Lunchtime") & (end_time_of_leave_event != "End of Day"):
                        events_dont_clash = False
                elif (start_time_of_current_leave_event == "Lunchtime") & (end_time_of_current_leave_event == "End of Day"):
                    if (start_time_of_leave_event != "Beginning of Day") & (end_time_of_leave_event != "Lunchtime"):
                        events_dont_clash = False
            else:
                events_dont_clash = False

        logger.error("Current state of the variable?: " + str(events_dont_clash))


    return events_dont_clash == True

def manager_is_currently_on_holiday(username_of_managed_user):

    logger.error("")

    manager_object = get_manager(username_of_managed_user)
    manager_username = str(manager_object.username)

    logger.error("2")

    todays_date = datetime.datetime.today().date()

    logger.error("3")

    current_set_of_leave_events = LEAVE_EVENTS.objects.exclude(status="Cancelled").exclude(status="Declined")

    logger.error("4")

    current_set_of_leave_events = LEAVE_EVENTS.objects.exclude(start_date__gte=todays_date).exclude(end_date__lte=todays_date)

    logger.error("5")

    new_set_of_leave_events = current_set_of_leave_events

    logger.error("6")

    manager_is_on_holiday = False

    logger.error("Current set: " + str(current_set_of_leave_events))

    while manager_is_on_holiday == False:
        for event in current_set_of_leave_events:
            if str(event.creator_id)!=str(manager_username):
                logger.error("7")
                manager_is_on_holiday == True
                #new_set_of_leave_events.remove(event)

    logger.error("length of array: " + len(new_set_of_leave_events))

    return manager_is_on_holiday

