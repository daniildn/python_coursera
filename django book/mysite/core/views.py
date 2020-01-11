# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import  django
# Create your views here.
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response

def hello(request):
    return HttpResponse("hello  world")


def current_time(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {'current_date': now})


def count_time(request, operation):
    operation = str(operation)
    operation = operation.split("/")
    try:
        offset = int(operation[1])
    except ValueError:
        raise Http404()

    if (operation[0] == 'plus'):
        dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
        offset = "Через %s" % (offset)
    elif (operation[0] == "minus"):
        dt = datetime.datetime.now() - datetime.timedelta(hours=offset)
        offset = "Минус %s" % (offset)
    html = "<html><body> %s часов будет %s.</body></html>" % (offset, dt)
    return HttpResponse(html)
