# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import urllib

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def facebook_callback(request):
    if request.method == "GET":
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
    elif request.method=="POST":
        data_request = json.loads(request.body.decode('utf-8'))
        if data_request["object"] == "page":
            for entry in data_request["entry"]:
                for messaging in entry["messaging"]:
                    send_response(messaging["message"]["text"],messaging["sender"]["id"])
                    return HttpResponse("")
        else:
            return HttpResponse("Not recognized")
        return HttpResponse("Failed")

def send_response(message, sender_id):
    PAGE_TOKEN = "EAANWDfOtda8BAPsjZAgMmUcVvjZBKoOq3kxZBbNHMIRNHxGo0ZAZArae0FZBKkxuRCNcszoF3ZB3XkZBfvgcIjzUmWleiZBc5b3gmMBGFNvh3tpYOrkfGf0k8ItuMKbbqP6KxFkMZCe2Jx9BK1QgL8oRD4Xgp0wkhqnGm1BeNA3j5hlAZDZD"

    request_body = {
        "recipient": {
            "id": sender_id
        },
        "message": message
    }
    request_body = urllib.parse.urlencode(request_body).encode('utf-8')
    try:
        req = urllib.request.Request("https://graph.facebook.com/v2.6/me/messages", data=request_body,
                                     headers={'content-type': 'application/json', "access_token":PAGE_TOKEN})
        response = urllib.request.urlopen(req)
    except Exception as e:
        print (e)


