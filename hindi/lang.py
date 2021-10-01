import re
import Stemmer as pyStemmer
from nltk.corpus import stopwords

class Tokenizer:
    def __init__(self, characters="alphanumeric"):

        if characters == "alphanumeric":
            self.regexpression = r"[^\u0900-\u0963\u0963-\u097f9-0\ ]+"

    def __call__(self, *args, **kwds):
        data = args[0]
        
        # data = re.sub(r"[^A-Za-z0-9\ ]+", "", data)
        # tokens = data.split()

#        print(data)
        tokens = re.split(r"[^a-zA-Z\u0900-\u0963\u0963-\u097f0-9#]+", data)
#        print(tokens)
        return tokens

class Stemmer:
    def __init__(self, noStop=False):
        self.stemmer = pyStemmer.Stemmer('hindi')
        self.stemmer.maxCacheSize = 1000000
        self.stopwords = set(open("hindiStopWords.txt", "r").read().splitlines())
        self.ignored_words = []
        self.noStop = noStop
        
    def __call__(self, *args, **kwds):

        new_words = []

        for word in args[0]:
            word = word.casefold().strip().strip("0")
            
            if self.noStop:
                new_words.append(self.stemmer.stemWord(word))
                continue

            if len(word) < 2 or len(word) > 15 or (word.isnumeric() and len(word) > 4):
                # self.ignored_words.append(word)
                continue

            if  '#' in word:
                continue

            if word in self.stopwords:
                # self.ignored_words.append(word)
                continue

            new_words.append(self.stemmer.stemWord(word))
        
        return new_words

if __name__ == '__main__':
    stemmer = Stemmer()
    words = stemmer.stopwords

    for word in words:
        match = re.findall(r"[\u0900-\u0963\u0963-\u097f]", word)
        print(word, match)