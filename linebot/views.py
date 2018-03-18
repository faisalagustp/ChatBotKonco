import json
import urllib

import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from management.models import user_account, survey_submission, survey_submission_value


@csrf_exempt
def line_callback(request):
    user_id = ''
    if request.method == "POST":
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
                            name = "Fulan"
                            u_ac = user_account()
                            u_ac.chat_id = chat_id
                            u_ac.type = "line"
                            u_ac.short_memory = "registration|ask_name"
                            options = {
                                "text": "Halo. Perkenalkan nama saya Konco. Apa benar saat ini Konco sedang chat dengan dengan " + name + "?",
                                "quick_replies": ["Ya", "Tidak"],
                            }
                            send_push_message(chat_id, "text", options)
                            u_ac.save()
                    return HttpResponse("")
        else:
            return HttpResponse("Not recognized")
        return HttpResponse("Failed")

def test_message(request):
    user_id = "U7c5db7efd702acf9b463cf7fc5d74551"
    type = "imagemap"
    options = ""
    if type == "text":
        options = {
            "text": "I will never ever ever be the same",
            "quick_replies": [],
        }
    elif type == "attachment":
        options = {
            "url": "https://upload.wikimedia.org/wikipedia/en/0/0e/Adele_-_Rolling_in_the_Deep.ogg",
            "tipe": "audio",
            "durasi": 22,
            "quick_replies": []
        }
    elif type == "generic":
        options = {
            "media_url": "https://www.solveemployment.org/static/images/web_ahmad.jpg",
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
    elif type == "imagemap":
        options = {
            "media_url": "https://www.solveemployment.org/static/images/web_ahmad.jpg",
            "media_url_type": "image",
            "title": "SolveEmployment, gini weh aku mah",
            "subtitle": "SolveEmployment, gini weh aku mah",
            "buttons": [
                {
                    "tipe_button": "text",
                    "konten": "Aku suka kamu",
                    "x" :0,
                    "y" :0,
                    "width" :100,
                    "height" :100,
                },
                {
                    "tipe_button": "url",
                    "konten": "https://solveemployment.org",
                    "x": 100,
                    "y": 100,
                    "width": 100,
                    "height": 100,
                },
                {
                    "tipe_button": "share",
                    "konten": "Share this",
                },
            ]
        }
    send_push_message(user_id,type,options)
    return HttpResponse(user_id)


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

def send_push_message(user_id,type,options):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer J2Lzw9hQNkaW8fY5MkJQyb+MdqihHXjGCE0iVDqi5cJGf6Ww+pSx5QTnL5I03SIeHuNYi2sz5a9QMm8BAiESS7Te2WwwbyiQ8EZ9dzym7mlBKcKL8nscfJnF4g7Pq8H077TBFM4rrPZV+1pXFSd0AQdB04t89/1O/w1cDnyilFU=",
        }
        data = {
            "to": [user_id],
            "messages": [

            ]
        }

        if type=="text":
            data["messages"].append(
                {
                    "type": "text",
                    "text": options["text"],
                }
            )
        elif type=="attachment":
            if options["tipe"]=="image":
                data["messages"].append(
                    {
                        "type": "image",
                        "originalContentUrl": options["url"],
                        "previewImageUrl": options["url"]
                    }
                )
            elif options["tipe"]=="video":
                data["messages"].append(
                    {
                        "type": "video",
                        "originalContentUrl": options["url"],
                        "previewVideoUrl": options["url"]
                    }
                )
            elif options["tipe"]=="file":
                data["messages"].append(
                    {
                        "type": "text",
                        "text": options["url"],
                    }
                )
            elif options["tipe"]=="audio":
                data["messages"].append(
                    {
                        "type": "audio",
                        "originalContentUrl": options["url"],
                        "duration": options["durasi"]*1000,
                    }
                )
        elif type=="generic":
            template = {
                    "type": "template",
                    "altText": options["title"],
                    "template": {
                        "type": "buttons",
                        "thumbnailImageUrl": options["media_url"],
                        "imageAspectRatio": "rectangle",
                        "imageSize": "cover",
                        "imageBackgroundColor": "#FFFFFF",
                        "title": options["title"],
                        "text": options["subtitle"],
                        "defaultAction": {
                            "type": "uri",
                            "label": "Visit Website",
                            "uri": options["url"]
                        },
                        "actions": []
                    }
                }

            for button in options["buttons"]:
                if button["tipe_button"]=="text":
                    template["template"]["actions"].append(
                        {
                            "type": "message",
                            "label": button["konten"],
                            "text": button["konten"]
                        }
                    )
                elif button["tipe_button"]=="url":
                    template["template"]["actions"].append(
                        {
                            "type": "uri",
                            "label": "View URL",
                            "uri": button["konten"]
                        }
                    )
            data["messages"].append(template)
        elif type=="location":
            data["messages"].append(
                {
                    "type": "location",
                    "title": options["location_name"],
                    "address": options["location_name"],
                    "latitude": options["lat"],
                    "longitude": options["long"]
                }
            )
        elif type=="carousel":
            carousel_message = {
                  "type": "template",
                  "altText": options[0]["title"],
                  "template": {
                      "type": "carousel",
                      "columns": [],
                      "imageAspectRatio": "rectangle",
                      "imageSize": "cover"
                  }
                }


            for option in options:
                template = {
                    "thumbnailImageUrl": option["media_url"],
                    "imageBackgroundColor": "#000000",
                    "title": option["title"],
                    "text": option["subtitle"],
                    "defaultAction": {
                        "type": "uri",
                        "label": "View detail",
                        "uri": option["url"],
                    },
                    "actions": []
                }

                for button in option["buttons"]:
                    if button["tipe_button"] == "text":
                        template["actions"].append(
                            {
                                "type": "message",
                                "label": button["konten"],
                                "text": button["konten"]
                            }
                        )
                    elif button["tipe_button"] == "url":
                        template["actions"].append(
                            {
                                "type": "uri",
                                "label": "View URL",
                                "uri": button["konten"]
                            }
                        )
                carousel_message["template"]["columns"].append(template)
            data["messages"].append(carousel_message)
        elif type=="imagemap":
            template = {
                "type": "imagemap",
                "baseUrl": options["media_url"],
                "altText": options["title"],
                "baseSize": {
                    "height": 1600,
                    "width": 900
                },
                "actions": []
            }

            for button in options["buttons"]:
                if button["tipe_button"] == "text":
                    template["actions"].append(
                        {
                            "type": "message",
                            "label": button["konten"],
                            "text": button["konten"],
                            "area" : {
                                "x": button["x"],
                                "y": button["y"],
                                "width": button["width"],
                                "height": button["height"],
                            }
                        }
                    )
                elif button["tipe_button"] == "url":
                    template["actions"].append(
                        {
                            "type": "uri",
                            "label": "View URL",
                            "linkUri": button["konten"],
                            "area" : {
                                "x": button["x"],
                                "y": button["y"],
                                "width": button["width"],
                                "height": button["height"],
                            }
                        }
                    )
            data["messages"].append(template)




        data = json.dumps(data)

        r = requests.post("https://api.line.me/v2/bot/message/multicast", headers=headers, data=data)
        if r.status_code != 200:
            print(r.status_code)
            print(r.text)
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
            send_push_message(u_ac.chat_id, "text", options)
        elif str(text).lower() == "tidak":
            u_ac.short_memory = "registration|ask_name|no"
            options = {
                "text": "Oh, kalau begitu nama kamu siapa?",
                "quick_replies": [],
            }
            send_push_message(u_ac.chat_id, "text", options)
            u_ac.save()
        else:
            facebook_name = 'https://graph.facebook.com/' + u_ac.chat_id + '?fields=name,id&access_token=' + PAGE_TOKEN
            facebook_name = requests.get(facebook_name).json()
            name = facebook_name["name"]
            options = {
                "text": "Saat ini fitur pengenalan bahasa indonesia belum diaktifkan di chat bot ini. Apa benar saat ini saya sedang chat dengan " + name + "?",
                "quick_replies": ["Ya","Tidak"],
            }
            send_push_message(u_ac.chat_id, "text", options)
    elif u_ac.short_memory == "registration|ask_name|no":
        text = str(text).replace("nama saya", "").strip()
        u_ac.name = text
        u_ac.short_memory = ""
        u_ac.save()
        options = {
            "text": "Hi " + text + ". Terimakasih telah menggunakan layanan kami. Pada masa percobaan ini, kami hanya bisa menangani broadcast post dan survey.",
            "quick_replies": [],
        }
        send_push_message(u_ac.chat_id, "text", options)
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
                        send_push_message(surveynya.user_account.chat_id, "text", options)
                    else:
                        u_ac.short_memory = ""
                        options = {
                            "text": "Survey dibatalkan",
                            "quick_replies": [],
                        }
                        send_push_message(surveynya.user_account.chat_id, "text", options)
                        surveynya.status = "done"
                        surveynya.save()
                    u_ac.save()
                else:
                    u_ac.short_memory = ""
                    options = {
                        "text": "Survey dibatalkan",
                        "quick_replies": [],
                    }
                    send_push_message(surveynya.user_account.chat_id, "text", options)
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
                        send_push_message(surveynya.user_account.chat_id, "text", options)
                        u_ac.save()
                    except Exception:
                        u_ac.short_memory = ""
                        options = {
                            "text": "Terima kasih. Respon anda telah tersimpan.",
                            "quick_replies": [],
                        }
                        send_push_message(surveynya.user_account.chat_id, "text", options)
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
                    send_push_message(surveynya.user_account.chat_id, "text", options)
                    surveynya.status = "done"
                    surveynya.save()
                u_ac.save()
