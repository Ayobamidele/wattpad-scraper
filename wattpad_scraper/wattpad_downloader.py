from typing import List, Union
from bs4 import BeautifulSoup
from wattpad_scraper.models import Author, Book, Chapter, Status
from wattpad_scraper.utils.request import get, user_login
from wattpad_scraper.utils.log import Log
from urllib.parse import quote
import os
from wattpad_scraper.utils.reading_list import ReadingListRequest, ReadingList
from wattpad_scraper.utils.request import access_for_authenticated_user, User


class Wattpad:
    def __init__(self, verbose=False) -> None:
        """
        Initialize the Wattpad class.
        
        Args:
            username (string)(optional): username or email
            password (string)(optional): password
            verbose (bool)(optional): verbose mode default False
        """
        self.verbose = verbose
        os.environ["WATTPAD_VERBOSE"] = str(verbose)
        self.log = Log(name="wattpad_log", verbose=verbose)

        self.main_url = "https://www.wattpad.com"
        self.user: User = None # type: ignore
        self.reading_list_req = ReadingListRequest(verbose=verbose)
    
    def login(self, username=None, password=None, cookie_file=None):
        """
        Login to Wattpad

        Args:
            username (string): username or email
            password (string): password
        """
        self.log.print("Logging in as {}".format(username), color="green")
        self.user = user_login(username, password, cookie_file)
        self.reading_list_req.user = self.user
        if 'USER_LOGGED_IN' in os.environ and os.environ['USER_LOGGED_IN'] == 'True':
            self.log.print("Logged in successfully", color="green")
        else:
            self.log.print("Login failed", color="red") 

    def get_book_by_url(self, url) -> Book:
        """
        Args:
            url (string): book url

        Returns:
            Book: returns a Book object

            Book object has the following attributes:
                url (string): book url
                name (string): book name
                author (Author): author object
                img_url (string): book image url
                tags (list): list of tags
                description (string): book description
                published (string): book published date
                reads (int): book reads
                votes (int): book votes
                status (Status): book status
                isMature (bool): book is mature
                chapters (list): list of chapter objects
        """

        response = get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Get book stats
        stats:[BeautifulSoup] = soup.find(class_='new-story-stats') # type: ignore
        if stats is None:
            raise Exception("Book not found", url)
        
            
        lis = stats.find_all('li') 

        reads = lis[0].find(
            class_="sr-only").get_text().replace('Reads', '').replace(',', '').strip()
        reads = int(reads)

        votes = lis[1].find(
            class_="sr-only").get_text().replace('Votes', '').replace(',', '').strip()
        votes = int(votes)

        parts = lis[2].find(
            class_="sr-only").get_text().replace('Parts', '').strip()
        parts = int(parts)

        # class : story-badges
        badges = soup.find(class_='story-badges')
        if badges is None:
            self.log.error("Badges not found", url)
        
        if badges:
            completed = badges.find(
                class_="tag-item").get_text().lower().startswith('com')  # type: ignore
            published = badges.find(
            class_='sr-only').get_text().split('First published ')[1] # type: ignore
        else:
            completed = False
            published = None
        status = None
        if completed:
            status = Status.COMPLETED
        else:
            status = Status.ONGOING

        # is mature class mature
        mature = badges.find(class_="mature") is not None # type: ignore

        # published sr-only > ex. Complete, First published Sep 25, 2018

        

        # description class description-text
        description = soup.find(class_='description-text')
        if description is None:
            self.log.error("Description not found", url)
            description = ""
        else:
            description = description.get_text().strip()
        

        # Get Chapters - Class: "story-chapter-list" > li > List<a> > text,href
        toc:[BeautifulSoup] = soup.find(class_='table-of-contents') # type: ignore
        if toc is None:
            raise Exception("Table of Contents not found", url)

        lis = toc.find_all('li') 
        chapters = []
        for n, li in enumerate(lis):
            a = li.find('a')
            url = a.get('href')
            if url.startswith('/'):
                url = self.main_url + url
            ch = Chapter(
                url=url, title=a.get_text().strip().replace('\n', ' '), chapter_number=n + 1)
            chapters.append(ch)

        # Get Title class: "sr-only" > text (title)
        title = soup.find(class_='sr-only')
        if title is None:
            self.log.error("Title not found", url)
            title = ""
        else:
            title = title.get_text().strip()


        # Get Author class: "author-info" > img,a > img:src,a:href,a:text
        author_info:BeautifulSoup = soup.find(class_='author-info') # type: ignore
        
        imgurl = author_info.find('img')
        img_url:str = ""
        if imgurl is not None:
            img_url = imgurl.get('src') # type: ignore
        else:
            self.log.error("Author image not found", url)

            
            
        if img_url.startswith('/'):
            img_url = self.main_url + img_url
        a = author_info.find('a')
        author_url:str = ""
        author_username:str = ""
        if a is None:
            self.log.error("Author not found", url)
        else:
            author_url = a.get('href') # type: ignore
        if author_url.startswith('/'):
            author_url = self.main_url + author_url
            author_username = a.get_text().strip() # type: ignore
        
            
        author = Author(url=author_url, username=author_username,
                        author_img_url=img_url)

        # Get Image class: "story-cover" > img > src
        book_img_url = soup.find(class_='story-cover').find('img').get('src') # type: ignore
        if book_img_url.startswith('/'): # type: ignore
            book_img_url = self.main_url + book_img_url # type: ignore
 
        # Get Tags class: tag-items > li > a > text
        tags = []
        tag_items = soup.find(class_='tag-items')
        if tag_items is not None:
            lis = tag_items.find_all('li') # type: ignore
            for li in lis:
                tags.append(li.find('a').get_text())

        # Get Book object
        if not isinstance(book_img_url, str):
            book_img_url = str(book_img_url)
        
        if not isinstance(published, str):
            published = str(published)
        
        book = Book(url=url, title=title, author=author, img_url=book_img_url, description=description,
                    published=published, isMature=mature, reads=reads, votes=votes, chapters=chapters,
                    total_chapters=parts, tags=tags, status=status)
        return book

    def search_books(self, query: str, limit: int = 15, mature: bool = True, free: bool = True, paid: bool = True,
                     completed: bool = False, show_only_total: bool = False) -> List[Book]: #type: ignore
        """
        Args:
            query (string): search query

        Returns:
            List[Book]: returns a list of Book objects
        """
        self.log.debug("Searching for '{}'".format(query),
                       "with options: mature={},free={},paid={},completed={},show_only_total={}".format(mature, free,
                                                                                                        paid, completed,
                                                                                                        show_only_total))
        mature_str = "&mature=true" if mature else ""
        free_str = "&free=1" if free else ""
        paid_str = "&paid=1" if paid else ""
        completed_str = "&filter=complete" if completed else ""

        parsed_query = quote(query)
        url = f"https://www.wattpad.com/v4/search/stories?query={parsed_query}{completed_str}{mature_str}{free_str}{paid_str}&fields=stories(id,title,voteCount,readCount,commentCount,description,completed,mature,cover,url,isPaywalled,length,language(id),user(name),numParts,lastPublishedPart(createDate),promoted,sponsor(name,avatar),tags,tracking(clickUrl,impressionUrl,thirdParty(impressionUrls,clickUrls)),contest(endDate,ctaLabel,ctaURL)),chapters(url),total,tags,nexturl&limit={limit}&offset=0"
        response = get(url)
        json_data = response.json()
        is_error = False
        er: Exception = Exception("Unknown Error")
        if not show_only_total:
            try:
                self.log.info(f"Found {json_data['total']} results")
                books = []
                for book in json_data['stories']:
                    b = Book.from_json(book)
                    books.append(b)
                return books
            except Exception as e:
                is_error = True
                er = e
                
                
        else:
            try:
                return json_data['total']
            except Exception as e:
                is_error = True
                er = e
        
        if is_error:
            self.log.error(f"[{response.status_code}] {response.text}\nError: {er}")
            self.log.info(f"if you can't solve this error, please report it to the developer")
            self.log.info(f"Or submit a bug report at https://github.com/shhossain/wattpad-scraper/issues")
            return []

    def get_user_reading_lists(self,username=None) -> List[ReadingList]:
        request = self.reading_list_req
        return request.get_user_reading_lists(username)

    @access_for_authenticated_user
    def create_reading_list(self, title: str) -> ReadingList:
        request = self.reading_list_req
        return request.create_reading_list(title) #type: ignore
    
    @access_for_authenticated_user
    def create_reading_list_if_not_exists(self, title: str) -> ReadingList:
        request = self.reading_list_req
        return request.create_reading_list_if_not_exists(title) #type: ignore

    def author_book_list(self,author_username: str):
        request = self.reading_list_req
        return request.author_book_list(author_username)

    def get_reading_list(self, id_or_url=None): #type: ignore
        request = self.reading_list_req
        return request.get_reading_list(id_or_url)

    @access_for_authenticated_user
    def delete_reading_list(self, reading_list: Union[str,ReadingList,int]) -> bool:
        request = self.reading_list_req
        if isinstance(reading_list, ReadingList):
            reading_list = reading_list.id #type: ignore 
        elif isinstance(reading_list, int):
            reading_list = str(reading_list)
        return request.delete_reading_list(reading_list)

    @access_for_authenticated_user
    def add_to_reading_list(self, book: Union[str,Book,int],reading_list: Union[str,ReadingList,int],) -> bool:
        request = self.reading_list_req
        if isinstance(reading_list, int):
            reading_list = str(reading_list)
        if isinstance(book, int):
            book = str(book)
        
        return request.add_to_reading_list(book=book, reading_list=reading_list)
    
    @access_for_authenticated_user
    def remove_from_reading_list(self, book: Union[str,Book,int],reading_list: Union[str,ReadingList,int],) -> bool:
        request = self.reading_list_req
        if isinstance(reading_list, int):
            reading_list = str(reading_list)
        if isinstance(book, int):
            book = str(book)
        
        return request.remove_from_reading_list(book=book, reading_list=reading_list)

# if __name__ == "__main__":
#     wattpad = Wattpad()
#     wattpad.search_book('harry potter')
