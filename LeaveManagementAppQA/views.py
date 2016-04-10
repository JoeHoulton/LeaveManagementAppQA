from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
import logging

from django.template import RequestContext

logger = logging.getLogger(__name__)


# Index page
def index(request):
    c = {}
    c.update(csrf(request))

    if request.user.is_authenticated():
        logger.error("Is authentecated")
        response = HttpResponseRedirect('/dashboard')
        return response
    else:
        logger.error("Is not authentecated")
        return render_to_response('login.html', c)


# 404 error handler (Not in use)
def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

