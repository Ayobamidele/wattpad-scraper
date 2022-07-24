# wattpad-scraper
Easy to use wattpad scraper


## Installation

```bash
pip install wattpad-scraper
```

## Usage

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
