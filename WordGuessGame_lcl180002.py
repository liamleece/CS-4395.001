import os
import sys
import nltk
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords


# Method to open the data file and read in the text
def method1(filepath):
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        text_in = f.read()
    return text_in

# function to preprocess the text for step 3
def processtext(text):
    # removes stop words, capital letters, non alpha characters, and words with less than 5 letters
    stop_words = set(stopwords.words('english'))
    pr_text = [t.lower() for t in text]
    pr_text = [w for w in pr_text if not w.lower() in stop_words]
    pr_text = [w for w in pr_text if w.isalnum()]
    pr_text = [w for w in pr_text if len(w) > 5]

    # lemmatizes the words and finds the nouns
    lemmer = WordNetLemmatizer()
    lemmas = [lemmer.lemmatize(t) for t in pr_text]
    lem_text = list(set(lemmas))
    tags = nltk.pos_tag(lem_text)
    print(tags[:20])
    nouns = [t for t, pos in tags if pos.startswith('N')]
    print('Number of processed tokens: %d' % len(pr_text))
    print('Number of nouns: %d\n' % len(nouns))
    return pr_text, nouns


# Guessing Game function
def guessing_game(wordbank):
    print("-=[ Guessing Game }=-")
    points = 5
    from random import seed
    from random import randint
    seed(1234)

    # outermost while loop so the game can be repeated upon completion
    while True:
        guess = ''
        answer = wordbank[randint(0, 49)]
        board = ""
        for j in range(len(answer)):
            board = board + "_ "
        # inner while loop to get guess from user
        while points > 0:
            print(board)
            guess = input("Enter a letter: ")
            if guess == "!":
                break

            # if the guessed letter is correct: fill in the spot on the board and add a point
            if answer.find(guess) != -1:
                index = [k for k, letter in enumerate(answer) if letter == guess]
                print("Right!")
                for c in index:
                    board = board[:(c*2)] + guess + board[(c*2)+1:]
                points = points + 1
                if board.find("_") == -1:
                    print("You win!!!")
                    print("Final word = " + answer)
                    print("Final score = %d" % points)
                    break
                print("Current score = %d\n" % points)

            # if the guess is wrong, lose a point and try again
            else:
                print("Sorry, guess again")
                points = points - 1
                print("Current score = %d\n" % points)
        ans = input("Play again? (y/n) : ")
        if ans != "y":
            break
    return points


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        fp = sys.argv[1]
        data = method1(fp)
        # calculates lexical diversity for step 2
        tokens = word_tokenize(data)
        utokens = set(tokens)
        print('Lexical Diversity: %.2f' % (len(utokens) / len(tokens)))
        text, nounlist = processtext(tokens)

        # makes a dictionary of the noun list and their frequencies
        Dict = {}
        for t in nounlist:
            Dict[t] = text.count(t)
        sorted_nouns = sorted(Dict.items(), key=lambda x: x[1], reverse=True)
        # gets the top 50 most common nouns from the dictionary
        top50 = []
        for i in range(50):
            top50.append(sorted_nouns[i][0])

# run the Guessing Game code
        score = guessing_game(top50)


