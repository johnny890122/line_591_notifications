import os
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from urllib.parse import parse_qs
import line_591_notifications.CONST as CONST
import line_591_notifications.utils as utils
import line_591_notifications.models as models
from dotenv import load_dotenv
load_dotenv()

def homepage(request: HttpRequest):
    context = {
        "auth_url": CONST.AUTHORIZE_URL,
        "response_type": "code",
        "client_id": os.environ.get("client_id"),
        "redirect_uri": CONST.BASE_URL + "/auth/",
        "scope": "notify",
        "state": utils.generate_csrf_token(),
        "form": models.RentConditionForm(),
    }
    if request.method == 'POST':
        form = models.RentConditionForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data["url"])     
            form.save()

    return render(request, 'homepage.html', context)