import os
import sys
import json

from lang import Stemmer, Tokenizer
from config import *
from indexer import CategoryInformation, PostingList

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

class Query:

    def __init__(self):
        self.words = []
        self.wordstr = None

    @classmethod
    def fromString(cls, str, stemmer, tokenizer):
        self = cls()

        self.words = []

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

    def findWordFromFile(self, wordQuery, idx):

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
                catInfo = PostingList.strToCategoryInfoList(str)
                wordResult = PostingList.categoryInfoListToDict(catInfo)
                return wordResult

        catInfo = PostingList.strToCategoryInfoList("")
        wordResult = PostingList.categoryInfoListToDict(catInfo)
        out = wordResult
        return out    

    def process(self, startWords):

        output = {}
        
        for k in self.wordstr.keys():
            if k == "":
                continue
            indexFileNo = binary_search(startWords, 0, len(startWords)-1, k)
            output[k] = self.findWordFromFile(k, indexFileNo)

        return output

if __name__ == "__main__":

    # qf = open("queries.txt", "r")
    stemmer = Stemmer(noStop=True)
    tokenizer = Tokenizer()

    startWords = []
    tf = open(os.path.join(sys.argv[1], "startWordFile.txt"), "r")
    startWords = tf.read().splitlines()

    query = Query.fromString(' '.join(sys.argv[2:]), stemmer, tokenizer)
    result = query.process(startWords)
    print(json.dumps(result, indent=4))