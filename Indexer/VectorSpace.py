__author__ = 'Marc'
import json
import re
import math
from pprint import pprint
from Libraries.porterStemmer import *
from functools import reduce

def comp(list1, list2):
    for val in list2:
        list1 = [x for x in list1 if x != val]
    return list1

def intersection(list1, list2):
    inter = [x for x in list1 if x in list2]
    return inter

def unique(list1):
    myset = set(list1)
    return list(myset)

def stemmer(text):
    stems = []
    output = ''
    text = [x for x in text if x != "."]
    text = comp(text, stopWords)
    for word in text:
        # print(word)
        output += p.stem(word, 0, len(word)-1)
        stems.append(output)
        output = ''

    text = stems
    stems = unique(text)
    stems.sort()
    return stems
    #print(stems)


IDF = dict()
p = PorterStemmer()
stopWords = []
# Creation of the stop words list
infile = open("stopWords.txt", 'r')
for line in infile:
    if line == '':
        break
    stopWords.extend(line.split())
infile.close()

with open('invertedfile.json')as fp:
    invertedIndex = json.load(fp)
    fp.close()
with open('indexfile.json')as fp:
    indexFile= json.load(fp)
    fp.close()

print('Preparing files...')
N = len(indexFile)
print(N,'documents in library \n',len(invertedIndex), 'terms in dictionnary')
TF = [[float(0) for x in range(len(invertedIndex))] for x in range(N)]
Wd = [0 for x in range(N)]

#Creation of the IDF and TF tables
j = 0
for key,values in invertedIndex.items():

    IDF[key] = math.log(1 + N/values[0])
    for tuples in values[1:] :

        TF[int(tuples[0])-1] [j]= 1 + math.log(tuples[1])


    j += 1
#Wd calculation
for x in range(N):
   Wd[x] = math.sqrt(reduce(lambda x, y : x+y,(map( lambda x : math.pow(x,2),TF[x]))))

while True:
    query = input("Search for : ")
    queryvector = stemmer(re.findall(r"[\w]+'?\.?[\w]+", query.casefold()))
    queryvector = intersection(queryvector,invertedIndex.keys())
    #print(queryvector)
    if not queryvector :
        print('not found')
        continue
    Wq = 0
    for terms in queryvector:
        Wq += math.pow(IDF[terms],2)
    Wq = math.sqrt(Wq)
    TFQuery = [[0 for x in range(len(queryvector))] for x in range(N)]
    IDFQuery = [0 for x in range(len(queryvector))]
    #Wd change pour chaque document somme de la colonne
    j=0
    for term in queryvector:

         IDFQuery[j]= IDF[term]
         for tuples in invertedIndex[term][1:]:

            TFQuery [int(tuples[0])-1][j] = 1 + math.log(tuples[1])

         j += 1



    distance = []
    for i in range(N):
        sum = j = 0
        for x in TFQuery[i]:
            sum += x * IDFQuery[j]
            #print(x*IDFQuery[j])
            j += 1
        #print(sum)
        if (sum > 0 and (Wd[i]*Wq)>0):
            distance.append( (i+1,sum/(Wd[i]*Wq)))

    #map(lambda x: map(lambda y: y | b, x), a)
    #print(distance)
    #print(TF[470])
    #print(TF[994])

    # pprint(TFQuery)
    # pprint(IDFQuery)
    # print(Wd)
    # print(Wq)



    distance.sort(key = lambda  tuple : tuple[1], reverse= True)
    for tup in distance[:20]:
        print(tup[0],indexFile[str(tup[0])], tup[1])



