import os
import heapq

import xml.etree.cElementTree as ET
from lxml import etree

from page import Page
from indexer import CategoryInformation, Index, PostingList, wordDocIndex

from config import *
from lang import Tokenizer, Stemmer
from utils import isAllNone, getSmallestElement

curpath = os.path.dirname(os.path.realpath(__file__) )
filename = os.path.join(curpath, "../", "enwiki-latest-pages-articles17.xml-p23570393p23716197")

class ParseWiki:
    def __init__(self, filename):
        self.filename = filename
        self.postings = PostingList(INTERMEDIATE_INDEX_FOLDER)
        self.file_no = 0
        self.stemmer = Stemmer()
        self.tokenizer = Tokenizer()

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
        
        index = Index(self.file_no, page, self.tokenizer, self.stemmer)
        
        self.postings.add(index)
        self.file_no += 1

    def end(self):

        if len(self.postings):
            self.postings.write()

        print("Done Parsing!")

    def combine(self):
        
        self.postings = PostingList(INDEX_FOLDER)

        index_files = os.listdir(INTERMEDIATE_INDEX_FOLDER)
        f_index_files = [open(os.path.join(INTERMEDIATE_INDEX_FOLDER, index_file), "r") for index_file in index_files]

        word_list = []
        for i in range(len(f_index_files)):
            wordLine = f_index_files[i].readline().strip().strip("\n")
            word, str = wordLine.split(":")
            word_list.append(wordDocIndex(word, str))

        while not isAllNone(word_list):

            # Write to file if indexsize is maxed out    
            if len(self.postings) % TOKENS_PER_FILE == 0 and len(self.postings) > 0:
                self.postings.write()

            indicesUsed = []

            ind, word = getSmallestElement(word_list)
            indicesUsed.append(ind)

            # Combine common words
            for i in range(len(word_list)):
                if word_list[i] is None:
                    continue
                
                if i != ind and word_list[i].word == word.word:
                    word = word + word_list[i]
                    indicesUsed.append(i)

            self.postings.invertedIndex[word.word] = word.str

            # Set used words to None
            for i in indicesUsed:
                word_list[i] = None
            
            # Read from files where the words were used up
            for i in range(len(word_list)):
                if word_list[i] is not None:
                    continue

                wordLine = f_index_files[i].readline().strip().strip("\n")

                if wordLine != "":
                    # print(wordLine, i, index_files[i])
                    word, str = wordLine.split(":")
                    word_list[i] = wordDocIndex(word, str)
                else:
                    word_list[i] = None

        if len(self.postings):
            self.postings.write()

target = ParseWiki(filename)
target.parse()
target.combine()