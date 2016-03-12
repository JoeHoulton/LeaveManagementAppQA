import time
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import Http404, HttpResponse
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


from models import *

month_names = "January Febuary March April May June July August September October November December"
month_names = month_names.split()


@login_required
def main(request, year=None):
    """Main listing, years and months; three years per page."""
    # prev / next years

    if year:
        year = int(year)
    else:
        year = time.localtime()[0]

    now_year, now_month = time.localtime()[:2]
    lst = []

    # create a list of months for each year, indicating ones that contain entries and current
    for y in [year, year+1, year+2]:
        mlst = []
        for n, month in enumerate(month_names):
            entry = current = False
            entries = LEAVE_EVENTS.objects.filter(start_date__year=y, end_date__month=n+1)

            if entries:
                entry = True
            if y == now_year and n+1 == now_month:
                current = True
            mlst.append(dict(n=n+1, name=month, entry=entry, current=current))
        lst.append((y, mlst))

    return render_to_response("main.html", dict(years=lst, user=request.user, year=year))

@login_required()
def calendar_view(request):
    language = 'en-gb'
    session_language = 'en-gb'

    if 'lang' in request.COOKIES:
        language = request.COOKIES['lang']

    if 'lang' in request.session:
        session_language = request.session['lang']

    return render_to_response('agenda-views.html',{'language': language,'session_language': session_language})


@login_required()
def date_picker_testing(request):

    c = {}
    c.update(csrf(request))
    return render_to_response('date_picker_testing.html', c)

@login_required()
def language(request, language='en-gb'):
    response = HttpResponse('setting language to %s' % language)

    response.set_cookie('lang', language)

    request.session['lang'] = language

    return response

@login_required()
def event_add_auth(request):

    event_name = request.POST.get('event_name', '')
    event_start_date = request.POST.get('start_date', '')
    event_end_date = request.POST.get('end_date', '')

    title = models.CharField(max_length=40)
    snippet = models.CharField(max_length=150, blank=True)
    reason = models.TextField(max_length=400, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    creator = models.ForeignKey(User, blank=True, null=True)

    event_start_date = datetime.strptime(event_start_date, '%d/%m/%Y').strftime('%Y-%m-%d')
    event_end_date = datetime.strptime(event_end_date, '%d/%m/%Y').strftime('%Y-%m-%d')

    new_entry = LEAVE_EVENTS(title=event_name, snippet="test", body="this is the reason for the request",start_date=event_start_date, end_date=event_end_date)
    new_entry.save()

    return HttpResponseRedirect('/event/success')

@login_required()
def get_cal_events(request):

    leave_request_dictionary = {}
    leave_request_records = []

    user_id = request.user

    user_leave_events = LEAVE_EVENTS.objects.filter(creator_id=user_id)

    for leave_event in user_leave_events:

        start_date_for_leave_event = leave_event.start_date.strftime("%Y-%m-%d")
        end_date_for_leave_event = leave_event.end_date.strftime("%Y-%m-%d")
        start_time_for_leave_event = leave_event.start_time
        end_time_for_leave_event = leave_event.end_time
        title_for_leave_event = leave_event.title

        leave_request_dictionary = {'start_date': start_date_for_leave_event,
                                        'end_date': end_date_for_leave_event,
                                        'start_time': start_time_for_leave_event.encode('ascii'),
                                        'end_time': end_time_for_leave_event.encode('ascii'),
                                        'title': title_for_leave_event.encode('ascii')
                                        }

        leave_request_records.append(leave_request_dictionary)


    data = json.dumps(leave_request_records)
    return HttpResponse(data, content_type="application/json")



@login_required()
def event_add_successful(request):

    return render_to_response('event_add_successful.html')
