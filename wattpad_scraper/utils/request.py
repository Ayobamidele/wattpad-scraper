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

import httpx
from fake_headers import Headers
import atexit
import os
import pickle


headers = Headers(
    browser='chrome',
    os='Windows',
    headers=True
)
temp_dir_path = "temp_catch_delete_if_not_needed"
if not os.path.exists(temp_dir_path):
    os.mkdir(temp_dir_path)

res_path = os.path.join(temp_dir_path, "response_memory.pickle")
session_path = os.path.join(temp_dir_path, "session.pickle")

def store_response():
    # store response memory in pickle file
    with open(os.path.join(temp_dir_path, "response_memory.pickle"), "wb") as f:
        pickle.dump(response_memory, f)

def load_response():
    # load response memory from pickle file
    if os.path.exists(res_path):
        with open(res_path, "rb") as f:
            response_memory = pickle.load(f)
    else:
        response_memory = {}
    return response_memory


def login(username,password):
    login_endpoint  ="https://www.wattpad.com/login?nextUrl=%2Fhome"
    data = {
        "username": username,
        "password": password
    }
    session.post(login_endpoint,data=data,headers=headers)




headers = headers.generate()
response_memory = load_response()


session = httpx.Client(headers=headers)
USER_LOGGED_IN = [False]


def get(url):
    if not USER_LOGGED_IN[0]:
        if "WATTPAD_USERNAME" in os.environ and "WATTPAD_PASSWORD" in os.environ:
            login(os.environ['WATTPAD_USERNAME'],os.environ['WATTPAD_PASSWORD'])
        USER_LOGGED_IN[0] = True

    if url not in response_memory:
        response_memory[url] = session.get(url)
    return response_memory[url]

def close():
    session.close()
    store_response()

atexit.register(close)