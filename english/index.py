import os
import sys
import copy
import heapq

import xml.etree.cElementTree as ET

from page import Page
from indexer import Index, PostingList, wordDocIndex

from config import *
from lang import Tokenizer, Stemmer
from utils import isAllNone, getSmallestElement, HeapNode

class ParseWiki:
    def __init__(self, filename):
        self.filename = filename
        self.postings = PostingList(INTERMEDIATE_INDEX_FOLDER)
        self.file_no = 0
        self.stemmer = Stemmer()
        self.tokenizer = Tokenizer()

        if not os.path.exists(sys.argv[2]):
            os.makedirs(sys.argv[2])

        self.titlef = open(os.path.join(sys.argv[2], f"titles_{self.postings.indexCount}.txt"), "w")
        self.totTokens = 0
        
    def parse(self):
        for event, elem in ET.iterparse(self.filename, events=('end',)):
        # for event, elem in etree.iterparse(self.filename, events=('end',)):

            if event != "end":
                continue

            if 'page' not in elem.tag:
                continue

            self.processChildren(list(elem))

            if self.file_no % INDEXSIZE == 0:
                self.titlef.close()
                self.postings.write()                
                self.titlef = open(os.path.join(sys.argv[2], f"titles_{self.postings.indexCount}.txt"), "w")

            elem.clear()
        self.end()

    def processChildren(self, children):

        print(self.file_no, end="\r")

        page = Page()
        page.initPageFromElement(children)
        self.titlef.write(page.title + "\n")

        if "Wikipedia:" in page.title or "Category:" in page.title:
            self.file_no += 1
            return
        
        index = Index(self.file_no, page, self.tokenizer, self.stemmer)
        
        self.postings.add(index)
        self.file_no += 1

    def end(self):

        if len(self.postings):
            self.postings.write()
        self.titlef.close()

        print("Done Parsing! - Intermediate Indexing Over")

    def combine(self):
        
        if os.path.exists(sys.argv[2]):
            files = os.listdir(sys.argv[2])
            for filePath in files:
                if 'title' not in filePath:
                    os.remove(os.path.join(sys.argv[2], filePath))

        self.postings = PostingList(sys.argv[2])

        index_files = os.listdir(INTERMEDIATE_INDEX_FOLDER)
        f_index_files = [open(os.path.join(INTERMEDIATE_INDEX_FOLDER, index_file), "r") for index_file in index_files if index_file[0].isnumeric()]

        word_list = []
        for i in range(len(f_index_files)):
            wordLine = f_index_files[i].readline().strip().strip("\n")
            word, str = wordLine.split(":")
            word_list.append(HeapNode(word, i, wordDocIndex(word, str)))

        heapq.heapify(word_list)
        heap = word_list.copy()
        count = 0

        while len(heap):

            # Write to file if indexsize is maxed out    
            if len(self.postings) % TOKENS_PER_FILE == 0 and len(self.postings) > 0:
                self.totTokens += len(self.postings.invertedIndex.keys())
                self.postings.write()

            newWord = heap[0].word
            word = None

            # Keep popping from heap as long as the word is the same
            while len(heap) and heap[0].word == newWord:
                
                if word is not None:
                    word = word + heap[0].catInfo # Combine postings for this word
                else:
                    word = heap[0].catInfo

                index_file_idx = heap[0].f
                wordLine = f_index_files[index_file_idx].readline().strip().strip("\n")

                heapq.heappop(heap)

                # Only add to heap if the line read is not empty
                if wordLine != "":
                    replaceWord, str = wordLine.split(":")
                    newNode = HeapNode(replaceWord, index_file_idx, wordDocIndex(replaceWord, str))
                    heapq.heappush(heap, newNode)

            self.postings.invertedIndex[word.word] = word.str
            print(count, end="\r")
            count += 1

        print("\n")

        if len(self.postings):
            self.totTokens += len(self.postings.invertedIndex.keys())
            self.postings.write()

        print("Final Inverted Index Made!")

if __name__ == '__main__':

    # print(sys.argv)
    assert len(sys.argv) == 4, "Three arguments required - Path to XML, Inverted Index Folder, Statistic File"

    if not os.path.exists(sys.argv[2]):
        os.makedirs(sys.argv[2], exist_ok=True)

    # curpath = os.path.dirname(os.path.realpath(__file__) )
    # filename = os.path.join(curpath, "../", "enwiki-latest-pages-articles17.xml-p23570393p23716197")
    filename = sys.argv[1]

    target = ParseWiki(filename)
    target.parse()
    target.combine()

    f = open(str(sys.argv[3]), "w")
    f.write(str(len(set(target.stemmer.ignored_words)) + target.totTokens) + "\n")
    f.write(str(target.totTokens) + "\n")
    f.close()

    print("Token Statistics Written")
