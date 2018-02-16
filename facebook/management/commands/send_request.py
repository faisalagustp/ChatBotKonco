# -*- coding: utf-8 -*-
from datetime import datetime

from django.core.management import BaseCommand
from management import models
from facebook.views import send_response

class Command(BaseCommand):
    # Show this when the user types help

    def handle(self, *args, **options):
        #post message
        posts = models.scheduled_post_report.objects.filter(user_account__type="facebook").exclude(status="done")\
            .filter(scheduled_post__datetime__lte=datetime.now()).filter(user_account__short_memory="")
        for post in posts:
            print("Masuk Satu")
            text = str(post.scheduled_post.post_text).replace("[name]",post.user_account.name)
            send_response(text,post.user_account.chat_id,"")
            post.datetime_sended = datetime.now()
            post.status="done"
            post.save()

        #surveys
        surveys = models.survey_submission.objects.filter(user_account__type="facebook").exclude(status="done")\
            .filter(survey__datetime__lte=datetime.now()).filter(user_account__short_memory="").exclude(status="on progress")
        for survey in surveys:
            print("Masuk Dua")
            text = str(survey.survey.description).replace("[name]",survey.user_account.name)
            text = survey.survey.survey_name + "\n\n" + text + "\n\n Tekan ya untuk melanjutkan, tekan tidak untuk tidak melanjutkan"
            send_response(text, survey.user_account.chat_id, "ya|tidak")

            survey.status = "on progress"
            survey.save()

            uac = survey.user_account
            uac.short_memory = "survey"
            uac.save()

