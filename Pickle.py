# Kyle Zarzana KJZ190000
# Liam Leece LCL180002
# CS 4395.001
# Professor Karen Mazidi


import os
import sys
import pickle
from collections import Counter

import nltk
from nltk import word_tokenize

# Reads in the text file and creates bigram and unigram dictionaries.
def method1(filepath):
    with open(os.path.join(os.getcwd(), filepath), 'r', encoding='utf-8') as f:
        text_in = f.read()
    temp = word_tokenize(text_in)
    bigram = list(nltk.ngrams(temp, 2))
    unigram = temp
    print(bigram[:30])
    print(unigram[:30])
    bi_dict = {}

    bi_dict = Counter(bigram)
    un_dict = {}
    un_dict = Counter(unigram)
    return un_dict, bi_dict

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    d1, d2 = method1('LangId.train.English')
    pickle.dump(d1, open('d1.p', 'wb'))
    pickle.dump(d2, open('d2.p', 'wb'))
    d3, d4 = method1('LangId.train.French')
    pickle.dump(d3, open('d3.p', 'wb'))
    pickle.dump(d4, open('d4.p', 'wb'))
    d5, d6 = method1('LangId.train.Italian')
    pickle.dump(d5, open('d5.p', 'wb'))
    pickle.dump(d6, open('d6.p', 'wb'))
