import cloudscraper


requests = cloudscraper.create_scraper(
    browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    }
)
response_memory = {}


def get(url):
    if url not in response_memory:
        response_memory[url] = requests.get(url)
    return response_memory[url]
