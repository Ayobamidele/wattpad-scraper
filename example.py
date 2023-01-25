from wattpad_scraper import Wattpad


EXAMPLE_URL = "https://www.wattpad.com/story/48217861-ruins-harry-potter-1"
EXAMPLE_AUTHOR = "haIfblood"

wt = Wattpad(verbose=True)
wt.login("username", "password")

# Get story by URL
book = wt.get_book_by_url(EXAMPLE_URL)

# Get A reading list
harry_potter = wt.create_reading_list_if_not_exists("Harry Potter")

harry_potter.add_book(book)

harry_potter.remove_book(book)

harry_potter.delete()
