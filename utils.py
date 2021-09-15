def isAllNone(list):
    for elem in list:
        if elem is not None:
            return False
    return True

def getSmallestElement(list):
    for i, elem in enumerate(list):
        if elem is not None:
            smallest = list[i]
            smallInd = i
            break
    
    for i, elem in enumerate(list):
        if elem is None:
            continue

        if elem < smallest:
            smallest = elem
            smallInd = i

    return smallInd, smallest

class HeapNode:
    def __init__(self, word, f, catInfo):
        self.word = word
        self.f = f
        self.catInfo = catInfo

    def __lt__(self, new_node):
        if self.word == new_node.word:
            return self.f < new_node.f
        else:
            return self.word < new_node.word