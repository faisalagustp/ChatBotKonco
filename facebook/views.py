# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
def facebook_callback(request):
    VERIFY_TOKEN = "faisalkasepfaisalkasep"
    mode = request.GET.get('hub.mode')
    token = request.GET.get('hub.verify_token')
    challenge = request.GET.get('hub.challenge')
    if mode!=None and token!=None:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return HttpResponse(challenge)
        else:
            return HttpResponse("Failed")
    return HttpResponse("Callback")