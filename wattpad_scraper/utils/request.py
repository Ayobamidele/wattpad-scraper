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
import re
from bs4 import BeautifulSoup

class Cookie():
    """Parse Cookie File For Request"""
    def __init__(self, file):
        super(Cookie, self).__init__()
        self.file = file
        self.keys_to_keep  = ['name', 'value', 'domain', 'path']

    
    def get_cookies_values(self):
        with open(self.file, 'r') as file:
            cookie_data = json.load(file)       
            list_of_cookie_dicts = [{ key: item[key] for key in self.keys_to_keep } for item in cookie_data]
        return list_of_cookie_dicts

    def jar_cookies(self):
        cookies = httpx.Cookies()
        for cookie in self.get_cookies_values():
            cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'])
        return cookies.jar



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


def access_for_authentcated_user(func):
    def is_authenticated(*args, **kwargs):
        if not USER_LOGGED_IN[0]:
            return "No Access Until Logged In"
        else:
            func(*args, **kwargs)
    return is_authenticated

def error(str):
    raise ValueError(str)

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

@access_for_authentcated_user
def get_user_details(data=None):
    if data == None:
        response = session.post('https://www.wattpad.com/home')
        data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    scripts = soup.find_all('script')
    script = [script for script in scripts if "wattpad.user =" in script.text][0].text
    pattern = re.compile(r"wattpad.user = (.*?);$", re.MULTILINE | re.DOTALL)
    scriptParse = re.search(pattern, str(script))
    userData = json.loads(scriptParse.groups(1)[0])
    return userData

def login(username,password):
    login_endpoint  ="https://www.wattpad.com/login?nextUrl=%2Fhome"
    data = {
        "username": username,
        "password": password
    }
    session.post(login_endpoint,data=data,headers=headers)


def cookie_login(file):
    cookie = Cookie(file)
    cookie_jar = cookie.jar_cookies()
    login_endpoint = "https://www.wattpad.com/login"
    session.cookies.jar = cookie_jar
    session.follow_redirects = True
    response = session.post(login_endpoint,headers=headers)
    data = get_user_details(response.text)
    os.environ['WATTPAD_USERNAME'] = data['username']

@access_for_authentcated_user
def create_reading_list(self, Title):
    json_data = {
    'id': None,
    'name': Title,
    'numStories': 0,
    'cover': 0,
    'tags': [],
    'featured': False,
    'action': 'create',
    }
    response = session.post('https://www.wattpad.com/api/v3/lists/', headers=headers, json=json_data)
    if response.status_code == 200:
        print(f'{Title} - Reading List was Successfully Created !!!')
        return True
    else:
        print(response.json()['message'])
        return False


def author_book_list(author_username):
    response = session.get(f"https://www.wattpad.com/v4/users/{author_username}/stories/published?offset=0&limit=102")
    return response.json()

def get_reading_list(id=None, title=None, username=None):
    if username == None:
        username = error("No Access Until Logged In") if not USER_LOGGED_IN[0] else os.environ['WATTPAD_USERNAME']
    response = session.get(f"https://www.wattpad.com/api/v3/users/{username}/lists")
    reading_list = response.json()['lists']
    if title != None or id != None:
        if title != None:
            reading_list = [ a for a in reading_list if a['name'] == title ]
        elif id != None:
            reading_list = [ a for a in reading_list if a['id'] == id ]
        return reading_list[0] if len(reading_list) > 0 else error("Reading List Does Not Exist !!")
    return reading_list

@access_for_authentcated_user
def delete_reading_list(Title):
    id = get_reading_list(title=Title)['id']
    response = session.delete(f'https://www.wattpad.com/api/v3/lists/{id}', headers=headers)
    # print(response, response.text,id, type(id))
    if response.status_code == 200:
        print(f'{Title} - Reading List was Successfully Deleted !!!')
        return True
    else:
        print(response.json()['message'])
        return False

@access_for_authentcated_user
def add_to_reading_list(idOfBook=None, urlOfBook=None, titleOfReadingList=None, idOfReadingList=None):
    book_id = idOfBook if urlOfBook == None else (urlOfBook.split("/"))[-1].split("-")[0]
    data = {
    'stories': str(book_id),
    }
    reading_list = idOfReadingList if titleOfReadingList == None else get_reading_list(title=titleOfReadingList)['id']
    response = session.post(f'https://www.wattpad.com/api/v3/lists/{str(reading_list)}/stories', headers=headers, data=data)
    if response.status_code == 200:
        print(f'The Book was Successfully Addeed to {get_reading_list(id=reading_list)["name"]}!!!')
        return True
    else:
        print(response.json()['message'])
        return False





headers = headers.generate()
response_memory = load_response()


session = httpx.Client(headers=headers)
USER_LOGGED_IN = [False]


def get(url):
    if not USER_LOGGED_IN[0]:
        if "WATTPAD_USERNAME" in os.environ and "WATTPAD_PASSWORD" in os.environ:
            login(os.environ['WATTPAD_USERNAME'],os.environ['WATTPAD_PASSWORD'])
        elif "WATTPAD_COOKIE_FILE" in os.environ:
            cookie_login(os.environ['WATTPAD_COOKIE_FILE'])
        USER_LOGGED_IN[0] = True

    if url not in response_memory:
        response_memory[url] = session.get(url)
    return response_memory[url]

def close():
    session.close()
    store_response()

atexit.register(close)