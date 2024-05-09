import os
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from dotenv import load_dotenv
import urllib.parse
import line_591_notifications.CONST as CONST
import line_591_notifications.utils as utils

def homepage(request: HttpRequest):
    load_dotenv()
    context = {
        "auth_url": CONST.AUTHORIZE_URL,
        "response_type": "code",
        "client_id": os.environ.get("client_id"),
        "redirect_uri": CONST.BASE_URL + "/auth/",
        "scope": "notify",
        "state": utils.generate_csrf_token()
    }

    return render(request, 'homepage.html', context)