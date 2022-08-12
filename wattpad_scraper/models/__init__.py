import json
from typing import Dict, List
from enum import Enum
from wattpad_scraper.utils.parse_content import parse_content
from wattpad_scraper.utils.request import get
from wattpad_scraper.utils.log import Log
from wattpad_scraper.utils.convert_to_epub import create_epub
from datetime import datetime
from bs4 import BeautifulSoup
import threading

class Status(Enum):
    ONGOING = 1
    COMPLETED = 2
    CANCELLED = 3
    HOLD = 4




class Chapter:
    def __init__(self, url:str, title:str=None, content=None,chapter_number:int=0) -> None:
        self.url = url
        self.title = title
        self._content = content
        self.number = chapter_number
        

    # to json
    def to_json(self) -> Dict[str, str]:
        return json.dumps(self.__dict__, indent=4)

    @property
    def content(self) -> List[str]:
        """
        Returns the content of the chapter. Will be parsed if not already parsed.
        """
        if self._content is None:
            self._content =  parse_content(self.url)
        return self._content
    
    def parse_content_again(self) -> List[str]:
        """
        Parses the content of the chapter again.
        """
        self._content = parse_content(self.url)
        return self._content
    

    def __str__(self) -> str:
        return f"Chapter(url={self.url}, title={self.title})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        return self.url == other.url
    
    def __dir__(self) -> List[str]:
        return ['url', 'title', 'content', 'number', 'parse_content_again', 'to_json']
    
    def __len__(self) -> int:
        total_len = 0
        for content in self.content:
            total_len += len(content)
        return total_len
    
    def __hash__(self) -> str:
        return hash(self.url)
    
    def __lt__(self, other) -> bool:
        return self.number < other.number
    
    def __le__(self, other) -> bool:
        return self.number <= other.number
    
    def __gt__(self, other) -> bool:
        return self.number > other.number
    
    def __ge__(self, other) -> bool:
        return self.number >= other.number
        
    def __ne__(self, other) -> bool:
        return self.url != other.url

class Author:
    def __init__(self, url: str, name: str, author_img_url: str = None, books=None) -> None:
        self.url = url
        self.author_img_url = author_img_url
        self.name = name
        self.books = books if books is not None else []

    def to_json(self) -> str:
        return json.dumps({'url': self.url, 'author_img_url': self.author_img_url, 'name': self.name, 'books': self.books if self.books != None else None}, indent=4)

    def __str__(self) -> str:
        return f'Author(name={self.name}, url={self.url})'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Author):
            return self.url == __o.url
        return False
    
    def __len__(self) -> int:
        return len(self.books)

def get_chapters(url: str) -> List[Chapter]:
    """
    Args:
        url (string): book url

    Returns:
        List[Chapter]: returns a list of Chapter objects

        Chapter object has the following attributes:
            url (string): chapter url
            title (string): chapter title
            content (list): list of chapter content
    """
    response = get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    main_url = "https://www.wattpad.com"

    toc = soup.find(class_='table-of-contents')
    lis = toc.find_all('li')
    chapters = []
    for n,li in enumerate(lis):
        a = li.find('a')
        url = a.get('href')
        if url.startswith('/'):
            url = main_url + url
        ch = Chapter(
            url=url, title=a.get_text().strip().replace('\n', ' '), chapter_number=n)
        chapters.append(ch)
        n += 1
    return chapters

