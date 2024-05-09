import json, os, requests, dotenv
from bs4 import BeautifulSoup
import CONST
import utils

def lambda_handler(event, context):
    # body = event["body"]
    # url = body["url"]
    # sort_params = body["sort_params"]

    url = f"{CONST.RENT_591_URL}?region=3&section=26,50,38&searchtype=1&other=cook,balcony_1&multiArea=30_40,40_50&showMore=1"
    sort_params = {
        'order': 'money',  # posttime, area
        'orderType': 'desc'  # asc
    }

    house591_spider = utils.House591Spider()
    filter_params = utils.parse_url_arguments(url)
    total_count, houses = house591_spider.search(filter_params, sort_params, want_page=1)
    for house in houses:
        post_id = house["post_id"]
        house_detail = house591_spider.house_detail(post_id)
        break
    
    res = utils.parse_detail(house_detail)

    return {
        "statusCode": 200,
        "body": res,
    }
