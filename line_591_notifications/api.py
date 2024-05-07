from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from . import models
import uuid, json, requests, urllib, os
from urllib.parse import parse_qs
import line_591_notifications.CONST as CONST
import line_591_notifications.utils as utils
from dotenv import load_dotenv
load_dotenv()

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
        else:
            # TODO: implementation: user information update
            pass
        
        token = utils.get_token(
            client_id=os.environ["client_id"],
            client_secret=os.environ["client_secret"],
            code=code, 
            redirect_uri=CONST.BASE_URL + "/auth/"
        )

        # TODO: implementation: 服務上限
        models.Notification(
            user=models.User.objects.get(id=user_id), token=token
        ).save()

        return HttpResponse(f"Authentication successful!", status=200)

    except ValidationError as e:
        return HttpResponse(f"Validation error: {str(e)}", status=400)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

