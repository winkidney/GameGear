# coding:utf-8
# Views.py of GameArt

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.utils.translation import ugettext as _


def home(request):
    return render_to_response('GameArt/base.html',
                              locals(),
                              context_instance=RequestContext(request))
def test(request):
    return HttpResponse(_(u'fuck'))