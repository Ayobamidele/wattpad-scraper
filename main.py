# from wattpad_scraper import Wattpad


# wattpad = Wattpad()
# books = wattpad.search_book("harry potter",limit=10)
# print(books[0].chapters[0].content) # on search book chapters have to load first so it may take a while
# print(len(books))



# import re
# pyfile = open("setup.py","r").read()
# pattern = r"version='(.*?)'"
# version = re.search(pattern, pyfile).group(1)
# replaceVersion = "v0.0.5"
# newpyfile = pyfile.replace(version,replaceVersion.replace("v",""))
# open("setup.py","w").write(newpyfile)


# oneline
import re;pyfile=open('setup.py','r').read();pattern=r'''version=\'(.*?)\'''';version=re.search(pattern,pyfile).group(1);replaceVersion='v0.0.5';newpyfile=pyfile.replace(version,replaceVersion.replace('v',''));open('setup.py','w').write(newpyfile)

