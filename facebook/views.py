# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import urllib
from django.utils import timezone

import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

PAGE_TOKEN = "EAANWDfOtda8BAPsjZAgMmUcVvjZBKoOq3kxZBbNHMIRNHxGo0ZAZArae0FZBKkxuRCNcszoF3ZB3XkZBfvgcIjzUmWleiZBc5b3gmMBGFNvh3tpYOrkfGf0k8ItuMKbbqP6KxFkMZCe2Jx9BK1QgL8oRD4Xgp0wkhqnGm1BeNA3j5hlAZDZD"
from management.models import user_account, survey_submission, survey_submission_value

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
    if request.method == "GET":
        VERIFY_TOKEN = "faisalkasepfaisalkasep"
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        if mode != None and token != None:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                return HttpResponse(challenge)
            else:
                return HttpResponse("Failed")
        return HttpResponse("Callback")
    elif request.method == "POST":
        data_request = json.loads(request.body.decode('utf-8'))
        if data_request["object"] == "page":
            for entry in data_request["entry"]:
                for messaging in entry["messaging"]:
                    if ("message" in messaging):
                        text = messaging["message"]["text"]
                        chat_id = messaging["sender"]["id"]
                        u_ac = user_account.objects.filter(type="facebook").filter(chat_id=chat_id)
                        if u_ac.count() > 0:
                            u_ac = u_ac[0]
                            analyze_reply(text, u_ac)
                        else:
                            facebook_name = 'https://graph.facebook.com/' + chat_id + '?fields=name,id&access_token=' + PAGE_TOKEN
                            facebook_name = requests.get(facebook_name).json()
                            name = facebook_name["name"]
                            u_ac = user_account()
                            u_ac.chat_id = chat_id
                            u_ac.type = "facebook"
                            u_ac.short_memory = "registration|ask_name"
                            options = {
                                "text": "Halo. Perkenalkan nama saya Konco. Apa benar saat ini Konco sedang chat dengan dengan " + name + "?",
                                "quick_replies": ["Ya","Tidak"],
                            }
                            send_response(chat_id, "text", options)
                            u_ac.save()
                    return HttpResponse("")
        else:
            return HttpResponse("Not recognized")
        return HttpResponse("Failed")


