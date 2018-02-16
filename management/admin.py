from django.contrib import admin
from management import models

# Register your models here.
class ScheduledPost(admin.ModelAdmin):
    pass

class ScheduledPostReport(admin.ModelAdmin):
    pass

class UserAccount(admin.ModelAdmin):
    pass

class Survey(admin.ModelAdmin):
    pass

class SurveyValue(admin.ModelAdmin):
    pass

class SurveySubmission(admin.ModelAdmin):
    pass

class SurveySubmissionValue(admin.ModelAdmin):
    pass


admin.site.register(models.scheduled_post, ScheduledPost)
admin.site.register(models.scheduled_post_report, ScheduledPostReport)
admin.site.register(models.user_account, UserAccount)
admin.site.register(models.survey, Survey)
admin.site.register(models.survey_value, SurveyValue)
admin.site.register(models.survey_submission, SurveySubmission)
admin.site.register(models.survey_submission_value, SurveySubmissionValue)