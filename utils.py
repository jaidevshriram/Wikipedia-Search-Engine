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

def getChar(num):
    if (num >= 0 and num <= 9):
        return chr(num + ord('0'))
    else:
        return chr(num - 10 + ord('A'))

def getNum(str):
    if str >= '0' and str <= '9':
        return ord(str) - ord('0')
    else:
        return ord(str) - ord('A') + 10

def encode32(num):

    out = ""
    while num:
        out += getChar(num % 32)
        num = num // 32

    return out[::-1]

def decode32(str):

    num = 0
    str = str[::-1]
    for i in range(len(str)):
        num += getNum(str[i]) * (32 ** i)
    return num