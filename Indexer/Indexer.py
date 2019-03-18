import re
import json
import tkinter
from tkinter import filedialog

from Libraries.porterStemmer import *


def comp(list1, list2):
    for val in list2:
        list1 = [x for x in list1 if x != val]
    return list1


def unique(list1):
    myset = set(list1)
    return list(myset)


def invertedfreq(list1, list2,hashtable):

    for item in sorted(list2):  # iterates through the sorted items.
        #print(item, documentIndex ,list1.count(item))
        if item not in hashtable: hashtable[item]=[0]
        hashtable[item].append([documentIndex, list1.count(item)])
        hashtable[item][0] += 1
    return


def invertedindex(text):

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
    invertedfreq(text, stems,indexHash)
    return


def index(documentindex, title, author, book):
    indexfile[documentindex]=(title, author, book)
    return


p = PorterStemmer()
header = 0
text = []
title = str()
author = str()
book = str()
stopWords = []
indexfile = dict()
documentIndex = ''
indexHash = dict()
# Creation of the stop words list
infile = open("stopWords.txt", 'r')
for line in infile:
    if line == '':
        break
    stopWords.extend(line.split())
infile.close()


#infile = open("test", 'r')
#infile = open("testfiles/cran.all.1400", 'r')
root = tkinter.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(initialdir = "./testfiles",title = "choose your file")
infile = open(file_path,'r')
for line in infile:

    matchHeader = re.match(r'\.(.*?)$', line, re.M|re.I)
    if line == '':
        break
    if not matchHeader and header == 0:
        title += line.rstrip('\n')
    if not matchHeader and header == 2:
       author += line.rstrip('\n')
    if not matchHeader and header == 3:
       book += line.rstrip('\n')

    if not matchHeader and header == 1:
        text.extend(re.findall(r"[\w]+'?\.?[\w]+", line.casefold()))

    if matchHeader:
        if text:

            invertedindex(text)


        if matchHeader.group(1) == "T":

            header = 0

        elif matchHeader.group(1) == "A":
            # print ("Author:")
            header = 2
        elif matchHeader.group(1) == "B":
            # print ("Bib:")
            header = 3
        elif matchHeader.group(1) == "W":
            header = 1
            index(documentIndex, title, author, book)
        else:
            if re.match(r'I (.*?)$', matchHeader.group(1), re.M | re.I):
                author = book = title = ''
                #print("\n Id", re.match(r'I (.*?)$', matchHeader.group(1), re.M | re.I).group(1))
                documentIndex = re.match(r'I (.*?)$', matchHeader.group(1), re.M | re.I).group(1)
                text = []
            else:
                print("No match!!")
infile.close()
if text:
    invertedindex(text)
    index(documentIndex ,title, author,book)

# for x in range(1401):
#     if (str(x) not in indexfile.keys()):
#         print(x)

for keys, values in indexHash.items():
     print(keys)
     print(values)

with open('invertedfile.json','w')as fp:
    json.dump(indexHash,fp)

with open('indexfile.json','w')as fp:
    json.dump(indexfile,fp)