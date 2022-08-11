# import cloudscraper


# requests = cloudscraper.create_scraper(
#     browser={
#         'browser': 'firefox',
#         'platform': 'windows',
#         'mobile': False
#     }
# )
# response_memory = {}


# def get(url):
#     if url not in response_memory:
#         response_memory[url] = requests.get(url)
#     return response_memory[url]

import requests
from fake_headers import Headers
import atexit
import os

headers = Headers(
    browser='chrome',
    os='Windows',
    headers=True
)

def login(username,password):
    login_endpoint  ="https://www.wattpad.com/login?nextUrl=%2Fhome"
    data = {
        "username": username,
        "password": password
    }
    session.post(login_endpoint,data=data,headers=headers)

headers = headers.generate()
response_memory = {}

session = requests.Session()
USER_LOGGED_IN = [False]



def get(url):
    if not USER_LOGGED_IN[0]:
        if "WATTPAD_USERNAME" in os.environ and "WATTPAD_PASSWORD" in os.environ:
            login(os.environ['WATTPAD_USERNAME'],os.environ['WATTPAD_PASSWORD'])
        USER_LOGGED_IN[0] = True

    if url not in response_memory:
        response_memory[url] = session.get(url,headers=headers)
    return response_memory[url]

def close():
    session.close()
atexit.register(close)