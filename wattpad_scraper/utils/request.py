import httpx
from fake_headers import Headers
import atexit
import os
import pickle
import json
from bs4 import BeautifulSoup
import re
from collections import defaultdict

MAX_RESPONSES = 1000

header = Headers(
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
            return pickle.load(f)
    else:
        return defaultdict(int)

def access_for_authenticated_user(func):
    def is_authenticated(*args, **kwargs):
        if os.environ.get('USER_LOGGED_IN') is None:
            return "No Access Until Logged In"
        else:
            return func(*args, **kwargs)

    return is_authenticated

headers = header.generate()
response_memory = load_response()
session = httpx.Client(headers=headers)

class Cookie:
    """Parse Cookie File For Request"""

    def __init__(self, file):
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
    """User Class"""

    def __init__(self, username=None, password=None, cookie_file=None, user_logged_in=False):
        self.username:str = username if username else ""
        self.password:str = password if password else ""
        self.cookie_file = cookie_file
        self.user_logged_in = user_logged_in

    def login(self):
        login_endpoint = "https://www.wattpad.com/login"
        data = {
            "username": self.username,
            "password": self.password
        }
        os.environ['WATTPAD_USERNAME'] = self.username
        os.environ['WATTPAD_PASSWORD'] = self.password
        
        session.post(login_endpoint, data=data, headers=headers)
        self.check_login()
        
    
    def check_login(self) -> bool:
        # https://www.wattpad.com/user/sh0339
        response = session.get(f"https://www.wattpad.com/user/{self.username}")
        soup = BeautifulSoup(response.text, 'html.parser')
        # #alias @sh0339
        alias = soup.find(id="alias").text #type: ignore
        if alias == f"@{self.username}":
            self.user_logged_in = True
            os.environ['USER_LOGGED_IN'] = 'True'
            return True
        else:
            os.environ['USER_LOGGED_IN'] = 'False'
            return False
        
        

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
        userData = json.loads(scriptParse.groups[0]) #type: ignore
        return userData

    def cookie_login(self):
        cookie = Cookie(self.cookie_file)
        cookie_jar = cookie.jar_cookies()
        login_endpoint = "https://www.wattpad.com/login"
        session.cookies.jar = cookie_jar
        session.follow_redirects = True
        response = session.post(login_endpoint, headers=headers)
        if response.status_code == 200:
            self.user_logged_in = True
            os.environ['USER_LOGGED_IN'] = 'True'
            data = self.get_user_details(response.text)
            self.username = data['username']
        else:
            os.environ['USER_LOGGED_IN'] = 'False'
        





def user_login(username=None, password=None, cookie_file=None):
    user = User(username, password, cookie_file)
    if cookie_file is not None:
        user.cookie_login()
    else:
        user.login()
    return user

def save_response(url, res):
    if len(response_memory) > MAX_RESPONSES:
        response_memory.clear() 
    response_memory[url] = res

def get(url) -> httpx.Response: 
    if response_memory[url] == 0:
        res = session.get(url)
        save_response(url, res)
    else:
        res = response_memory[url]
    return response_memory[url] # type: ignore

    

def close():
    session.close()
    store_response()


atexit.register(close)
