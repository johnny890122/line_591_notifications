import os
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from dotenv import load_dotenv
import urllib.parse
import line_591_notifications.CONST as CONST
import line_591_notifications.utils as utils

def homepage(request: HttpRequest):
    load_dotenv()
    arguments = {
        "response_type": "code",
        "client_id": os.environ.get("CLIENT_ID"),
        "redirect_uri": CONST.BASE_URL + "/auth/",
        "scope": "notify",
        "state": utils.generate_csrf_token()
    }

    context = {
        'url': CONST.AUTHORIZE_URL + '?' + urllib.parse.urlencode(arguments)
    }
    return render(request, 'homepage.html', context)