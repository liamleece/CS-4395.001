# Kyle Zarzana KJZ190000
# Liam Leece LCL180002
# CS 4395.001
# Professor Karen Mazidi


import os  # used by method 1
import pickle
import re
import nltk


# Each bigram’s probability with Laplace smoothing is: (b + 1) / (u + v) where b is
# the bigram count, u is the unigram count of the first word in the bigram, and v is the total vocabulary
# size (add the lengths of the 3 unigram dictionaries).
def calc_probabilites(text, uni_dict, bi_dict, v):

    p_laplace = 1
    unigrams_test = nltk.word_tokenize(text)
    bigrams_test = list(nltk.ngrams(unigrams_test, 2))

    for bigram in bigrams_test:
        b = bi_dict[bigram] if bigram in bi_dict else 0
        u = uni_dict[bigram[0]] if bigram[0] in uni_dict else 0

        p_laplace = p_laplace * ((b + 1) / (u + v))

    return p_laplace


# Compares the language guesses to the solutions
def compare_list(list, sol_list):
    count = 0
    failures = []
    for i in range(len(sol_list)):
        if list[i] == sol_list[i]:
            count += 1
        else:
            failures.append(i)

    print('Line numbers of test failures: ')
    print(failures)
    return count / len(sol_list)


if __name__ == '__main__':
    dict_in1 = pickle.load(open('d1.p', 'rb'))  # read binary
    dict_in2 = pickle.load(open('d2.p', 'rb'))  # read binary
    dict_in3 = pickle.load(open('d3.p', 'rb'))  # read binary
    dict_in4 = pickle.load(open('d4.p', 'rb'))  # read binary
    dict_in5 = pickle.load(open('d5.p', 'rb'))  # read binary
    dict_in6 = pickle.load(open('d6.p', 'rb'))  # read binary

    # Test file
    v = len(dict_in1) + len(dict_in3) + len(dict_in5)
    with open(os.path.join(os.getcwd(), 'LangId.test'), 'r', encoding='utf-8') as f:
        text_in = f.read()

    # Solution File
    with open(os.path.join(os.getcwd(), 'LangId.sol'), 'r', encoding='utf-8') as f:
        sol = f.read()

    # Determine the lang
    lines = text_in.split('\n')
    results = []
    for s in lines:
        eng = calc_probabilites(s, dict_in1, dict_in2, v)
        fr = calc_probabilites(s, dict_in3, dict_in4, v)
        it = calc_probabilites(s, dict_in5, dict_in6, v)
        lang = max(eng, fr, it)

        if eng == lang:
            results.append("English")
        elif fr == lang:
            results.append("French")
        elif it == lang:
            results.append("Italian")

    sol_list = re.sub(r'\d+', '', sol)
    sol_list = nltk.word_tokenize(sol_list)
    accuracy = compare_list(results, sol_list)
    print(accuracy)



