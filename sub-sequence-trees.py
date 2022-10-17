import sys
from treelib import Node, Tree

def addUniqueStartingSubsequence(uniqueSubsequences, sequence, index, subSequence):
    if ( index == len(sequence) ):
        if subSequence not in uniqueSubsequences and len(subSequence) != 0:
            uniqueSubsequences.append(subSequence)
    else:
        if subSequence not in uniqueSubsequences and len(subSequence) != 0:
           uniqueSubsequences.append(subSequence)
        addUniqueStartingSubsequence(uniqueSubsequences, sequence, index + 1, subSequence+[sequence[index]])
    return

def createTrees(dict):
    tree = Tree()
    itemsNotInThisTree = {}

    for count, key in enumerate(dict):
        print(str(count/len(dict)*100) + "% of tree calculated")
        memberOfTree = False
        if count == 0:
            tree.create_node(key , key)  # root node
            memberOfTree = True
        else:

            # Just realised I can speed up the searching of the tree by SEARCHING IT AS A TREE, DOH!
            treeAsList = [tree[node].tag for node in tree.expand_tree(mode=Tree.DEPTH)]
            currentLongestSubsequence = 0
            for node in treeAsList:
                if (node == key[0:len(node)]) and (len(node) > currentLongestSubsequence):
                    currentLongestSubsequence += len(node) - currentLongestSubsequence
                    if tree.contains(key):
                        tree.move_node(key, node)
                        memberOfTree = True
                    else:
                        tree.create_node(key , key, parent = node)
                        memberOfTree = True

        if not memberOfTree:
            itemsNotInThisTree[key] = dict[key]

    print('')
    tree.show(line_type="ascii-exr")
    tree.save2file('sequenceTree.txt')
    # any that are not in the tree, add to a new sorted dict and then run through creating the tree again
    if len(itemsNotInThisTree) != 0:
        itemsNotInThisTree = sortDictOnKeyLength(itemsNotInThisTree)
        createTrees(itemsNotInThisTree)


def sortDictOnKeyLength(dict):
    sortedDict = {}
    for k in sorted(dict, key=len):
        sortedDict[k] = dict[k]
    return sortedDict

def removeItemsFromDictThatAreNotInList(dict, inputList):
    modifiedDict = {}
    for sequence in dict:
            if list(sequence) in inputList:
                    modifiedDict[sequence] = dict[sequence]
    return modifiedDict

def main():
    sequences = []

    with open(sys.argv[1]) as f:
        lines = [line.rstrip('\n') for line in f]
        for count, line in enumerate(lines):
            # count can be used here to restrict the amount of lines in the file to read in
            sequence = []
            for char in line:
                sequence.append(char)
            sequences.append(sequence)

    dictOfListsOfUniqueSubsequences = {}
    for sequence in sequences:
        uniqueSubsequences = []
        addUniqueStartingSubsequence(uniqueSubsequences, sequence, 0, [])
        for uniqueSubsequence in uniqueSubsequences:
            uniqueSubsequence = ''.join(uniqueSubsequence)
            if uniqueSubsequence in dictOfListsOfUniqueSubsequences:
                # increase the count value for this sequence in the dictionary
                dictOfListsOfUniqueSubsequences[uniqueSubsequence] = dictOfListsOfUniqueSubsequences[uniqueSubsequence]+1
            else:
                # if not in the dictionary already add it and set count to 1
                dictOfListsOfUniqueSubsequences[uniqueSubsequence] = 1

    # the only items that do not exist in the file that we DO want in the dictionary are single char root nodes. So add them in if they are not present:
    dictOfListsOfUniqueSubsequences = removeItemsFromDictThatAreNotInList(dictOfListsOfUniqueSubsequences, sequences)

    # get root nodes for tree 
    potentialRootNodes = []
    for key in dictOfListsOfUniqueSubsequences:
        if key[0] not in potentialRootNodes:
            potentialRootNodes.append(key[0])

    for potentialRootNode in potentialRootNodes:
        if not (potentialRootNode in dictOfListsOfUniqueSubsequences):
            # how many keys start with the char
            numberOfSequencesStartingWithRootNode = 0
            for sequence in sequences:
                if sequence[0] == potentialRootNode:
                    numberOfSequencesStartingWithRootNode += 1
            dictOfListsOfUniqueSubsequences[potentialRootNode] = numberOfSequencesStartingWithRootNode

    dictOfListsOfUniqueSubsequences = sortDictOnKeyLength(dictOfListsOfUniqueSubsequences)

    with open('sequenceTree.txt', 'w') as f:
        print(dictOfListsOfUniqueSubsequences, file=f)
        print('', file=f)
    print('')
    print(dictOfListsOfUniqueSubsequences)
    print('')
    createTrees(dictOfListsOfUniqueSubsequences)

if __name__ == '__main__':
    main()