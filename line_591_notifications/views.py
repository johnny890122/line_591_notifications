import os, json
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from urllib.parse import parse_qs
import line_591_notifications.CONST as CONST
import line_591_notifications.utils as utils
import line_591_notifications.forms as forms
import line_591_notifications.models as models
import line_591_notifications.api as api

from dotenv import load_dotenv
load_dotenv()

def homepage(request: HttpRequest):
    context = {
        "auth_url": CONST.AUTHORIZE_URL,
        "response_type": "code",
        "client_id": os.environ.get("client_id"),
        "base_url": CONST.BASE_URL, 
        "scope": "notify",
        "state": utils.generate_csrf_token(),
        "form": forms.RentConditionForm(),
        "login_url": CONST.LOGIN_URL,
        "login_id": os.environ.get("login_id"),
        "scope": "openid", 
    }
    # if request.method == 'POST':
    #     data = dict(request.POST)
    #     models.RentCondition(
    #         url=data["url"]
    #     ).save()

    return render(request, 'homepage.html', context)

def login(request: HttpRequest):
    res = api.login(request).content
    data = json.loads(res.decode("utf-8"))

    context = {
        "base_url": CONST.BASE_URL,
        "user_id": data["user_id"]
    }

    return render(request, 'loginInfo.html', context)