from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from . import models
import uuid, json
from urllib.parse import parse_qs

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
        data = parse_qs(request.body.decode())
        user_id = uuid.uuid4()
        # user_id = data.get("user_id") # TODO: implementation: get user_id from request body
        code_lst = data["code"]

        if not user_id or not code_lst:
            return HttpResponse("Missing user_id or code in request body", status=400)
        
        if not models.User.objects.filter(id=user_id).exists():
            user = models.User(id=user_id).save()
        else:
            # TODO: implementation: user information update
            pass
        
        for code in code_lst:
            if not models.Notification.objects.filter(user=user, code=code).exists():
                models.Notification(
                    user=models.User.objects.get(id=user_id), code=code
                ).save()
            else:
                pass
                # TODO: implementation: user already subscribed

        return HttpResponse("Authentication successful", status=200)

    except ValidationError as e:
        return HttpResponse(f"Validation error: {str(e)}", status=400)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

