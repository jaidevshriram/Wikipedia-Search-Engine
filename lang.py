import re
import nltk
import Stemmer as pyStemmer
from nltk.corpus import stopwords

class Tokenizer:
    def __init__(self, characters="alphanumeric"):

        if characters == "alphanumeric":
            self.regexpression = r"[^A-Za-z9-0\ ]+"

    def __call__(self, *args, **kwds):
        data = args[0]
        
        # data = re.sub(r"[^A-Za-z0-9\ ]+", "", data)
        # tokens = data.split()

        tokens = re.split(r"[^A-Za-z0-9#]+", data)
        return tokens

class Stemmer:
    def __init__(self, noStop=False):
        self.stemmer = pyStemmer.Stemmer('english')
        self.stemmer.maxCacheSize = 500000
        self.stopwords = set(stopwords.words('english'))
        self.noStop = noStop
        
    def __call__(self, *args, **kwds):

        new_words = []

        for word in args[0]:
            word = word.casefold().strip().strip("0")
            
            if self.noStop:
                new_words.append(self.stemmer.stemWord(word))
                continue

            if word in self.stopwords or len(word) < 2 or len(word) > 15 or (word.isnumeric() and len(word) > 5):
                continue

            if word[0] == '#':
                continue

            new_words.append(self.stemmer.stemWord(word))
        
        return new_words