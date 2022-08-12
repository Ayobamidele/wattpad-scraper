from ebooklib import epub
from wattpad_scraper.utils.request import get
from wattpad_scraper.utils.log import Log
import threading
from os import path
import re




def add_image(url: str, file_name: str, ebook: epub.EpubBook, verbose: bool = False) -> None:
    res = get(url)
    img_item = epub.EpubItem(
        uid=file_name, file_name=f"images/{file_name}", media_type='image/jpeg', content=res.content)
    ebook.add_item(img_item)
    return img_item


def create_epub(book, loc: str = None, verbose: bool = True) -> None:
    log = Log(name="wattpad_convert_epub", verbose=verbose)
    log.info("To turn off verbose mode, convert_to_epub(verbose=False)")

    book_id = book.url.split("/")[-1].split("-")[0]
    ebook = epub.EpubBook()
    ebook.set_identifier(book_id)
    ebook.add_author(book.author.name)
    ebook.set_title(book.title)
    ebook.set_language('en')

    log.print(f"Creating epub for {book.title}",color="green")
    # add cover image
    log.print("Adding cover image",color="green")
    res = get(book.img_url)
    ebook.set_cover("cover.jpg", content=res.content)

    # about page
    log.print("Adding about page",color="green")
    about_page = epub.EpubHtml(
        title='About', file_name='about.xhtml', lang='en')
    about_page.content = f"<h1>{book.title}</h1><p>{book.description}</p>"
    ebook.add_item(about_page)

    chapters = []
    log.print("Getting chapters",color="green")
    log.print(f"Chapters: {book.total_chapters}",color="green")
    book_chapters = book.chapters_with_content
    for chapter in book_chapters:
        log.print(
            f"Adding chapter {chapter.number} {chapter.title}({len(chapter)} chars)",color="green")
        chapter_obj = epub.EpubHtml(
            title=chapter.title, file_name=f"{chapter.number}.xhtml", lang='en')
        h1tag = f"<h1>{chapter.number}. {chapter.title}</h1>"
        content = h1tag
        threads = []
        img_no = 1
        for line in chapter.content:
            if ("https://" in line or "http://" in line) and " " not in line:
                log.print(f"Found image in {chapter.title} ({img_no})",color="green")
                file_name = line.split("/")[-2]
                file_name = f"{chapter.number}-{file_name}.jpeg"
                t = threading.Thread(target=add_image, args=(
                    line, file_name, ebook, verbose))
                threads.append(t)
                t.start()
                content += f"<img src='images/{file_name}' alt='{file_name}'/><br/>"
                img_no += 1
            else:
                ptag = f"<p>{line}</p>"
                content += ptag
        for t in threads:
            t.join()
        chapter_obj.content = content
        ebook.add_item(chapter_obj)
        chapters.append(chapter_obj)

    ebook.toc = tuple(chapters)
    ebook.add_item(epub.EpubNcx())
    ebook.add_item(epub.EpubNav())

    style = '''
    @namespace epub "http://www.idpf.org/2007/ops";
    body {
        font-family: Cambria, Liberation Serif, Bitstream Vera Serif, Georgia, Times, Times New Roman, serif;
    }
    h2 {
        text-align: left;
        text-transform: uppercase;
        font-weight: 200;     
    }
    ol {
            list-style-type: none;
    }
    ol > li:first-child {
            margin-top: 0.3em;
    }
    nav[epub|type~='toc'] > ol > li > ol  {
        list-style-type:square;
    }
    nav[epub|type~='toc'] > ol > li > ol > li {
            margin-top: 0.3em;
    }'''

    # add css file
    nav_css = epub.EpubItem(
        uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    ebook.add_item(nav_css)

    # create spin, add cover page as first page
    ebook.spine = ['cover', about_page, 'nav'] + [item for item in chapters]

    file_name_pat = re.compile(r'[^a-zA-Z0-9_-]')
    file_name = file_name_pat.sub('', book.title.lower().replace(" ", "_"))
    if loc is None:
        log.print("Saving epub in current directory",color="green")
        epub.write_epub(file_name + ".epub", ebook, {})
    else:
        log.print(f"Saving epub in {loc}",color="green")
        if not path.exists(loc):
            log.print(
                f"Path {loc} does not exist, saving in current directory",color="green")
            epub.write_epub(file_name + ".epub", ebook, {})
        else:
            if path.isdir(loc):
                loc = path.join(loc, file_name + ".epub")
        epub.write_epub(loc, ebook, {})
    log.success("Epub created")
