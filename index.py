import os

import xml.etree.cElementTree as ET
from lxml import etree

from page import Page
from indexer import Index, PostingList

from config import *

curpath = os.path.dirname(os.path.realpath(__file__) )
filename = os.path.join(curpath, "../", "enwiki-latest-pages-articles17.xml-p23570393p23716197")

class ParseWiki:
    def __init__(self, filename):
        self.filename = filename
        self.postings = PostingList()
        self.file_no = 0

    def end(self, tag):
        if tag == "page":
            self.pageno += 1
        
    def parse(self):
        for event, elem in ET.iterparse(self.filename, events=('end',)):
        # for event, elem in etree.iterparse(self.filename, events=('end',)):

            if event != "end":
                continue

            if 'page' not in elem.tag:
                continue

            children = list(elem)
            self.processChildren(list(elem))

            if self.file_no % INDEXSIZE == 0:
                self.postings.write()

            elem.clear()
        self.end()

    def processChildren(self, children):

        print(self.file_no, end="\r")

        page = Page()
        page.initPageFromElement(children)
        
        index = Index(self.file_no, page)
        
        self.postings.add(index)
        self.file_no += 1

    def end(self):
        print("Done Parsing!")

target = ParseWiki(filename)
target.parse()
