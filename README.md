# Wattpad Scraper(wattpad stories downloader)
[![Downloads](https://static.pepy.tech/personalized-badge/wattpad-scraper?period=total&units=international_system&left_color=black&right_color=blue&left_text=Downloads)](https://pepy.tech/project/wattpad-scraper)
<br>
Get wattpad stories, download wattpad stories, convert wattpad stories to ebook (epub/pdf [In Development])

## Major Features
- Search books 
- Get book by wattpad url
- Convert books to epub
- Login to wattpad

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

### Create Users Book List
```python
#First login to perform actions on your book list
from wattpad_scraper.utils import ReadingList

readingList = ReadingList()

readingList.create_reading_list("Super Fly")
```

### Get Users Book List
Gets the Books in a reading list
```python
from wattpad_scraper.utils import ReadingList

readingList = ReadingList()

# By default without passsing any arguement it returns all your reading lists 
readingList.get_reading_list()

#Get your reading list by it's title
readingList.get_reading_list(title="Super Fly")

# Get all users reading list
readingList.get_reading_list(username="Ghost_Lord")

#Get the reading list of a user by their title
readingList.get_reading_list(title="GEMS", username="Ghost_Lord")
```


### Delete Reading List
```python
from wattpad_scraper.utils import ReadingList

readingList = ReadingList()

readingList.delete_reading_list("Super Fly")
```


### Add a book to a reading list
```python
from wattpad_scraper.utils import ReadingList

readingList = ReadingList()

readingList.add_to_reading_list(urlOfBook="https://www.wattpad.com/story/116064909-around-the-world-in-80-days-completed", titleOfReadingList="Hype")
```

### Get Authors Book List
```python
from wattpad_scraper.utils import ReadingList

readingList = ReadingList()

readingList.author_book_list("amberkbryant")

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

## Auth System

## Login with username and password
```python
from wattpad_scraper import Wattpad as wt

w = wt()
w.login(username="username", password="password")
book= w.search_books("Rules") 
contents = book.chapters[2].content
# better search books that are not shown in search results for non logged users.
# More features are coming soon.
```

### Login with cookies
1. Download an extension called "Cookie - Editor" in your browser.
2. Open the extension and click Export.
3. Save copied text in to a file and rename with the `` .json`` extension.
4. Copy file location
```python
from wattpad_scraper import Wattpad as wt

w = wt(cookie_file='/home/Desktop/wattpad-cookies.json')
w.search_books("Rules")
```


### Working with reading list
```python
from wattpad_scraper import Wattpad as wt

w = wt()
w.login(username="username", password="password")

# Create a reading list
reading_list = w.create_reading_list("Super Fly")

# Get a reading list by it's title (For logged in user)
super_fly = w.get_reading_list("Super Fly")

# Get a reading list by it's id
super_fly = w.get_reading_list(123456)

# Get a reading list by it's url
super_fly = w.get_reading_list("https://www.wattpad.com/list/123456-super-fly")

# Get all reading lists of a user
reading_lists = w.get_user_reading_lists("Ghost_Lord")
# alternatively you can use id or url of the user

# Add a book to a reading list
book = w.search_books("Rules")[0]
w.add_to_reading_list(book, reading_list)
# alternatively you can use id or url of the book
w.add_to_reading_list(book.id, reading_list.id)
w.add_to_reading_list(book.url, reading_list.url)

# You can also add a book to a reading list from the reading list object
reading_list.add_book(book)

# Remove a book from a reading list
w.remove_from_reading_list(book, reading_list)
# alternatively you can use id or url of the book
w.remove_from_reading_list(book.id, reading_list.id)
w.remove_from_reading_list(book.url, reading_list.url)

# You can also remove a book from a reading list from the reading list object
reading_list.remove_book(book)

# Delete a reading list
w.delete_reading_list(reading_list)
# alternatively you can use id or url of the reading list
w.delete_reading_list(reading_list.id)
w.delete_reading_list(reading_list.url)

# You can also delete a reading list from the reading list object
reading_list.delete()

# Get all books in a reading list
books = reading_list.books # returns a list of Book objects
```



