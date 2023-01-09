from wattpad_scraper import Wattpad


url = "https://www.wattpad.com/story/304168482-to-the-moon-and-back"


class TestDownloader:
    def test_convert_to_epub(self):
        wt = Wattpad()
        book = wt.get_book_by_url(url)
        book.convert_to_epub()
        assert book is not None
    

if __name__ == "__main__":
    t = TestDownloader()
    t.test_convert_to_epub()
