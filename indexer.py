import os
from lang import Tokenizer, Stemmer

class CategoryInformation:
    def __init__(self):
        self.title = 0
        self.infobox = 0
        self.body = 0
        self.categories = 0
        self.links = 0
        self.references = 0

    def __add__(self, new):
        self.title += new.title
        self.infobox += new.infobox
        self.body += new.body
        self.categories += new.categories
        self.links += new.links
        self.references += new.references

    def __str__(self):
        return f"t{self.title}i{self.infobox}b{self.body}c{self.categories}l{self.links}r{self.references}"

class Index:
    def __init__(self, fileno, page):
        self.tokenizer = Tokenizer()
        self.stemmer = Stemmer()
        self.index = {}
        self.fileno = fileno

        page.body = self.stemmer(self.tokenizer(page.body))
        page.categories = self.stemmer(self.tokenizer(' '.join(page.categories)))
        page.infobox = self.stemmer(self.tokenizer(page.infobox))
        page.references = self.stemmer(self.tokenizer(' '.join(page.references)))
        page.links = self.stemmer(self.tokenizer(' '.join(page.links)))

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

class PostingList:
    def __init__(self, intermediateIndexPath="intermediate/"):
        self.invertedIndex = {}
        self.indexCount = 0
        self.intermediateIndexPath = "intermediate/"

    def add(self, index):

        for key in index.index.keys():
            if key not in self.invertedIndex.keys():
                self.invertedIndex[key] = ""
            self.invertedIndex[key] += f"d{index.fileno}" + str(index.index[key])

    def write(self):

        if not os.path.exists(self.intermediateIndexPath):
            os.makedirs(self.intermediateIndexPath)
        
        file = os.path.join(self.intermediateIndexPath, f"{self.indexCount}.txt")
        f = open(file, "w")

        tokens = sorted(self.invertedIndex.keys())
        for token in tokens:
            f.write(f"{token}{self.invertedIndex[token]}\n")
        f.close()

        self.indexCount += 1
        self.invertedIndex = {} 
