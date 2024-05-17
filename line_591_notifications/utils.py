import urllib, json, requests
from typing import Dict
from django.utils.crypto import get_random_string
from urllib.parse import urlparse, parse_qs
from line_591_notifications import CONST

def generate_csrf_token() -> str:
    """
    Generate a CSRF token.

    Returns:
        str: The generated CSRF token.
    """
    csrf_token = get_random_string(length=32)
    return csrf_token

def get_line_token(
        code:str, client_id:str, client_secret:str, 
        redirect_uri:str, token_url:str
    ) -> str:
    """
    Retrieves an access token using the provided authorization code.

    Args:
        code (str): The authorization code.
        client_id (str): The client ID.
        client_secret (str): The client secret.
        redirect_uri (str): The redirect URI.
        token_url (str): The authorization URL.

    Returns:
        str: The access token.

    Raises:
        requests.RequestException: If there is an error with the request.
        KeyError: If a required key is missing in the JSON response.
        json.JSONDecodeError: If there is an error decoding the JSON response.
        Exception: For any other unexpected errors.

    """
    try:
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret
        }
        res = requests.post(
            url=token_url, params=data, headers=headers
        )
        res.raise_for_status()  # Raise an HTTPError for bad responses
        data = res.json()  # Automatically parse JSON response
        return data["access_token"]
    except requests.RequestException as e:
        # Handle any request-related errors
        print(f"Request Error: {e}")
    except KeyError as e:
        # Handle missing key in JSON response
        print(f"KeyError: {e}")
    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        print(f"JSONDecodeError: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected Error: {e}")

    return None  # Return None in case of error

def parse_rent_url(url: str) -> Dict[str, str]:
    """
    Parses the given URL and returns a dictionary of query parameters.

    Args:
        url (str): The URL to parse.

    Returns:
        dict: A dictionary containing the query parameters as key-value pairs.

    Raises:
        None
    """
    try:
        parsed_url = urlparse(url)
        if not parsed_url.query:
            return {}
        query_params = parse_qs(parsed_url.query)
        return {k: v[0] for k, v in query_params.items()}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

def notify(token: str) -> requests.Response:
    headers = {'Authorization': 'Bearer ' + token}
    message = {'message': parser()}

    res = requests.post(
        url=CONST.NOTIFY_URL, headers=headers,
        data=message
    )
    return res

def parser():
    return "喵喵喵"