`index.py` is the script that indexes a given data dump. It iterates through each article in the XML, creates a page instance (defined in page.py), then indexes this (logic in indexer.py), and finally inverts this and writes to a file after several files. 

`config.py` has some settings/options that the project uses, such as number of files per intermediate index.

`lang.py` has definitions for the stemmer and tokenizer used throughout this project

`search.py` implements the search functionality. It reads a query file and creates a posting list and then calculates the tf-idf scores per document. It returns the titles for the top documents.