"""ChatBot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from facebook.views import facebook_callback
from linebot.views import line_callback
import management.views as management_callback


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^facebook/callback', facebook_callback),
    url(r'^line/callback', line_callback),
    url(r'^$', management_callback.landing_page),
    url(r'^privacy-policy$', management_callback.privacy_policy),
    url(r'^post$', management_callback.list_scheduled_post),
    url(r'^post/add$', management_callback.add_scheduled_post),
    url(r'^post/(\d+)$', management_callback.detail_scheduled_post),
    url(r'^post/(\d+)/edit$', management_callback.edit_scheduled_post),
    url(r'^survey$', management_callback.list_survey),
    url(r'^survey/add$', management_callback.add_survey),
    url(r'^survey/(\d+)$', management_callback.detail_survey),
    url(r'^survey/(\d+)/edit$', management_callback.edit_survey),
]
