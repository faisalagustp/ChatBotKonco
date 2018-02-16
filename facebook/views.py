# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import urllib

import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from management.models import user_account
'''
    Halo. Perkenalkan nama saya Konco. Apa benar saat ini Konco sedang chat dengan dengan <nama>?
    kalo ya:
        Hi <nama>. Terimakasih telah menggunakan layanan kami. Kamu boleh tanya aku tentang apapun yang kamu mau.
    kalo tidak:
        Oh, kalau begitu nama kamu siapa?
        Hi <nama>. Terimakasih telah menggunakan layanan kami. Kamu boleh tanya aku tentang apapun yang kamu mau.
'''

@csrf_exempt
def facebook_callback(request):
    PAGE_TOKEN = "EAANWDfOtda8BAPsjZAgMmUcVvjZBKoOq3kxZBbNHMIRNHxGo0ZAZArae0FZBKkxuRCNcszoF3ZB3XkZBfvgcIjzUmWleiZBc5b3gmMBGFNvh3tpYOrkfGf0k8ItuMKbbqP6KxFkMZCe2Jx9BK1QgL8oRD4Xgp0wkhqnGm1BeNA3j5hlAZDZD"
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
                    if("message" in messaging):
                        text = messaging["message"]["text"]
                        chat_id = messaging["sender"]["id"]
                        u_ac = user_account.objects.filter(type="facebook").filter(chat_id=chat_id)
                        if u_ac.count()>0:
                            u_ac = u_ac[0]
                            analyze_reply(text,u_ac)
                            send_response(u_ac.short_memory,text)
                        else:
                            facebook_name = 'https://graph.facebook.com/'+chat_id+'?fields=name,id&access_token='+PAGE_TOKEN
                            facebook_name = requests.get(facebook_name).json()
                            name = facebook_name["name"]
                            u_ac = user_account()
                            u_ac.chat_id = chat_id
                            u_ac.type = "facebook"
                            u_ac.short_memory = "registration|ask_name"
                            send_response("Halo. Perkenalkan nama saya Konco. Apa benar saat ini Konco sedang chat dengan dengan "+name+"?",chat_id,"Ya|Tidak")
                            u_ac.save()
                    return HttpResponse("")
        else:
            return HttpResponse("Not recognized")
        return HttpResponse("Failed")

def send_response(message, sender_id,options):
    PAGE_TOKEN = "EAANWDfOtda8BAPsjZAgMmUcVvjZBKoOq3kxZBbNHMIRNHxGo0ZAZArae0FZBKkxuRCNcszoF3ZB3XkZBfvgcIjzUmWleiZBc5b3gmMBGFNvh3tpYOrkfGf0k8ItuMKbbqP6KxFkMZCe2Jx9BK1QgL8oRD4Xgp0wkhqnGm1BeNA3j5hlAZDZD"

    try:
        params = {
            "access_token": PAGE_TOKEN
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "recipient": {
                "id": sender_id
            },
            "message": {
                "text": message
            }
        }

        if options!= "":
            data_options = []
            for option in options.split("|"):
                data_options.append({
                    "content_type":"text",
                    "title":option
                })
            data["message"]["quick_replies"] = data_options

        data = json.dumps(data)
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            pass
    except Exception as e:
        print ("Error")

def analyze_reply(text,u_ac):
    print(text)
    print(u_ac)