corpusText = ""

import csv
import numpy as np

with open('encouragement_comments.csv') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',')
    for row in csvReader:
        corpusText+=row[0]

corpusText = corpusText.replace('\n',' ')
corpusText = corpusText.replace('\t',' ')
corpusText = corpusText.replace('“', ' " ')
corpusText = corpusText.replace('”', ' " ')

corpus = corpusText.split()


def make_pairs(corpus):
    for i in range(len(corpus)-1):
        yield (corpus[i], corpus[i+1])
        
pairs = make_pairs(corpus)
'''
for pair in pairs: 
    print("pair: ", pair)
word_dict = {}
'''
word_dict = {}

for word_1, word_2 in pairs:
    if word_1 in word_dict.keys():
        word_dict[word_1].append(word_2)
    else:
        word_dict[word_1] = [word_2]
 
first_word = np.random.choice(corpus)

while first_word.islower():
    first_word = np.random.choice(corpus)

chain = [first_word]

n_words = 20

for i in range(n_words):
    print('chain[-1]', chain[-1])
    print("np.random.choice: ", np.random.choice(word_dict[chain[-1]]))
    chain.append(np.random.choice(word_dict[chain[-1]]))

print(' '.join(chain))