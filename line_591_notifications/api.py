from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
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

    # try:
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
    # id_token = data.get("id_token")

    # # Save user to database
    # if not id_token:
    #     return HttpResponse("Failed to retrieve ID token", status=500)
    # else:
    #     if not models.User.objects.filter(id=id_token).exists():
    #         user = models.User(id=id_token).save()
    # return JsonResponse({"user_id": id_token}, status=200)
    
    # except ValidationError as e:
    #     return HttpResponse(f"Validation error: {str(e)}", status=400)
    # except KeyError as e:
    #     return HttpResponse(f"Missing key in response: {str(e)}", status=500)
    # except Exception as e:
    #     return HttpResponse(f"An unexpected error occurred: {str(e)}", status=500)


@csrf_exempt
def auth(request: HttpRequest):
    """
    Authenticate the user and obtain an authorization code.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response indicating the result of the authentication process.
    """

    if request.method == "POST":
        try:
            data = {k: v[0] for k, v in dict(request.POST).items()}
        except (AttributeError, IndexError) as e:
            return HttpResponse("Invalid data format", status=400)
        
        user_id = data.get("user")
        code = data.get("code")
        rent_url = data.get("rent_url")

        if not user_id or not code or not rent_url:
            return HttpResponse("Missing arguments in request body", status=400)
        
        if not models.User.objects.filter(id=user_id).exists():
            user = models.User(id=user_id).save()
        else:
            user = models.User.objects.filter(id=user_id).first()

        try:
            res = utils.get_token(
                client_id=os.environ["client_id"],
                client_secret=os.environ["client_secret"],
                code=code, 
                token_url=CONST.NOTIFY_TOKEN_URL,
                redirect_uri=CONST.BASE_URL + "/isAuth/"
            )
        except Exception as e:
            return HttpResponse("Error getting token", status=500)

        models.Notification(
            user=user, 
            code=code,
            token=res.get("access_token", ""),
            rent_url=rent_url
        ).save()
        return HttpResponse("Get authorization code!", status=200)

    return HttpResponse("Only POST method is allowed", status=405)

