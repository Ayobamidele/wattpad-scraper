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
import json
from .reading_list import access_for_authenticated_user
from bs4 import BeautifulSoup
import re

headers = Headers(
    browser='chrome',
    os='Windows',
    headers=True
)


class Cookie:
    """Parse Cookie File For Request"""

    def __init__(self, file):
        super(Cookie, self).__init__()
        self.file = file
        self.keys_to_keep = ['name', 'value', 'domain', 'path']

    def get_cookies_values(self):
        with open(self.file, 'r') as file:
            cookie_data = json.load(file)
            list_of_cookie_dicts = [{key: item[key] for key in self.keys_to_keep} for item in cookie_data]
        return list_of_cookie_dicts

    def jar_cookies(self):
        cookies = httpx.Cookies()
        for cookie in self.get_cookies_values():
            cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'])
        return cookies.jar


class User:
    """Save User Data For Request"""

    def __init__(self, username=None, password=None, cookie_file=None, user_logged_in=False):
        super(User, self).__init__()
        self.username = username
        self.password = password
        self.cookie_file = cookie_file
        self.user_logged_in = user_logged_in

    def login(self):
        login_endpoint = "https://www.wattpad.com/login?nextUrl=%2Fhome"
        data = {
            "username": self.username if self.username is None else os.environ['WATTPAD_USERNAME'],
            "password": self.password if self.password is None else os.environ['WATTPAD_PASSWORD']
        }
        session.post(login_endpoint, data=data, headers=headers)

    @access_for_authenticated_user
    def get_user_details(self, data=None):
        if data is None:
            response = session.post('https://www.wattpad.com/home')
            data = response.text
        soup = BeautifulSoup(data, 'html.parser')
        scripts = soup.find_all('script')
        script = [script for script in scripts if "wattpad.user =" in script.text][0].text
        pattern = re.compile(r"wattpad.user = (.*?);$", re.MULTILINE | re.DOTALL)
        scriptParse = re.search(pattern, str(script))
        userData = json.loads(scriptParse.groups(1)[0])
        return userData

    def cookie_login(self):
        cookie = Cookie(self.cookie_file)
        cookie_jar = cookie.jar_cookies()
        login_endpoint = "https://www.wattpad.com/login"
        session.cookies.jar = cookie_jar
        session.follow_redirects = True
        response = session.post(login_endpoint, headers=headers)
        data = self.get_user_details(response.text)
        self.username = data['username']


class Author(User):
    """Inherits properties of user"""



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
            return pickle.load(f)
    else:
        return {}


headers = headers.generate()
response_memory = load_response()

session = httpx.Client(headers=headers)


def user_login():
    if not os.environ['USER_LOGGED_IN']:
        user = User()
        if "WATTPAD_USERNAME" in os.environ and "WATTPAD_PASSWORD" in os.environ:
            user.username = os.environ['WATTPAD_USERNAME']
            user.password = os.environ['WATTPAD_PASSWORD']
            user.login()
        elif "WATTPAD_COOKIE_FILE" in os.environ:
            user.cookie_file = os.environ['WATTPAD_COOKIE_FILE']
            User.cookie_login()
        os.environ['USER_LOGGED_IN'] = 'True'
        user.user_logged_in = True


def get(url):
    user_login()

    if url not in response_memory:
        response_memory[url] = session.get(url)
    return response_memory[url]


def close():
    session.close()
    store_response()


atexit.register(close)