class Book:
    """
    Book class
        Attributes:
            url: str
            title: str
            author: Author object
            img_url: str
            tags: list of str
            status: Status (ONGOING, COMPLETED, CANCELLED, HOLD)
            isMature: bool
            description: str
            published: str
            reads: int
            votes: int
            total_chapters: int
            chapters: list of Chapter objects

    """

    def __init__(self, url: str, title: str,  img_url: str, total_chapters: int,description: str, author: Author=None, tags: List[str]=None,  published: str=None, reads: int = None, votes: int = None, status: Status = Status.ONGOING, isMature: bool = False, chapters: List[Chapter] = None) -> None:
        self.url = url
        self.title = title
        self.author = author
        self._chapters = chapters
        self.img_url = img_url
        self.tags = tags
        self.status = status
        self.isMature = isMature
        self.description = description
        self.published = published
        self.reads = reads
        self.votes = votes
        self.total_chapters = total_chapters
        self._chapters_with_content:List[Chapter] = []
        self.log = Log("wattpad_log")

        

    @property
    def chapters(self) -> List[Chapter]:
        if self._chapters is None:
            self._chapters =  get_chapters(self.url)
        return self._chapters

    @property
    def chapters_with_content(self) -> List[Chapter]:
        threads = []
        for chapter in self.chapters:
            self.log.print(f"Getting content for chapter {chapter.number}",color="blue")
            t = threading.Thread(target=lambda: chapter.content)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return self.chapters

    def genarate_chapters(self) :
        for chapter in self.chapters:
            chapter.content
            yield chapter
        

    def convert_to_epub(self,loc:str=None,verbose:bool=True) -> None:
        """
        Converts the book to epub format
        
        Args:
            loc (string): location to save the epub file default is current directory
            verbose (bool): if true prints the progress of the conversion default is true
        """
        create_epub(self,loc,verbose)

    def to_json(self) -> str:
        # withouth chapters
        return json.dumps({'url': self.url, 'title': self.title, 'author': self.author.to_json(), 'img_url': self.img_url, 'tags': self.tags, 'status': self.status.name, 'isMature': self.isMature, 'description': self.description, 'published': self.published, 'reads': self.reads, 'votes': self.votes, 'total_chapters': self.total_chapters}, indent=4)
    
    def __str__(self) -> str:
        return f"Book(title={self.title}, url={self.url}, status={self.status.name}, total_chapters={self.total_chapters})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        return self.url == other.url
    
    # len
    def __len__(self) -> int:
        return self.total_chapters
    
    def __dir__(self) -> List[str]:
        return ['url', 'title', 'author', 'img_url', 'tags', 'status', 'isMature', 'description', 'published', 'reads', 'votes', 'total_chapters','chapters','to_json']


    # from json
    @classmethod
    def from_json(cls, json_str: str) -> 'Book':
        json_str = json.loads(json_str) if isinstance(json_str,str) else json_str
        title = json_str['title']
        url = json_str['url']
        img_url = json_str['cover']
        description = json_str['description']
        author_name = json_str['user']['name']
        author_url = f"https://www.wattpad.com/user/{author_name}"
        author = Author(name=author_name, url=author_url)
        tags = json_str['tags']
        status = Status.COMPLETED if json_str['completed'] else Status.ONGOING
        isMature = json_str['mature']
        published = json_str['lastPublishedPart']['createDate']
        published = datetime.strptime(published, '%Y-%m-%d %H:%M:%S')
        published = published.strftime('%d/%m/%Y')
        reads = json_str['readCount']
        votes = json_str['voteCount']
        total_chapters = json_str['numParts']
        return cls(url=url, title=title, img_url=img_url, description=description, author=author, tags=tags, status=status, isMature=isMature, published=published, reads=reads, votes=votes, total_chapters=total_chapters)

#     {
    #   "id": "80033537",
    #   "title": "ROMEO [2] ⚡ harry potter ",
    #   "description": "❝ 𝐇𝐄 𝐖𝐀𝐒 𝐒𝐋𝐄𝐄𝐏 𝐀𝐍𝐃 𝐒𝐇𝐄 𝐖𝐀𝐒 𝐖𝐀𝐊𝐄𝐅𝐔𝐋𝐍𝐄𝐒𝐒. 𝐓𝐇𝐄 𝐆𝐈𝐑𝐋 𝐖𝐈𝐓𝐇 𝐀 𝐒𝐎𝐔𝐋 𝐖𝐇𝐄𝐑𝐄 𝐑𝐎𝐒𝐄𝐒 𝐆𝐑𝐄𝐖, 𝐓𝐇𝐄 𝐁𝐎𝐘 𝐖𝐈𝐓𝐇 𝐀 𝐒𝐎𝐔𝐋 𝐃𝐄𝐒𝐓𝐈𝐍𝐄𝐃 𝐅𝐎𝐑 𝐂𝐀𝐋𝐀𝐌𝐈𝐓𝐘. \n\n𝐖 𝐇 𝐀 𝐓  𝐀  𝐏 𝐀 𝐈 𝐑  𝐓 𝐇 𝐄 𝐘  𝐖 𝐄 𝐑 𝐄. ❞\n\n[spin off to Caecus, a Harry Potter fanfiction- read once you reach PART III in caecus] [4/8/16 to 26/07/18]\n\n© Aug 2016- wattpad.com/sweetwines",
    #   "user": {
    #     "name": "sweetwines"
    #   },
    #   "completed": true,
    #   "numParts": 42,
    #   "lastPublishedPart": {
    #     "createDate": "2020-12-20 13:13:29"
    #   },
    #   "voteCount": 3387,
    #   "readCount": 114760,
    #   "commentCount": 2677,
    #   "cover": "https://img.wattpad.com/cover/80033537-256-k109399.jpg",
    #   "mature": false,
    #   "url": "https://www.wattpad.com/story/80033537-romeo-2-%E2%9A%A1-harry-potter",
    #   "tags": [
    #     "goldenera",
    #     "harrypotter",
    #     "hogwarts",
    #     "hpau",
    #     "hpromance",
    #     "wattys2018"
    #   ],
    #   "isPaywalled": false,
    #   "length": 354012,
    #   "language": {
    #     "id": 1
    #   }
    # },