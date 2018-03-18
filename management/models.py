from django.db import models

# Create your models here.
class scheduled_post(models.Model):
    post_text = models.TextField(null=True,blank=True)
    datetime = models.DateTimeField()
    message_type = models.CharField(max_length=20)
    json_extra = models.TextField(null=True,blank=True)

class scheduled_post_report(models.Model):
    scheduled_post = models.ForeignKey(scheduled_post)
    user_account = models.ForeignKey("user_account")
    datetime_sended = models.DateTimeField(null=True,blank=True)
    status = models.CharField(max_length=20)

class user_account(models.Model):
    chat_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100,null=True,blank=True)
    type = models.CharField(max_length=20)
    short_memory = models.TextField(null=True,blank=True)

class survey(models.Model):
    survey_name = models.CharField(max_length=250)
    datetime = models.DateTimeField(null=True,blank=True)
    description = models.TextField()
    for_type = models.CharField(max_length=20)

class survey_value(models.Model):
    survey = models.ForeignKey(survey)
    text = models.TextField()
    type = models.CharField(max_length=20)
    options = models.TextField()

class survey_submission(models.Model):
    survey = models.ForeignKey(survey)
    user_account = models.ForeignKey(user_account)
    status = models.CharField(max_length=20)

class survey_submission_value(models.Model):
    survey_submission = models.ForeignKey(survey_submission)
    survey_value = models.ForeignKey(survey_value)
    value = models.TextField()
    datetime = models.DateTimeField()