def response_test(request):
    type = "generic"
    options = ""
    if type == "text":
        options = {
            "text":"I will never ever ever be the same",
            "quick_replies":["Yes","No"],
        }
    elif type == "attachment":
        options = {
                    "url" : "http://www.gunadarma.ac.id/library/articles/graduate/psychology/2008/Artikel_10503160.pdf",
                    "tipe": "file",
                    "quick_replies" : []
                  }
    elif type == "generic":
        options = {
            "media_url" : "https://www.solveemployment.org/static/images/web_ahmad.jpg",
            "media_url_type": "image",
            "title": "SolveEmployment, gini weh aku mah",
            "subtitle": "SolveEmployment, gini weh aku mah",
            "url": "https://solveemployment.org",
            "buttons": [
                {
                    "tipe_button": "text",
                    "konten": "Aku suka kamu",
                },
                {
                    "tipe_button": "call",
                    "konten": "+6285624155417",
                },
                {
                    "tipe_button": "share",
                    "konten": "Share this",
                },
            ]
        }
    elif type == "location":
        options = {
            "lat": 0,
            "long": 0,
            "location_name": "Null Island",
        }
    elif type == "carousel":
        options = [{
            "media_url" : "https://www.solveemployment.org/static/images/web_ahmad.jpg",
            "media_url_type": "image",
            "title": "SolveEmployment, gini weh aku mah",
            "subtitle": "SolveEmployment, gini weh aku mah",
            "url": "https://solveemployment.org",
            "buttons": [
                {
                    "tipe_button" : "url",
                    "konten": "https://solveeducation.org",
                },
                {
                    "tipe_button": "text",
                    "konten": "Aku suka kamu",
                },
            ]
        },{
            "media_url" : "https://www.solveemployment.org/static/images/web_ahmad.jpg",
            "media_url_type": "image",
            "title": "SolveEmployment, gini weh aku mah",
            "subtitle": "SolveEmployment, gini weh aku mah",
            "url": "https://solveemployment.org",
            "buttons": [
                {
                    "tipe_button" : "url",
                    "konten": "https://solveeducation.org",
                },
                {
                    "tipe_button": "text",
                    "konten": "Aku suka kamu",
                },
            ]
        },{
            "media_url" : "https://www.solveemployment.org/static/images/web_ahmad.jpg",
            "media_url_type": "image",
            "title": "SolveEmployment, gini weh aku mah",
            "subtitle": "SolveEmployment, gini weh aku mah",
            "url": "https://solveemployment.org",
            "buttons": [
                {
                    "tipe_button" : "url",
                    "konten": "https://solveeducation.org",
                },
                {
                    "tipe_button": "text",
                    "konten": "Aku suka kamu",
                },
            ]
        }]
    elif type=="listview":
        options = [{
            "media_url": "https://www.solveemployment.org/static/images/web_ahmad.jpg",
            "media_url_type": "image",
            "title": "SolveEmployment, gini weh aku mah",
            "subtitle": "SolveEmployment, gini weh aku mah",
            "url": "https://solveemployment.org",
            "buttons": [
                {
                    "tipe_button": "url",
                    "konten": "https://solveeducation.org",
                },
                {
                    "tipe_button": "text",
                    "konten": "Aku suka kamu",
                },
            ]
        }, {
            "media_url": "https://www.solveemployment.org/static/images/web_ahmad.jpg",
            "media_url_type": "image",
            "title": "SolveEmployment, gini weh aku mah",
            "subtitle": "SolveEmployment, gini weh aku mah",
            "url": "https://solveemployment.org",
            "buttons": [
                {
                    "tipe_button": "url",
                    "konten": "https://solveeducation.org",
                },
                {
                    "tipe_button": "text",
                    "konten": "Aku suka kamu",
                },
            ]
        }, {
            "media_url": "https://www.solveemployment.org/static/images/web_ahmad.jpg",
            "media_url_type": "image",
            "title": "SolveEmployment, gini weh aku mah",
            "subtitle": "SolveEmployment, gini weh aku mah",
            "url": "https://solveemployment.org",
            "buttons": [
                {
                    "tipe_button": "url",
                    "konten": "https://solveeducation.org",
                },
                {
                    "tipe_button": "text",
                    "konten": "Aku suka kamu",
                },
            ]
        }]

    send_response(1937861672968054, type, options)
    return HttpResponse("Wkwkw")

def make_quick_replies(quick_replies):
    qr = []
    for opsi in quick_replies:
        qr.append(
            {
                "content_type": "text",
                "title": opsi,
                "payload": opsi,
            }
        )
    return qr

