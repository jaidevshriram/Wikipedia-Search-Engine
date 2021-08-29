import re
import nltk
from nltk.corpus import stopwords

class Tokenizer:
    def __init__(self, characters="alphanumeric"):

        if characters == "alphanumeric":
            self.regexpression = r"[^A-Za-z9-0\ ]+"

    def __call__(self, *args, **kwds):
        data = args[0]
        
        # data = re.sub(r"[^A-Za-z0-9\ ]+", "", data)
        # tokens = data.split()

        tokens = re.split(r"[^A-Za-z0-9]+", data)
        return tokens

class Stemmer:
    def __init__(self):
        self.stemmer = nltk.stem.SnowballStemmer('english')
        self.stopwords = set(stopwords.words('english'))

    def __call__(self, *args, **kwds):

        new_words = []

        for word in args[0]:
            word = word.casefold()
            
            if word in self.stopwords:
                continue

            new_words.append(self.stemmer.stem(word))
        
        return new_words