from wattpad_scraper import Wattpad


wattpad = Wattpad()
books = wattpad.search_book("harry potter",limit=10)
print(books[0].chapters[0].content) # on search book chapters have to load first so it may take a while
print(len(books))