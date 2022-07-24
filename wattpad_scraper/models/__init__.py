import json
from typing import Dict, List
from enum import Enum
from ..utils.parse_content import parse_content


class Status(Enum):
    ONGOING = 1
    COMPLETED = 2
    CANCELLED = 3
    HOLD = 4


class Chapter:
    def __init__(self, url, title=None, content=None) -> None:
        self.url = url
        self.title = title
        self._content = content

    # to json
    def to_json(self) -> Dict[str, str]:
        return json.dumps(self.__dict__, indent=4)

    @property
    def content(self) -> List[str]:
        if self._content is None:
            self._content =  parse_content(self.url)
        return self._content


class Author:
    def __init__(self, url: str, name: str, author_img_url: str = None, books=None) -> None:
        self.url = url
        self.author_img_url = author_img_url
        self.name = name
        self.books = books

    def to_json(self) -> str:
        return json.dumps({'url': self.url, 'author_img_url': self.author_img_url, 'name': self.name, 'books': self.books.to_json() if self.books != None else None}, indent=4)


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

    def __init__(self, url: str, title: str, author: Author, img_url: str, total_chapters: int, tags: List[str], description: str, published: str, reads: int = None, votes: int = None, status: Status = Status.ONGOING, isMature: bool = False, chapters: List[Chapter] = None) -> None:
        self.url = url
        self.title = title
        self.author = author
        self.chapters = chapters
        self.img_url = img_url
        self.tags = tags
        self.status = status
        self.isMature = isMature
        self.description = description
        self.published = published
        self.reads = reads
        self.votes = votes
        self.total_chapters = total_chapters

    def to_json(self) -> str:
        # withouth chapters
        return json.dumps({'url': self.url, 'title': self.title, 'author': self.author.to_json(), 'img_url': self.img_url, 'tags': self.tags, 'status': self.status.name, 'isMature': self.isMature, 'description': self.description, 'published': self.published, 'reads': self.reads, 'votes': self.votes, 'total_chapters': self.total_chapters}, indent=4)
