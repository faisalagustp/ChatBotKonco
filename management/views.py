from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from management.models import scheduled_post, survey as Survey, user_account as UserAccount, scheduled_post_report, survey_value as SurveyValue, survey_submission


def landing_page(request):
    return render(request,"landing_page/index.html")

def list_scheduled_post(request):
    if request.GET.get("id")!=None:
        if request.GET.get("action")=="delete":
            sp = scheduled_post.objects.get(id=request.GET.get("id"))
            sp.delete()
            return redirect("/post")
    posts = scheduled_post.objects.all()
    return render(request, "scheduled_post/index.html",{
        "posts" : posts,
    })


def add_scheduled_post(request):
    users = UserAccount.objects.all()
    if request.method=="POST":
        with transaction.atomic():
            sch_post = scheduled_post()
            sch_post.datetime = request.POST.get("datetime")
            sch_post.post_text = request.POST.get("post_text")
            sch_post.message_type = request.POST.get("message_type")
            sch_post.json_extra = request.POST.get("json_extra")
            sch_post.save()

            list_of_id = []
            if request.POST.get("send_to")=="users":
                list_of_id = request.POST.getlist("target_users")
            else:
                users = UserAccount.objects.all()
                for user in users:
                    list_of_id.append(user.id)

            for id_target_user in list_of_id:
                user_account = UserAccount.objects.filter(id=id_target_user)
                if user_account.count()>0:
                    user_account = user_account[0]
                    spr = scheduled_post_report()
                    spr.user_account = user_account
                    spr.status = "planned"
                    spr.scheduled_post = sch_post
                    spr.save()

        return redirect("/post/"+str(sch_post.id))
    else:
        return render(request, "scheduled_post/form.html",{
            "users" : users
        })

def edit_scheduled_post(request,id):
    post = get_object_or_404(scheduled_post,id=id)
    return render(request, "scheduled_post/form.html",{
        "post": post
    })

def detail_scheduled_post(request,id):
    post = get_object_or_404(scheduled_post, id=id)
    return render(request, "scheduled_post/detail.html",{
        "post": post
    })

def list_survey(request):
    if request.GET.get("id")!=None:
        if request.GET.get("action")=="delete":
            sp = Survey.objects.get(id=request.GET.get("id"))
            sp.delete()
            return redirect("/survey")
    surveys = Survey.objects.all()
    return render(request, "survey/index.html",{
        "surveys" : surveys
    })

def add_survey(request):
    users = UserAccount.objects.all()
    if request.method=="POST":
        with transaction.atomic():
            srvy = Survey()
            srvy.survey_name = request.POST.get("survey_name")
            srvy.datetime = request.POST.get("datetime")
            srvy.description = request.POST.get("description")
            srvy.for_type = request.POST.get("for_type")
            srvy.save()

            # options
            # question1$option1|option2|option3|option4...,
            options = request.POST.get("options")
            options = str(options).split(",")
            for option in options:
                option = option.split("$")
                sv = SurveyValue()
                sv.survey = srvy
                sv.text = str(option[0]).strip()
                sv.type = "question"
                sv.options = str(option[1]).strip()
                sv.save()

            ##target user
            list_of_id = []
            if request.POST.get("send_to") == "users":
                list_of_id = request.POST.getlist("target_users")
            else:
                users = UserAccount.objects.all()
                for user in users:
                    list_of_id.append(user.id)

            for id_target_user in list_of_id:
                user_account = UserAccount.objects.filter(id=id_target_user)
                if user_account.count() > 0:
                    user_account = user_account[0]
                    sv = survey_submission()
                    sv.user_account = user_account
                    sv.survey = srvy
                    sv.status = ""
                    sv.save()
        return redirect("/survey/"+str(srvy.id))
    else:
        return render(request, "survey/form.html",{
            "users": users
        })

def edit_survey(request,id):
    survey_data = get_object_or_404(Survey, id=id)
    return render(request, "survey/form.html", {
        "survey": survey_data
    })

def detail_survey(request,id):
    survey_data = get_object_or_404(Survey, id=id)
    return render(request, "survey/detail.html",{
        "survey": survey_data
    })