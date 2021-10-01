import os
import glob
from tqdm import tqdm

from itertools import repeat

from multiprocessing import Pool

from utils import encode32, decode32
from indexer import strToPost, CategoryInformation

src_path = 'index/'
dst_path = 'index-final/'
os.makedirs(dst_path, exist_ok=True)
THRESHOLD = 200000

makestr = str

# Get All Index Files

def getIndexFiles():
    all_index_files = os.listdir(src_path)
    index_files = []
    for idx in all_index_files:
        if len(idx.split('_')) > 1 or not idx[0].isnumeric():
            continue
        else:
            index_files.append(idx)
    return index_files

def processIndexFile(index_file_p):
    fr = open(os.path.join(src_path, index_file_p), "r")
    fw = open(os.path.join(dst_path, index_file_p), "w")

    for line in fr.readlines():
        line = line.strip().strip("\n")

        # Process the string
        if line == "":
            break

        try:
            word, str = line.split(":")
        except:
            print("Failed:", line)
            continue
            
        splitstr = str.split('d')[1:]
        # print(list(zip(repeat(CategoryInformation), 
        #     splitstr, 
        #     repeat(True), 
        #     repeat(['a']), 
        #     repeat(len(splitstr)))))
        docIDScoreMap = list(map(strToPost, 
            repeat(CategoryInformation), 
            splitstr, 
            repeat(True), 
            repeat(['a']), 
            repeat(len(splitstr)),
            repeat(True)))
        
        # Sort by TFIDF weights
        sortedDocID = sorted(docIDScoreMap, key=lambda x: x[1], reverse=True)

        # Take the threshold
        filteredDocs = sortedDocID[:THRESHOLD]

        # Write back the string to fw
        newstr = ""
        for doc in filteredDocs:
            doc = doc[2]
            # print(doc.docId, doc)
            # print(type(doc.docId))
            # print(encode32(doc.docId))
            newstr += f"d{encode32(doc.docId)}" + makestr(doc)
        
        out = f"{word}:" + newstr

        fw.write(out + "\n")

    print(index_file_p, "Done!")

    fr.close()
    fw.close()

if __name__ == '__main__':
    pool = Pool(12)

    index_files = getIndexFiles()
    print(index_files)
    pool.map(processIndexFile, index_files)
    pool.close()
    pool.join()

    print("NOW COPY TITLES")