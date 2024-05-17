from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from . import models
import uuid, json, requests, urllib, os
from urllib.parse import parse_qs
import line_591_notifications.CONST as CONST
import line_591_notifications.utils as utils
import line_591_notifications.models as models
from dotenv import load_dotenv
load_dotenv()

@csrf_exempt
def login(request: HttpRequest):
    """
    Handles the login process for the application.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response indicating the result of the login process.
    """

    try:
        # Check if the 'code' parameter is present in the GET request
        code = request.GET.get("code")
        if not code:
            return HttpResponse("Missing 'code' in request", status=400)

        # Obtain token
        data = utils.get_token(
            client_id=os.environ.get("login_id"), 
            client_secret=os.environ.get("login_secret"),
            code=code, 
            token_url=CONST.LOGIN_TOKEN_URL,
            redirect_uri=CONST.BASE_URL + "/isLogin/"
        )
        id_token = data.get("id_token")

        # Save user to database
        if not id_token:
            return HttpResponse("Failed to retrieve ID token", status=500)
        else:
            if not models.User.objects.filter(id=id_token).exists():
                user = models.User(id=id_token).save()
        return JsonResponse({"user_id": id_token}, status=200)
    
    except ValidationError as e:
        return HttpResponse(f"Validation error: {str(e)}", status=400)
    except KeyError as e:
        return HttpResponse(f"Missing key in response: {str(e)}", status=500)
    except Exception as e:
        return HttpResponse(f"An unexpected error occurred: {str(e)}", status=500)


@csrf_exempt
def auth(request: HttpRequest):
    """
    Authenticates the user and subscribes them to notifications.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response indicating the result of the authentication.

    Raises:
        ValidationError: If there is a validation error.
        Exception: If an unexpected error occurs.
    """
    try:
        user_id = uuid.uuid4()
        # user_id = data.get("user_id") # TODO: implementation: get user_id from request body
        code = request.GET["code"]

        if not user_id or not code:
            return HttpResponse("Missing user_id or code in request body", status=400)
        
        if not models.User.objects.filter(id=user_id).exists():
            user = models.User(id=user_id).save()
        
        data = utils.get_token(
            client_id=os.environ["client_id"],
            client_secret=os.environ["client_secret"],
            code=code, 
            token_url=CONST.NOTIFY_TOKEN_URL,
            redirect_uri=CONST.BASE_URL + "/isAuth/"
        )
        return JsonResponse({"notify_id": data["access_token"]}, status=200)
    except ValidationError as e:
        return HttpResponse(f"Validation error: {str(e)}", status=400)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

@csrf_exempt
def notify(request: HttpRequest):
    """
    Sends notifications to users based on the available notifications in the database.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response indicating the status of the notification sending process.
            If successful, returns a response with status code 200 and a message "Notification sent!".
            If an error occurs, returns a response with status code 500 and an error message.
    """
    try:
        notifications = models.Notification.objects.all()
        for notification in notifications:
            if not notification.token:
                continue
            res = utils.notify(notification.token)
            if res.status_code == 401:
                notification.delete()
            elif res.status_code == 200:
                print(f"Notification sent to {notification.user.id}")
        return HttpResponse(f"Notification sent!", status=200)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

