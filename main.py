from wattpad_scraper import Wattpad as wt

w = wt()
books = w.search_book('game of thrones')
print(books)