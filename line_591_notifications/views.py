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
        "auth_redirect_url": CONST.BASE_URL + "/isAuth/",
        "client_id": os.environ.get("client_id"),
        "response_type": "code",
        "scope": "notify",
        "state": utils.generate_csrf_token(),
    }

    return render(request, 'homepage.html', context)

def login(request: HttpRequest):
    context = {
        "login_url": CONST.LOGIN_URL,
        "login_id": os.environ.get("login_id"),
        "scope": "openid", 
        "redirect_url": CONST.BASE_URL + "/isLogin/",
        "response_type": "code",
        "state": utils.generate_csrf_token(),
    }

    return render(request, 'login.html', context)

def isLogin(request: HttpRequest):
    try:
        res = api.login(request).content
        data = json.loads(res.decode("utf-8"))
        if data["user_id"]:
            context = {"user_id": data["user_id"]}
            return render(request, 'isLogin.html', context)
        else:
            return redirect("/")
    except Exception as e:
        return redirect("/")

def isLogout(request: HttpRequest):
    return render(request, 'isLogout.html')

def isAuth(request: HttpRequest):
    try:
        context = {
            "base_url": CONST.BASE_URL,
            "form": forms.NotifyForm(),
            "notify_code": request.GET["code"],
        }

        if request.method == 'POST':
            res = api.auth(request)
            if res.status_code == 200:
                return HttpResponse("Done", status=200)
            else:
                return HttpResponse("Expired", status=400)
                
    except Exception as e:
        return redirect("/")
    return render(request, 'isAuth.html', context)

def isDone(request: HttpRequest):
    return render(request, 'isDone.html')
