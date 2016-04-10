from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

import json
import logging

from LeaveManagementAppQA.cal.models import LEAVE_EVENTS

logger = logging.getLogger(__name__)

@login_required()
def calendar_view(request):
    return render_to_response('agenda-views.html',{'username': request.user})

@login_required()
def date_picker_testing(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('date_picker_testing.html', c)

# Get all calendar events for logged in user and return these in JSON format
@login_required()
def get_cal_events(request):

    leave_request_dictionary = {}
    leave_request_records = []

    user_id = request.user
    cancelled_status = "Cancelled"

    user_leave_events = LEAVE_EVENTS.objects.filter(creator_id=user_id).exclude(status=cancelled_status)

    for leave_event in user_leave_events:

        start_date_for_leave_event = leave_event.start_date.strftime("%Y-%m-%d")
        end_date_for_leave_event = leave_event.end_date.strftime("%Y-%m-%d")
        start_time_for_leave_event = leave_event.start_time
        end_time_for_leave_event = leave_event.end_time
        title_for_leave_event = leave_event.title
        status_for_leave_event = leave_event.status
        reason_for_leave_event = leave_event.body

        leave_request_dictionary = {'start_date': start_date_for_leave_event,
                                    'end_date': end_date_for_leave_event,
                                    'start_time': start_time_for_leave_event.encode('ascii'),
                                    'end_time': end_time_for_leave_event.encode('ascii'),
                                    'title': title_for_leave_event.encode('ascii'),
                                    'leave_status':status_for_leave_event,
                                    'leave_reason':reason_for_leave_event
                                    }

        leave_request_records.append(leave_request_dictionary)


    data = json.dumps(leave_request_records)
    return HttpResponse(data, content_type="application/json")
