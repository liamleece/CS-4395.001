# Liam Leece & Kyle Zarzana
# lcl180002     kjz190000
# Web Crawler Project
import pickle
from urllib import request
from nltk import sent_tokenize, word_tokenize, RegexpTokenizer
from bs4 import BeautifulSoup
import requests
import re
from nltk.corpus import stopwords

# function to scrape text from the urls provided
# does not alter or trim the text at all
def scrapeText(urls):
    counter = 1
    for u in urls:
        html = request.urlopen(u).read().decode('utf8')
        soup2 = BeautifulSoup(html, features="html.parser")

        # extracts text into 15 files formatted as raw_fileXX.txt
        text = soup2.get_text()
        f2 = open("raw_file{0:02d}.txt".format(counter), 'w', encoding='utf-8')
        f2.write(text)
        counter = counter + 1

# function to clean the text files produced from scrapeText
# removes newlines and tokenizes text into sentences
def cleanFiles():
    for i in range(1, 16):
        f3 = open("raw_file{0:02d}.txt".format(i), 'r', encoding="utf-8")
        text = f3.read()
        f3.close()
        text = re.sub(r'\s+', ' ', text)
        sent = sent_tokenize(text)

        # puts clean text into 15 files formatted as clean_textXX.txt
        f4 = open("clean_file{0:02d}.txt".format(i), 'w', encoding="utf-8")
        for s in sent:
            f4.write(s)
            f4.write('\n')
        f4.close()

# function to clean the text even more and extract the top 25 important words
# removes punctuation, stopwords, whitespace, and capital letters
# picks terms based on frequency count
def extractTerms():
    stop_words = set(stopwords.words('english'))
    for i in range(1, 16):
        f3 = open("clean_file{0:02d}.txt".format(i), 'r', encoding="utf-8")
        text = f3.read()
        tokenizer = RegexpTokenizer(r'\w+')
        text = tokenizer.tokenize(text)
        f3.close()
        filtered_text = []
        word_count = {}
        for t in text:
            if t.lower() not in stop_words:
                filtered_text.append(t.lower())
        for w in filtered_text:
            if w not in word_count:
                word_count[w] = 1
            elif w in word_count:
                word_count[w] += 1

        # prints out the top 25 words along with their frequencies
        sorted_words = dict(sorted(word_count.items(), key=lambda x: x[1], reverse=True))
        print(list(sorted_words.items())[:25])


if __name__ == '__main__':
    # starts with a wiki page about The Princess Bride
    starter_url = "https://en.wikipedia.org/wiki/The_Princess_Bride_(film)"
    r = requests.get(starter_url)
    data = r.text
    soup = BeautifulSoup(data)

    counter = 0
    # write urls to a file
    with open('urls.txt', 'w') as f:
        for link in soup.find_all('a'):
            link_str = str(link.get('href'))

            # removes links leading to more wiki pages along with some links that dont exist anymore
            if link_str.startswith('http') and 'wiki' not in link_str and 'channel4' not in link_str and 'hugo' not in link_str and 'news-of-the-screen' not in link_str:
                f.write(link_str + '\n')
    f.close()

    # saves the first 15 relevant links
    count = 0
    urllist = []
    urllist.append(starter_url)
    with open('urls.txt', 'r') as f:
        urls = f.read().splitlines()
    for u in urls:
        count = count + 1
        urllist.append(u)
        if count == 14:
            break
    f.close()

    scrapeText(urllist)
    cleanFiles()
    extractTerms()

    # Knowledge base
    facts = {'princess': 'The princess lives in the kingdom of Florin',
             'film': 'The film was released in 1987',
             'Reiner': 'Reiner rented a house in England near these sites and frequently invited the cast over for meals and light-hearted get-togethers. Many cast members believed this helped to create a sense of "family" that helped to improve their performances for the film',
             'Hollywood': 'The film was distributed by 20th Century Fox',
             'Elwes': 'During the casting period in Los Angeles, Elwes was in Germany on set for Maschenka. Reiner flew out to Berlin to meet with Elwes, confirming his appropriateness for the role.',
             'giant': 'Fezzik is very tall and big so at a very young age, his parents made him fight competitively.',
             'inconceivable': 'Vizzini is The Sicilian criminal, bully, and mastermind employed by Prince Humperdinck to kidnap Buttercup and kill her, leaving evidence to frame Guilder of the murder so that Humperdinck can declare war',
             'sword': 'When Count Rugen, a nobleman with a six-fingered right hand, asked him to forge a sword to accommodate his unusual grip, Domingo labored over the sword for a year',
             'father': 'Inigos father, Domingo, refused to sell him the sword, not as a matter of money, but because Count Rugen could not appreciate the great work of the sword. He proclaimed that the sword would now belong to Inigo. Rugen then promptly killed Domingo. Eleven-year-old Inigo witnessed the crime and challenged Rugen to a fight, wherein Rugen disarmed Inigo in under a minute',
             'wrestling': 'Andre headlined WrestleMania III in 1987, and in 1988, he defeated Hogan to win the WWF Championship, his sole world heavyweight championship'}
    print()
    for key, value in facts.items():
        print(key, " : ", value)
    pickle.dump(facts, open('dict.p', 'wb'))

