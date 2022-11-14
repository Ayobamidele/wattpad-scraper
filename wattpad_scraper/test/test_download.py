from wattpad_scraper import Wattpad


url = "https://www.wattpad.com/story/228886227-looking-glass-and-the-cube-of-orion-hmk-book-1-%E2%9C%94%EF%B8%8F"


class TestDownloader:
    def test_convert_to_epub(self):
        wt = Wattpad()
        book = wt.get_book_by_url(url)
        book.convert_to_epub()
        assert book is not None
    

