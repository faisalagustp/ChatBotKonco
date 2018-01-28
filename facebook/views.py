# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def facebook_callback(request):
    return JsonResponse({
        "test" : "Test"
    })