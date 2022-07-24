# wattpad-scraper
Easy to use wattpad scraper

### Important Links
- [GitHub](https://github.com/shhossain/wattpad-scraper)
- [PYPI](https://pypi.org/project/wattpad-scraper/)

## Installation

```bash
pip install wattpad-scraper
```

## Usage

### Get Book By Url
```python
from wattpad_scraper import Wattpad

wattped = Wattpad()
book_url = "https://www.wattpad.com/story/162756571-bending-the-rules-the-rules-1"
book = wattped.get_book_by_url(book_url)
print(book.title) # "Bending the Rules: The Rules 1"
print(book.author.name, book.author.url) 
print(book.description)
print(book.chapters)
print(book.chapters[0].title,book.chapters[0].content)
```

### Search Books
```python
from wattpad_scraper import Wattpad

wattpad = Wattpad()
books = wattpad.search_book("harry potter",limit=10)
print(books[0].chapters[0].content) # on search book chapters have to load first so it may take a while
print(len(books)) # 10
```
