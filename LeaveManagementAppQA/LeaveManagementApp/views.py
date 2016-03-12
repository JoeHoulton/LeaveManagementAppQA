from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf

def index(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)
