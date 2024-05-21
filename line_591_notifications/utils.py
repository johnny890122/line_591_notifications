import urllib, json, requests, time, random, ast, hashlib
from typing import Dict, List
from django.utils.crypto import get_random_string
from line_591_notifications import CONST
import line_591_notifications.spider.crawler as crawler
from urllib.parse import parse_qs, urlparse

def hash(str: str) -> str:
    """
    Hashes the input string using SHA-256 algorithm.

    Args:
        str (str): The string to be hashed.

    Returns:
        str: The hashed string.

    """
    return hashlib.sha256(str.encode()).hexdigest()

def generate_csrf_token() -> str:
    """
    Generate a CSRF token.

    Returns:
        str: The generated CSRF token.
    """
    csrf_token = get_random_string(length=32)
    return csrf_token

def get_token(
        code:str, client_id:str, client_secret:str, 
        redirect_uri:str, token_url:str, grant_type:str='authorization_code'
    ) -> str:
    """
    Retrieves an access token from the token URL using the provided code and credentials.

    Args:
        code (str): The authorization code.
        client_id (str): The client ID.
        client_secret (str): The client secret.
        redirect_uri (str): The redirect URI.
        token_url (str): The token URL.
        grant_type (str, optional): The grant type. Defaults to 'authorization_code'.

    Returns:
        str: The access token.

    Raises:
        requests.RequestException: If there is a request-related error.
        KeyError: If there is a missing key in the JSON response.
        json.JSONDecodeError: If there is a JSON decoding error.
        Exception: If there is any other unexpected error.
    """
    
    try:
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        data = {
            'grant_type': grant_type, 'code': code,
            'client_id': client_id, 'client_secret': client_secret, 
            'redirect_uri': redirect_uri,
        }
        res = requests.post(
            url=token_url, headers=headers, data=data
        )
        res.raise_for_status()  # Raise an HTTPError for bad responses
        return res.json()
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

def get_url_arguments(url: str):
    parsed_url = urlparse(url)
    if not parsed_url.scheme or parsed_url.scheme not in ['http', 'https']:
        raise ValueError("Invalid URL scheme. Only 'http' and 'https' are supported.")
    
    if not parsed_url.netloc:
        raise ValueError("Invalid URL. Netloc (domain) is missing.")
    
    if not parsed_url.query:
        raise ValueError("No query parameters found in the URL.")
    
    query_params = parse_qs(parsed_url.query)

    #TODO: Return a dictionary containing the parsed query parameters
    return {key: value[0] if len(value) == 1 else value for key, value in query_params.items()}

def extract_detail(detail: Dict):    
    # TODO: customize the return value
    return {
        "url": detail["shareInfo"]["url"],
    }

def crawl_591(url: str):
    house591_spider = crawler.House591Spider()
    houses = house591_spider.search(
        filter_params=get_url_arguments(url), 
        sort_params=CONST.SORT_PARAMS,
        max_houses=CONST.MAX_HOUSE
    )
    
    res = []
    for house in houses:
        house_detail = house591_spider.house_detail(house["post_id"])
        res.append(extract_detail(house_detail))

    return res

def notify(token: str, rent_url: str) -> requests.Response:
    headers = {'Authorization': 'Bearer ' + token}
    results = crawl_591(rent_url)
    for result in results:
        res = requests.post(
            url=CONST.NOTIFY_URL, headers=headers,
            data={'message': result["url"]}
        )
    return res
