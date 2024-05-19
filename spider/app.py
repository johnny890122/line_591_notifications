import json, os, requests, dotenv
from bs4 import BeautifulSoup
import CONST
import utils
import urllib.parse

def lambda_handler(event, context):
    body = urllib.parse.parse_qs(event["body"])
    url = body["url"][0]

    sort_params = {
        'order': 'posttime',  # posttime, area
        'orderType': 'desc'  # asc
    }

    house591_spider = utils.House591Spider()
    filter_params = utils.parse_url_arguments(url)
    total_count, houses = house591_spider.search(filter_params, sort_params, want_page=1)
    
    counter = 0
    res = []
    for house in houses:
        if counter >= 2:
            break
        else:
            counter += 1
        house_detail = house591_spider.house_detail(house["post_id"])
        res.append(utils.parse_detail(house_detail))

    return {
        "statusCode": 200,
        "body": res,
    }
