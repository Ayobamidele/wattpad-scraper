from cgi import test
import imp
import unittest

from wattpad_scraper import Wattpad

class TestWattpadDownloader(unittest.TestCase):
  def test_check_url(self):

    wattpad = Wattpad()
    result = wattpad.search_book("harry potter", limit=10)

    example_url = "https://www.wattpad.com/story/48217861-ruins-harry-potter-1"
    test_url = result[2].url

    self.assertEqual(example_url, test_url)

  def test_search_one_book(self):
    wattpad = Wattpad()
    result = wattpad.search_book("harry potter", limit=10)

    example_book = ["This story takes place in, but does not directly follow the events, Harry Potter: The Goblet of Fire. I will reference to the movie script every now and then, but will not follow how every scene is laid out. This story was inspired by Taylor Swift's song, How You Get the Girl, so I highly suggest checking the song out if you haven't heard it before (and checking it out again because it's amazing).", "Feel free to point out any grammar errors or parts that don't make any sense. This will improve my writing and hopefully improve the story. It's been edited as of July 9th, 2016 but sometimes I miss some mistakes and parts that had a gap for a scene change in the original draft but the gap disappeared upon copying it over here. ", "I'd like to warn everyone that Harry is very OOC (out of character) and does act inappropriately. I'm aware of that and apologize in advance for any strange comments from him. (You will find that he randomly spills sexual comments and I'm hanging my head in shame because Harry is awkward when it comes to relationships, but not that awkward).", 'I would like to thank She Who Must Not Be Named for creating such a magical world that we can all just dive into. Although I am still not over not being accepted into Hogwarts and not experiencing the whole experience, at least I can read (and watch movies) about it.', 'Onwards with the story. ☺️']
    test_book = result[0].chapters[0].content
    
    self.assertEqual(example_book , test_book)

if __name__ == "__main__":
  unittest.main()