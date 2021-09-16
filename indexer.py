import os
import math

from itertools import repeat

from config import TOT_ARTICLES
from utils import encode32, decode32, removeDocInfo

def strToPost(cls, str, score=False, fields=[], totDocs=10):
    str += "x"

    if score:
        str = "d" + str

    self = cls()

    number = ""
    field = ""

    docId, str = removeDocInfo(str)
    self.docId = decode32(docId)

    for char in str:
        # print(char, "-")
        if char.isdigit():
            number += char
            continue

        if char.isalpha():
            if field == "":
                field = char
                continue

            if char != field:
                if field == 'd':
                    self.docId = decode32(number)
                elif field == 't':
                    self.title = int(number)
                elif field == 'i':
                    self.infobox = int(number)
                elif field == 'b':
                    self.body = int(number)
                elif field == 'c':
                    self.categories = int(number)
                elif field == 'l':
                    self.links = int(number)
                elif field == 'r':
                    self.references = int(number)

                field = char
                number = ""

    if score:
        tf = 0
        tf += 1000 * self.title
        tf += 10 * self.infobox
        tf += 20 * self.body
        tf += 10 * self.categories
        tf += 0.1 * self.links
        tf += 0.01 * self.references

        for field in fields:
            if field == 'a':
                continue

            if field == 't':
                tf += 10000 * self.title
            elif field == 'i':
                tf += 10000 * self.infobox
            elif field == 'b':
                tf += 10000 * self.body
            elif field == 'c':
                tf += 10000 * self.categories
            elif field == 'l':
                tf += 10000 * self.links
            elif field == 'r':
                tf += 10000 * self.references

        idf = TOT_ARTICLES / totDocs
        score = math.log(tf) + math.log(idf)

        return self.docId, score

    # print("doc", self.docId)
    # print("title", self.title)
    return self


class CategoryInformation:
    def __init__(self):
        self.docId = None
        self.title = 0
        self.infobox = 0
        self.body = 0
        self.categories = 0
        self.links = 0
        self.references = 0

    @classmethod
    def fromstr(cls, str):
        return strToPost(cls, str)

    def __add__(self, new):
        self.title += new.title
        self.infobox += new.infobox
        self.body += new.body
        self.categories += new.categories
        self.links += new.links
        self.references += new.references

    def __str__(self):
        out = ""
        if self.title:
            out += f"t{self.title}"
        if self.infobox:
            out += f"i{self.infobox}"
        if self.body:
            out += f"b{self.body}"
        if self.categories:
            out += f"c{self.categories}"
        if self.links:
            out += f"l{self.links}"
        if self.references:
            out += f"r{self.references}"

        # return f"t{self.title}i{self.infobox}b{self.body}c{self.categories}l{self.links}r{self.references}"

        return out

    def __getitem__(self, name: str):
        if name == "title":
            return self.title
        if name == "infobox":
            return self.infobox
        if name == "categories":
            return self.categories
        if name == "references":
            return self.references
        if name == "links":
            return self.links
        if name == "body":
            return self.body
        if name == "doc":
            return self.docId

class Index:
    def __init__(self, fileno, page, tokenizer, stemmer):
        self.tokenizer = tokenizer
        self.stemmer = stemmer
        self.index = {}
        self.fileno = fileno

        # self.allTokenCount += len(page.body.split(" ")) + len(' '.join(page.categories).split(" ")) + len(' '.join(page.references).split(" ")) + \
            # len(page.infobox.split(" ")) + len(' '.join(page.links).split(" ")) + len(page.title.split(" "))

        page.body = self.stemmer(self.tokenizer(page.body))
        page.categories = self.stemmer(self.tokenizer(' '.join(page.categories)))
        page.infobox = self.stemmer(self.tokenizer(page.infobox))
        page.references = self.stemmer(self.tokenizer(' '.join(page.references)))
        page.links = self.stemmer(self.tokenizer(' '.join(page.links)))
        page.title = self.stemmer(self.tokenizer(page.title))

        for token in page.body:
            if token not in self.index.keys():
                self.index[token] = CategoryInformation()
            self.index[token].body += 1

        for token in page.categories:
            if token not in self.index.keys():
                self.index[token] = CategoryInformation()
            self.index[token].categories += 1

        for token in page.infobox:
            if token not in self.index.keys():
                self.index[token] = CategoryInformation()
            self.index[token].infobox += 1

        for token in page.references:
            if token not in self.index.keys():
                self.index[token] = CategoryInformation()
            self.index[token].references += 1

        for token in page.links:
            if token not in self.index.keys():
                self.index[token] = CategoryInformation()
            self.index[token].links += 1

        for token in page.title:
            if token not in self.index.keys():
                self.index[token] = CategoryInformation()
            self.index[token].title += 1

        # print(self.index['vagabond'])

class PostingList:
    def __init__(self, intermediateIndexPath="intermediate/"):
        self.invertedIndex = {}
        self.indexCount = 0
        self.intermediateIndexPath = intermediateIndexPath
        self.startWordFile = "startWordFile.txt"

    def add(self, index):

        for key in index.index.keys():
            if key not in self.invertedIndex.keys():
                self.invertedIndex[key] = ""
            self.invertedIndex[key] += f"d{encode32(index.fileno)}" + str(index.index[key])

    def write(self):

        if not os.path.exists(self.intermediateIndexPath):
            os.makedirs(self.intermediateIndexPath)
        
        file = os.path.join(self.intermediateIndexPath, f"{self.indexCount}.txt")
        # print(f"Opening file {file}")
        f = open(file, "w")

        tokens = sorted(self.invertedIndex.keys())
        for token in tokens:
            f.write(f"{token}:{self.invertedIndex[token]}\n")
        f.close()

        self.indexCount += 1
        self.invertedIndex = {} 

        startWorldFilePath = os.path.join(self.intermediateIndexPath, self.startWordFile)
        f = open(startWorldFilePath, "a")
        f.write(tokens[0]+"\n")
        f.close()

    @classmethod
    def strToCategoryInfoList(cls, str, pool=None, fields=['a']):

        if pool is None:
            splitstr = str.split('d')
            results = []
            for str in splitstr[1:]:
                results.append(CategoryInformation.fromstr("d" + str))
            return results
        else:
            splitstr = str.split('d')[1:]
            docInfo = pool.starmap(strToPost, zip(repeat(CategoryInformation), splitstr, repeat(True), repeat(fields), repeat(len(splitstr))))
            return docInfo

    @classmethod
    def categoryInfoListToDict(cls, catList):
        out = {
            "title": [],
            "body": [],
            "infobox": [],
            "categories": [],
            "references": [],
            "links": [],
        }

        for catInfo in catList:
            for field in out.keys():
                if catInfo[field] > 0:
                    out[field].append(catInfo["doc"])

        return out

    def __len__(self):
        return len(self.invertedIndex.keys())

class wordDocIndex:
    def __init__(self, word, str):
        self.str = str
        self.word = word

    def __add__(self, wDocInd):
        self.str += wDocInd.str
        return self

    def __lt__(self, new):
        if self.word == new.word:
            return False
        else:
            return self.word < new.word

    def getJSON(self):  

        word_results = {}

        docs = self.str.split("d")
        for i in range(len(docs)):

            docInfo = CategoryInformation(f"d{docs[i]}")
            word_results[docInfo.docId] = docInfo
