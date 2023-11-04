# Wattpad Scraper(wattpad stories downloader)
[![Downloads](https://static.pepy.tech/personalized-badge/wattpad-scraper?period=total&units=international_system&left_color=black&right_color=blue&left_text=Downloads)](https://pepy.tech/project/wattpad-scraper)
<br>
Get wattpad stories, download wattpad stories, convert wattpad stories to ebook (epub/pdf [In Development])

## Announcement!!!
I'm thrilled to announce that the package is now under my fresh and dynamic new ownership! Exciting changes are on the horizon as I embark on a journey of development and innovation. I'm currently working on an experimental web extension that mirrors the capabilities of the package. Stay tuned for a blend of professionalism and friendliness in my upcoming updates. I can't wait to bring you along on this exciting adventure!


## Major Features
- Search books 
- Get book by wattpad url
- Convert books to epub
- Login to wattpad

### Important Links
- [GitHub](https://github.com/Ayobamidele/wattpad-scraper)

## Installation

```bash
pip install wattpad-scraper
```

## Usage

### Get Book By Url
```python
from wattpad_scraper import Wattpad

wattped = Wattpad()
# wattpad = Wattpad(verbose=True)  if you want to see output in console
book_url = "https://www.wattpad.com/story/162756571-bending-the-rules-the-rules-1"
book = wattped.get_book_by_url(book_url)
print(book.title) # "Bending the Rules: The Rules 1"
print(book.author.name, book.author.url) 
print(book.description)
print(book.chapters)
print(book.chapters[0].title,book.chapters[0].content)

# Content is a List of strings and image urls.

```

### Search Books
```python
from wattpad_scraper import Wattpad

wattpad = Wattpad()
books = wattpad.search_books('harry potter by joekih01',completed=True,mature=True,free=True,paid=True,limit=10) 
print(books[0].chapters[0].content) # on search book chapters have to load first so it may take a while
print(len(books)) # 10
```

### Convert Book to Epub
```python
from wattpad_scraper import Wattpad as wt

w = wt()
books = w.search_books('harry potter by joekih01')
book = books[0]
book.convert_to_epub() # will save book to epub file in current directory

# book.convert_to_epub(loc='/path/to/save/book/to/epub') # to save book to specific location
# book.convert_to_epub(verbose=False) # to disable terminal outputs while converting

```

### Auth System (Beta) (More Features are coming soon)
```python
from wattpad_scraper import Wattpad as wt

w = wt("wattpad_username","wattpad_password")
book= w.search_books("Rules") 
contents = book.chapters[2].content
# better search books that are not shown in search results for non logged users.
# More features are coming soon.
```

#### Cookie authentication
1. Download an extension called "Cookie - Editor" in your browser.
2. Open the extension and click Export.
3. Save copied text in to a file and rename with the `` .json`` extension.
4. Copy file location
```python
from wattpad_scraper import Wattpad as wt

w = wt(cookie_file='/home/Desktop/wattpad-cookies.json')
w.search_books("Rules")
```

