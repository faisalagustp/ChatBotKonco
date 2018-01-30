import json
import urllib

import requests
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def line_callback(request):
    if request.method == "POST":
        data_request = json.loads(request.body.decode('utf-8'))
        send_message(data_request["events"][0]["replyToken"], data_request["events"][0]["message"]["text"])
        send_push_message(data_request["events"][0]["source"]["userId"])
    return HttpResponse("clash Clawk")


def send_message(reply_token, text):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer J2Lzw9hQNkaW8fY5MkJQyb+MdqihHXjGCE0iVDqi5cJGf6Ww+pSx5QTnL5I03SIeHuNYi2sz5a9QMm8BAiESS7Te2WwwbyiQ8EZ9dzym7mlBKcKL8nscfJnF4g7Pq8H077TBFM4rrPZV+1pXFSd0AQdB04t89/1O/w1cDnyilFU=",
        }
        data = json.dumps({
            "replyToken": reply_token,
            "messages": [
                {
                    "type": "text",
                    "text": text
                }
            ]
        })

        r = requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, data=data)
        if r.status_code != 200:
            print(r.status_code)
            print(r.text)
    except Exception as e:
        print(e)


def send_push_message(user_id):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer J2Lzw9hQNkaW8fY5MkJQyb+MdqihHXjGCE0iVDqi5cJGf6Ww+pSx5QTnL5I03SIeHuNYi2sz5a9QMm8BAiESS7Te2WwwbyiQ8EZ9dzym7mlBKcKL8nscfJnF4g7Pq8H077TBFM4rrPZV+1pXFSd0AQdB04t89/1O/w1cDnyilFU=",
        }
        data = json.dumps({
            "to": [user_id],
            "messages": [
                {
                    "type": "text",
                    "text": "Example of"
                },
                {
                    "type": "text",
                    "text": "push message"
                }
            ]
        })

        r = requests.post("https://api.line.me/v2/bot/message/multicast", headers=headers, data=data)
        if r.status_code != 200:
            print(r.status_code)
            print(r.text)
    except Exception as e:
        print(e)