def send_response(sender_id, type, options):
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
            "message": {}
        }

        if type == "attachment":
            data["message"]["attachment"] = {
                "type": options["tipe"],
                "payload": {
                    "url": options["url"],
                    "is_reusable": True
                },

            }
            qr = make_quick_replies(options["quick_replies"])
            if len(qr) != 0:
                data["message"]["quick_replies"] = qr
        elif type == "text":
            data["message"]["text"] = options["text"]
            qr = make_quick_replies(options["quick_replies"])
            if len(qr)!=0:
                data["message"]["quick_replies"] = qr
        elif type == "generic":
            data["message"]["attachment"] = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Welcome!",
                            "image_url": "https://www.solveemployment.org/static/images/web_ahmad.jpg",
                            "subtitle": "We have the right hat for everyone.",
                            "default_action": {
                                "type": "web_url",
                                "url": "https://www.solveemployment.org/",
                            },
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "Start Chatting",
                                    "payload": "DEVELOPER_DEFINED_PAYLOAD"
                                }
                            ]
                        }
                    ]
                }
            }
            data["message"]["attachment"]["payload"]["elements"][0]["title"] = options["title"]
            data["message"]["attachment"]["payload"]["elements"][0]["image_url"] = options["media_url"]
            data["message"]["attachment"]["payload"]["elements"][0]["subtitle"] = options["subtitle"]
            data["message"]["attachment"]["payload"]["elements"][0]["default_action"]["url"] = options["url"]
            data["message"]["attachment"]["payload"]["elements"][0]["buttons"] = []
            for buttons in options["buttons"]:
                if buttons["tipe_button"]=="text":
                    data["message"]["attachment"]["payload"]["elements"][0]["buttons"].append(
                        {
                            "type": "postback",
                            "title": buttons["konten"],
                            "payload": "PAYLOAD_APAAN"
                        }
                    )
                elif buttons["tipe_button"]=="call":
                    data["message"]["attachment"]["payload"]["elements"][0]["buttons"].append(
                        {
                            "type": "phone_number",
                            "title": "call",
                            "payload": buttons["konten"],
                        }
                    )
                elif buttons["tipe_button"]=="share":
                    data["message"]["attachment"]["payload"]["elements"][0]["buttons"].append(
                        {
                            "type": "element_share",
                        }
                    )
                else:
                    data["message"]["attachment"]["payload"]["elements"][0]["buttons"].append(
                        {
                            "type": "web_url",
                            "title": buttons["konten"],
                            "url": buttons["konten"]
                        }
                    )
        elif type == "location":
            data["message"]["attachment"] = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": options["location_name"],
                            "image_url": "https://maps.googleapis.com/maps/api/staticmap?size=764x400&center=" + str(options["lat"]) + "," + str(options["long"]) + "&zoom=25&markers=" + str(options["lat"]) + "," + str(options["long"]),
                            "item_url": "http://www.google.com/maps/search/?api=1&query=" + str(options["lat"]) + "," + str(options["long"]) + "&z=16"
                        }
                    ]
                }
            }
        elif type == "quick_replies":
            data["message"]["text"] = options["text"]
            data["message"]["quick_replies"] = []
            for opsi in options["options"]:
                data["message"]["quick_replies"].append(
                    {
                        "content_type": "text",
                        "title": opsi,
                        "payload": opsi,
                    }
                )
        elif type == "carousel":
            data["message"]["attachment"] = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [

                    ]
                }
            }

            for option in options:
                template = {
                    "title": "Welcome!",
                    "image_url": "https://www.solveemployment.org/static/images/web_ahmad.jpg",
                    "subtitle": "We have the right hat for everyone.",
                    "default_action": {
                        "type": "web_url",
                        "url": "https://www.solveemployment.org/",
                    },
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "Start Chatting",
                            "payload": "DEVELOPER_DEFINED_PAYLOAD"
                        }
                    ]
                }
                template["title"] = option["title"]
                template["image_url"] = option["media_url"]
                template["subtitle"] = option["subtitle"]
                template["default_action"]["url"] = option["url"]
                template["buttons"] = []
                for button in option["buttons"]:
                    if button["tipe_button"] == "text":
                        template["buttons"].append(
                            {
                                "type": "postback",
                                "title": button["konten"],
                                "payload": "PAYLOAD_APAAN"
                            }
                        )
                    elif button["tipe_button"] == "call":
                        template["buttons"].append(
                            {
                                "type": "phone_number",
                                "title": "call",
                                "payload": button["konten"],
                            }
                        )
                    elif button["tipe_button"] == "share":
                        template["buttons"].append(
                            {
                                "type": "element_share",
                            }
                        )
                    else:
                        template["buttons"].append(
                            {
                                "type": "web_url",
                                "title": button["konten"],
                                "url": button["konten"]
                            }
                        )
                data["message"]["attachment"]["payload"]["elements"].append(template)


        print(data)
        data = json.dumps(data)
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            print(r.content)
    except Exception as e:
        print(e)


