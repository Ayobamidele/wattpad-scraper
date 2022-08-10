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

headers = Headers(
    browser='chrome',
    os='Windows',
    headers=True
)


headers = headers.generate()
response_memory = {}

session = requests.Session()
def get(url):
    if url not in response_memory:
        response_memory[url] = session.get(url,headers=headers)
    return response_memory[url]

def close():
    session.close()
atexit.register(close)