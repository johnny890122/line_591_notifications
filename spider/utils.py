from urllib.parse import urlparse, parse_qs
from typing import Dict

import time, random, requests
from bs4 import BeautifulSoup

class House591Spider():
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
        }

    def search(self, filter_params=None, sort_params=None, want_page=1):
        total_count = 0
        house_list = []
        page = 0

        # 紀錄 Cookie 取得 X-CSRF-TOKEN
        s = requests.Session()
        url = 'https://rent.591.com.tw/'
        r = s.get(url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        token_item = soup.select_one('meta[name="csrf-token"]')

        headers = self.headers.copy()
        headers['X-CSRF-TOKEN'] = token_item.get('content')

        # 搜尋房屋
        url = 'https://rent.591.com.tw/home/search/rsList'
        params = 'is_format_data=1&is_new_list=1&type=1'
        if filter_params:
            # 加上篩選參數，要先轉換為 URL 參數字串格式
            params += ''.join([f'&{key}={value}' for key, value, in filter_params.items()])
        else:
            params += '&region=1&kind=0'
        # 在 cookie 設定地區縣市，避免某些條件無法取得資料
        s.cookies.set('urlJumpIp', filter_params.get('region', '1') if filter_params else '1', domain='.591.com.tw')

        # 排序參數
        if sort_params:
            params += ''.join([f'&{key}={value}' for key, value, in sort_params.items()])

        while page < want_page:
            params += f'&firstRow={page*30}'
            r = s.get(url, params=params, headers=headers)
            if r.status_code != requests.codes.ok:
                print('請求失敗', r.status_code)
                break
            page += 1

            data = r.json()
            total_count = data['records']
            house_list.extend(data['data']['data'])
            # 隨機 delay 一段時間
            time.sleep(random.uniform(2, 5))

        return total_count, house_list

    def house_detail(self, house_id: int):

        # 紀錄 Cookie 取得 X-CSRF-TOKEN, deviceid
        s = requests.Session()
        url = f'https://rent.591.com.tw/home/{house_id}'
        r = s.get(url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        token_item = soup.select_one('meta[name="csrf-token"]')

        # 設定 headers
        headers = self.headers.copy()
        headers['X-CSRF-TOKEN'] = token_item.get('content')
        headers['deviceid'] = s.cookies.get_dict()['T591_TOKEN']
        headers['device'] = 'pc'

        # 取得房屋詳細資料
        url = f'https://bff.591.com.tw/v1/house/rent/detail?id={house_id}'
        r = s.get(url, headers=headers)
        if r.status_code != requests.codes.ok:
            print('請求失敗', r.status_code)
            return
        house_detail = r.json()['data']
        return house_detail

def parse_url_arguments(url: str):
    """
    Parse the query parameters from a given URL.

    Args:
        url (str): The URL to parse.

    Returns:
        dict: A dictionary containing the parsed query parameters.

    Raises:
        ValueError: If the URL scheme is invalid or not supported,
                    if the netloc (domain) is missing,
                    or if there are no query parameters in the URL.
    """

    parsed_url = urlparse(url)
    # Check if the scheme is present and is http or https
    if not parsed_url.scheme or parsed_url.scheme not in ['http', 'https']:
        raise ValueError("Invalid URL scheme. Only 'http' and 'https' are supported.")
    
    # Check if the netloc (domain) is present
    if not parsed_url.netloc:
        raise ValueError("Invalid URL. Netloc (domain) is missing.")
    
    # Check if there are query parameters
    if not parsed_url.query:
        raise ValueError("No query parameters found in the URL.")
    
    query_params = parse_qs(parsed_url.query)

    return {key: value[0] if len(value) == 1 else value for key, value in query_params.items()}
    #TODO: Return a dictionary containing the parsed query parameters

def parse_detail(house_detail: Dict):
    """
    Parse the details of a house.

    Args:
        house_detail (Dict): A dictionary containing the details of a house.

    Returns:
        Dict: A dictionary containing the parsed details of the house.
    """
    
    # TODO: customize the return value
    return {
        "url": house_detail["shareInfo"]["url"],
    }