def analyze_reply(text, u_ac):
    if u_ac.short_memory == "registration|ask_name":
        if "ya" in str(text).lower():
            u_ac.short_memory = ""
            facebook_name = 'https://graph.facebook.com/' + u_ac.chat_id + '?fields=name,id&access_token=' + PAGE_TOKEN
            facebook_name = requests.get(facebook_name).json()
            name = facebook_name["name"]
            u_ac.name = name
            u_ac.save()

            options = {
                "text": "Hi " + name + ". Terimakasih telah menggunakan layanan kami. Pada masa percobaan ini, kami hanya bisa menangani broadcast post dan survey.",
                "quick_replies": ["Ya", "Tidak"],
            }
            send_response(u_ac.chat_id, "text", options)
        elif str(text).lower() == "tidak":
            u_ac.short_memory = "registration|ask_name|no"
            options = {
                "text": "Oh, kalau begitu nama kamu siapa?",
                "quick_replies": [],
            }
            send_response(u_ac.chat_id, "text", options)
            u_ac.save()
        else:
            facebook_name = 'https://graph.facebook.com/' + u_ac.chat_id + '?fields=name,id&access_token=' + PAGE_TOKEN
            facebook_name = requests.get(facebook_name).json()
            name = facebook_name["name"]
            options = {
                "text": "Saat ini fitur pengenalan bahasa indonesia belum diaktifkan di chat bot ini. Apa benar saat ini saya sedang chat dengan " + name + "?",
                "quick_replies": ["Ya","Tidak"],
            }
            send_response(u_ac.chat_id, "text", options)
    elif u_ac.short_memory == "registration|ask_name|no":
        text = str(text).replace("nama saya", "").strip()
        u_ac.name = text
        u_ac.short_memory = ""
        u_ac.save()
        options = {
            "text": "Hi " + text + ". Terimakasih telah menggunakan layanan kami. Pada masa percobaan ini, kami hanya bisa menangani broadcast post dan survey.",
            "quick_replies": [],
        }
        send_response(u_ac.chat_id, "text", options)
    elif str(u_ac.short_memory).startswith("survey"):
        question_number = u_ac.short_memory.replace("survey", "")
        surveynya = survey_submission.objects.filter(user_account_id=u_ac.id).filter(status="on progress")
        if surveynya.count() > 0:
            surveynya = surveynya[0]
            if question_number == "":
                if "ya" in text:
                    list_question = surveynya.survey.survey_value_set.all()
                    if list_question.count() > 0:
                        u_ac.short_memory = "survey|1"
                        list_question = list_question[0]
                        options = {
                            "text": list_question.text,
                            "quick_replies": list_question.options.split(","),
                        }
                        send_response(surveynya.user_account.chat_id, "text", options)
                    else:
                        u_ac.short_memory = ""
                        options = {
                            "text": "Survey dibatalkan",
                            "quick_replies": [],
                        }
                        send_response(surveynya.user_account.chat_id, "text", options)
                        surveynya.status = "done"
                        surveynya.save()
                    u_ac.save()
                else:
                    u_ac.short_memory = ""
                    options = {
                        "text": "Survey dibatalkan",
                        "quick_replies": [],
                    }
                    send_response(surveynya.user_account.chat_id, "text", options)
                    surveynya.status = "done"
                    surveynya.save()
                    u_ac.save()
            else:
                question_number = question_number.replace("|", "")
                question_number = int(question_number)
                list_question = surveynya.survey.survey_value_set.all()
                if list_question.count() > question_number:
                    question = list_question[question_number - 1]
                    val = survey_submission_value()
                    val.survey_submission = surveynya
                    val.survey_value = question
                    val.value = text
                    val.datetime = timezone.now()
                    val.save()
                    try:
                        list_question = list_question[question_number]
                        u_ac.short_memory = "survey|" + str(question_number + 1)
                        options = {
                            "text": list_question.text,
                            "quick_replies": [],
                        }
                        send_response(surveynya.user_account.chat_id, "text", options)
                        u_ac.save()
                    except Exception:
                        u_ac.short_memory = ""
                        options = {
                            "text": "Terima kasih. Respon anda telah tersimpan.",
                            "quick_replies": [],
                        }
                        send_response(surveynya.user_account.chat_id, "text", options)
                        surveynya.status = "done"
                        surveynya.save()
                else:
                    question = list_question[question_number - 1]
                    val = survey_submission_value()
                    val.survey_submission = surveynya
                    val.survey_value = question
                    val.value = text
                    val.datetime = timezone.now()
                    val.save()
                    u_ac.short_memory = ""
                    options = {
                        "text": "Terima kasih. Respon anda telah tersimpan.",
                        "quick_replies": [],
                    }
                    send_response(surveynya.user_account.chat_id, "text", options)
                    surveynya.status = "done"
                    surveynya.save()
                u_ac.save()
