from hashlib import new
import os
import sys
import json
import random

import linecache

from multiprocessing import Pool

from lang import Stemmer, Tokenizer
from config import *
from indexer import CategoryInformation, PostingList, strToPost

def binary_search(arr, l, r, x):
    if l > r:
        return -1
    else:
        if (arr[r] <= x):
            return r

        mid = (l+r)//2

        if arr[mid] < x:
            if (mid+1) < len(arr) and arr[mid+1] > x:
                return mid
            else:
                return binary_search(arr, mid+1, r, x)
        elif arr[mid] > x:
            return binary_search(arr, l, mid-1, x)
        else:
            return mid

class TitleCache:
    def __init__(self, title_path, titles_per_file):
        self.title_path = title_path
        self.titles_per_file = titles_per_file
    
    def getFileNo(self, docId):
        titleFile = docId //  self.titles_per_file
        titleFileLine = docId % self.titles_per_file + 1
        return titleFile, titleFileLine

    def __call__(self, docId):
        titleFile, titleFileLine = self.getFileNo(docId)
        title = linecache.getline(os.path.join(self.title_path, f"titles_{titleFile}.txt"), titleFileLine)

        return title.strip().strip('\n').lower()

class Query:

    def __init__(self):
        self.words = []
        self.wordstr = None
        self.pool = None
        self.titleCache = None

    @classmethod
    def fromString(cls, str, stemmer, tokenizer, titleCache, pool):
        self = cls()

        self.words = []
        self.titleCache = titleCache
        self.pool = pool

        splitstr = str.strip().strip("\n").split(":")

        self.wordstr = {}

        if len(splitstr) == 1:
            self.type = "regular"
            words = stemmer(tokenizer(splitstr[0]))
            for word in words:
                if word in self.wordstr.keys():
                    self.wordstr[word].add("a")
                else:
                    self.wordstr[word] = set(["a"])
        else:
            self.type = "field"
            for i in range(1, len(splitstr)):
                field = splitstr[i-1][-1]
                word = splitstr[i][:-2] if i < (len(splitstr) - 1) else splitstr[i]

                all_words = stemmer(tokenizer(word))
                for word in all_words:
                    if word in self.wordstr.keys():
                        self.wordstr[word].add(field)
                    else:
                        self.wordstr[word] = set([field])
                    
        return self

    def findWordFromFile(self, wordQuery, fields, idx):

        out = {}

        if idx == -1:
            catInfo = PostingList.strToCategoryInfoList("")
            wordResult = PostingList.categoryInfoListToDict(catInfo)
            out = wordResult
            return out

        f = open(os.path.join(sys.argv[1], f"{idx}.txt"), "r")
        while True:
            line = f.readline().strip().strip("\n")
            if line == "":
                break
            word, str = line.split(":")
            
            if word == wordQuery:
                catInfo = PostingList.strToCategoryInfoList(str, self.pool, fields)
                return catInfo

        catInfo = PostingList.strToCategoryInfoList("")
        # wordResult = PostingList.categoryInfoListToDict(catInfo)
        # out = wordResult
        return catInfo    

    def process(self, startWords):

        output = {}
        
        for k, v in self.wordstr.items():
            if k == "":
                continue
            indexFileNo = binary_search(startWords, 0, len(startWords)-1, k)
            docInfo = self.findWordFromFile(k, list(v), indexFileNo)

            for docId, docScore in docInfo:
                if docId in output.keys():
                    output[docId] += docScore
                else:
                    output[docId]  = docScore

        docIds = sorted(output.keys(), key=lambda x: output[x])[::-1]

        while len(docIds) < 10:
            newDocId = random.randint(1, TOT_ARTICLES)
            if newDocId not in docIds:
                docIds.append(newDocId)

        return docIds[:10]

if __name__ == "__main__":

    stemmer = Stemmer(noStop=True)
    tokenizer = Tokenizer()
    titleCache = TitleCache(sys.argv[1], INDEXSIZE)
    pool = Pool(NUM_WORKERS)

    startWords = []
    tf = open(os.path.join(sys.argv[1], "startWordFile.txt"), "r")
    startWords = tf.read().splitlines()

    qf = open("queries.txt", "r")
    out = open("queries_op.txt", "w")
    for query in qf.readlines():
        query = query.strip("\n").strip()
        query = Query.fromString(query, stemmer, tokenizer, titleCache, pool)
        result = query.process(startWords)
        print(len(result))
        docTitles = list(map(titleCache, result))
        print(docTitles)
        print('----')
        # print(json.dumps(result, indent=4))

    qf.close()
    out.close()