import json

from Libraries import pyparsing as pp

from Libraries.porterStemmer import *


def contrary(list1, list2):
    not_list1 = [x for x in list1 if x not in list2]
    return not_list1


def intersection(list1, list2):
    inter = [x for x in list1 if x in list2]
    return inter


def union(list1, list2):
    """
    return the 
    :param list1: a list of document ids for a keyword
    :param list2: a list of docunent ids for another keyword
    :return: returns the concatenation of the two lists above
    """
    return list1 + list2


def document_list(key, index):

    """
    this function returns the list of ids
    :param key: the word to be searched in the inverted index
    :param index:  the inverted index of all the documents
    :return: documents, a list of all document ids containing the key
    """
    porter = PorterStemmer()
    documents = []
    stemmed_key = ''
    stemmed_key += porter.stem(key, 0, len(key) - 1)
    if stemmed_key in index:
        for entry in index[stemmed_key][1:]:
            documents.append(entry[0])

    # print(doclist)
    return documents


def binary_search(tree, index):

    """
    the function recursively reads the tree and outputs a list of documents.
    :param tree: the binary search tree containing the query
    :param index: the inverted index on which the query is processed
    :return: a list of documents ids
    """
    if not isinstance(tree, pp.ParseResults):
        return document_list(tree, index)

    elif tree[0] == "NOT":
        docs = binary_search(tree[1], index)
        results = list(range(1, 1401))
        results = ["{:d}".format(x) for x in results]

        return contrary(results, docs)
    elif tree[1] == "AND":
        return intersection(binary_search(tree[0], index), binary_search(tree[2], index))

    elif tree[1] == "OR":
        return union(binary_search(tree[0], index), binary_search(tree[2], index))


def makelrlike(numterms):
    if numterms is None:
        # None operator can only by binary op
        initlen = 2
        incr = 1
    else:
        initlen = {0: 1, 1: 2, 2: 3, 3: 5}[numterms]
        incr = {0: 1, 1: 1, 2: 2, 3: 4}[numterms]

    # define parse action for this number of terms,
    # to convert flat list of tokens into nested list
    def pa(s, l, t):
        t = t[0]
        if len(t) > initlen:
            ret = pp.ParseResults(t[:initlen])
            i = initlen
            while i < len(t):
                ret = pp.ParseResults([ret] + t[i:i + incr])
                i += incr
            return pp.ParseResults([ret])

    return pa


identifier = pp.Word(pp.alphanums)
comparison_term = identifier
condition = identifier

expr = pp.operatorPrecedence(condition, [

    ("NOT", 1, pp.opAssoc.RIGHT, ),
    (pp.oneOf("AND OR"), 2, pp.opAssoc.LEFT, makelrlike(2)),

])


#We load the json file containing the inverted index
with open('invertedfile.json')as fp:
    invertedIndex = json.load(fp)
    fp.close()


while True:
    query = input("Please enter your boolean query using (,),AND,OR,NOT : ")
    if not query:
        print('empty query')
        continue
    binaryTree = expr.parseString(query)[0]
    print(binary_search(binaryTree, invertedIndex))
    print(len(binary_search(binaryTree, invertedIndex)))
