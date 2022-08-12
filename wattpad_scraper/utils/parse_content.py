from typing import List
from wattpad_scraper.utils.request import get
from wattpad_scraper.utils.log import Log
from bs4 import BeautifulSoup


def chapter_soups(url : str) -> BeautifulSoup:
    page = 1
    soups = []
    while 1:
        res = get(url + '/page/' + str(page))
        soup = BeautifulSoup(res.content, "html.parser")
        next_part = soup.find("div",{"class":["next-up","next-part","orange"]})
        next_part = "next-up next-part orange hidden" in str(next_part)
        soups.append(soup)
        page += 1
        if not next_part:
            break
    return soups
    
    
def parse_content(url : str) -> List[str]:
    """parse wattpad chapters

    Args:
        url (string): chapter url

    Returns:
        list: returns a list of content ether a text or a img url
    """
    log = Log(name="wattpad_log",)
    log.debug("Parsing {}".format(url))
    soups = chapter_soups(url)
    contents = []
    log.info("Got content in {} pages".format(len(soups)))

    for soup in soups:
        ptags = soup.select('p[data-p-id]')
        for p in ptags:
            # check if if p tag have img tag
            if p.find('img') is not None:
                # if p tag have img tag, get img tag src
                img_url = p.find('img').get('src')
                if img_url.startswith('/'):
                    img_url = 'https://www.wattpad.com' + img_url
                contents.append(img_url)
            else:
                # if p tag don't have img tag, get text
                contents.append(p.get_text())
    log.debug("This chapter has {} contents".format(len(contents)))
    return contents