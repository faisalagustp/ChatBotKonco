import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def line_callback(request):
    if request.method == "POST":
        data_request = json.loads(request.body.decode('utf-8'))
        print(data_request)
    return HttpResponse("clash Clawk")
