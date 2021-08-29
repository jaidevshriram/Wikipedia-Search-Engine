import os
from xml.etree import cElementTree  # C implementation of xml.etree.ElementTree
from xml.parsers.expat import ExpatError  # XML formatting errors

import xml.etree.ElementTree as ET

#-------- Select the XML file: --------#
#Current file name and directory:
curpath = os.path.dirname(os.path.realpath(__file__) )
filename = os.path.join(curpath, "../", "enwiki-latest-pages-articles17.xml-p23570393p23716197")
#print "Filename: %s" % (filename)

#-------- Parse the XML file: --------#
try:
    #Parse the given XML file:
    tree = cElementTree.parse(filename)
except ExpatError as e:
    print("[XML] Error (line %d): %d" % (e.lineno, e.code))
    print("[XML] Offset: %d" % (e.offset))
    raise e
except IOError as e:
    print("[XML] I/O Error %d: %s" % (e.errno, e.strerror))
    raise e
else:
    root = tree.getroot()

    i = 0
    for child in root:
        i += 1
        tag = child.tag.split('}')[-1]
        print(tag)

        if i> 25:
            break   
        # exit()

    # print(catalogue)