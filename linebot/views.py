from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def line_callback(request):
    return HttpResponse("clash Clawk")
