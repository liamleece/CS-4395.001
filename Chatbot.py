import os
import tflearn
import nltk
import numpy
import random
import json
import pickle
from nltk import WordNetLemmatizer
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn

lm = WordNetLemmatizer()


def bag_of_words(s, words_list):
    bg = [0 for _ in range(len(words_list))]

    s_words = nltk.word_tokenize(s)
    s_words = [lm.lemmatize(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words_list):
            if w == se:
                bg[i] = 1

    return numpy.array(bg)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open("intents.json") as file:
        data = json.load(file)
    if os.path.exists('data.pickle'):
        with open("data.pickle", "rb") as f:
            words, labels, training, output = pickle.load(f)
    else:
        words = []
        labels = []
        docs_x = []
        docs_y = []

        for intent in data["intents"]:
            for pattern in intent["patterns"]:
                wrds = nltk.word_tokenize(pattern)
                words.extend(wrds)
                docs_x.append(wrds)
                docs_y.append(intent["tag"])

            if intent["tag"] not in labels:
                labels.append(intent["tag"])

        words = [lm.lemmatize(w.lower()) for w in words if w not in "?"]
        words = sorted(list(set(words)))
        labels = sorted(labels)

        training = []
        output = []

        out_empty = [0 for _ in range(len(labels))]

        # creating the bag of words
        for x, doc in enumerate(docs_x):
            bag = []

            wrds = [w for w in doc]

            for w in words:
                if w in wrds:
                    bag.append(1)
                else:
                    bag.append(0)

            output_row = out_empty[:]
            output_row[labels.index(docs_y[x])] = 1

            training.append(bag)
            output.append(output_row)

        training = numpy.array(training)
        output = numpy.array(output)

        with open("data.pickle", "wb") as f:
            pickle.dump((words, labels, training, output), f)

    # tf learn
    net = tflearn.input_data(shape=[None, len(training[0])])

    # puts 8 nodes in two hidden layers
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)

    model = tflearn.DNN(net)

    if os.path.exists("model.tflearn.meta"):
        model.load("model.tflearn")
    else:
        model.fit(training, output, n_epoch=2000, batch_size=8, show_metric=True)
        model.save("model.tflearn")

    saved_sent = []
    print("Hello! What is your name?")
    inp = input("You: ")
    user_data = open(inp+'.txt', 'w')
    dislike = wn.synset('hate.v.01')
    like = wn.synset('like.v.01')

    while True:

        # sentiment analysis of input
        rand = random.randint(1, 10)
        neg = 0
        pos = 0
        verb = ''
        subject = ''
        verbs = []
        count = 0
        tokens = inp.split()
        tags = nltk.pos_tag(tokens)
        for token in tokens:
            syn_list = list(swn.senti_synsets(token))
            if syn_list:
                syn = syn_list[0]
                neg += syn.neg_score()
                pos += syn.pos_score()

        if neg >= .325 or pos >= .7:
            for t in tags:
                if 'VB' in t[1] and count == 0:
                    verbs = wn.synsets(t[0], pos=wn.VERB)
                    verb = verbs[0]
                    count = count+1
                    break
                # if count == 1 and ('NN' in t[1] or 'DT' in t[1]):
                #     subject += (t[0] + " ")

            if len(str(verb)) != 0:
                if neg >= .325 and wn.wup_similarity(verb, dislike) > .7:
                    user_data.write(inp+'\n')
                    saved_sent.append(inp)
                elif pos >= .625 and wn.wup_similarity(verb, like) > .4:
                    user_data.write(inp+'\n')
                    saved_sent.append(inp)
        # break statement
        if inp.lower() == "quit":
            print("Goodbye!")
            break

        # bag of words prediction
        results = model.predict([bag_of_words(inp, words)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]

        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        if rand >= 9 and saved_sent:
            print("You once said: " + random.choice(saved_sent))
            print("Is this still true?")
        else:
            print(random.choice(responses))
        inp = input("You: ")
