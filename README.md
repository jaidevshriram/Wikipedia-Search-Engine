# Wikipedia Search Engine

This is an efficient search engine for Wikipedia corpus pages with support for English and Hindi queries.

## How to Run

### Index the Data

The first part is indexing the Wikipedia data, stored as a XML file, to make search easier
and quicker.

```
bash index.sh  <path_to_wiki_dump> <path_to_inverted_index> statistics_file.txt
```

This will parse the data and store the final inverted index in a new location. Note that it will also create an intermediate representation at `intermediate/`.

### Searching Through Data

With this, we can search through the data:

```
bash search.sh <path_to_inverted_index> <path_to_file_with_queries>
```

## Important Files

- `index.py` is the script that indexes a given data dump. It iterates through each article in the XML, creates a page instance (defined in page.py), then indexes this (logic in indexer.py), and finally inverts this and writes to a file after several files. 

- `config.py` has some settings/options that the project uses, such as number of files per intermediate index.

- `lang.py` has definitions for the stemmer and tokenizer used throughout this project

- `search.py` implements the search functionality. It reads a query file and creates a posting list and then calculates the tf-idf scores per document. It returns the titles for the top documents.
