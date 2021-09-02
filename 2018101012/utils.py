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