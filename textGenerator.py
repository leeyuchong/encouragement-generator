corpus = ""

import csv
import numpy as np

with open('encouragement_comments.csv') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',')
    for row in csvReader:
        corpus+=row[0]

corpus = corpus.replace('\n',' ')
corpus = corpus.replace('\t',' ')
corpus = corpus.replace('“', ' " ')
corpus = corpus.replace('”', ' " ')

for spaced in ['.','-',',','!','?','(','—',')']:
    corpus = corpus.replace(spaced, ' {0} '.format(spaced))

print(corpus)
print(" ")
print(len(corpus))

corpus_words = corpus.split(' ')
corpus_words= [word for word in corpus_words if word != '']
corpus_words 
print("len corpus_words: ", len(corpus_words))
print("type of corpus_words: ", type(corpus_words))
len(corpus_words) # 2185920

distinct_words = list(set(corpus_words))
word_idx_dict = {word: i for i, word in enumerate(distinct_words)}
distinct_words_count = len(list(set(corpus_words)))
print("distict_words_count: ", distinct_words_count)
distinct_words_count # 32663


k = 3 # adjustable
sets_of_k_words = [ ' '.join(corpus_words[i:i+k]) for i, _ in enumerate(corpus_words[:-k]) ]

print("set_of_k_words: ", sets_of_k_words)

from scipy.sparse import dok_matrix

sets_count = len(list(set(sets_of_k_words)))
next_after_k_words_matrix = dok_matrix((sets_count, len(distinct_words)))

print("next_after_k_words_matrix: ", next_after_k_words_matrix)
print("")
distinct_sets_of_k_words = list(set(sets_of_k_words))
k_words_idx_dict = {word: i for i, word in enumerate(distinct_sets_of_k_words)}
print("k_words_idx_dict: ", k_words_idx_dict)

for i, word in enumerate(sets_of_k_words[:-k]):

    word_sequence_idx = k_words_idx_dict[word]
    next_word_idx = word_idx_dict[corpus_words[i+k]]
    next_after_k_words_matrix[word_sequence_idx, next_word_idx] +=1


import random
from random import random 

def weighted_choice(objects, weights):
    """ returns randomly an element from the sequence of 'objects', 
        the likelihood of the objects is weighted according 
        to the sequence of 'weights', i.e. percentages."""

    weights = np.array(weights, dtype=np.float64)
    sum_of_weights = weights.sum()
    # standardization:
    np.multiply(weights, 1 / sum_of_weights, weights)
    weights = weights.cumsum()
    x = random()
    for i in range(len(weights)):
        if x < weights[i]:
            return objects[i]

def sample_next_word_after_sequence(word_sequence, alpha = 0):
    next_word_vector = next_after_k_words_matrix[k_words_idx_dict[word_sequence]] + alpha
    print("next_word_vector: ", next_word_vector)
    
    # frequency of sequential sets of k-words over the samples of the current words
    likelihoods = next_word_vector/next_word_vector.sum()
    
    print("likelihoods: ", likelihoods.toarray())

    return weighted_choice(distinct_words, likelihoods.toarray())
    
def stochastic_chain(seed, chain_length, seed_length):
    current_words = seed.split(' ')
    if len(current_words) != seed_length:
        raise ValueError(f'wrong number of words, expected {seed_length}')
    sentence = seed

    for _ in range(chain_length):
        sentence+=' '
        next_word = sample_next_word_after_sequence(' '.join(current_words))
        sentence+=next_word
        current_words = current_words[1:]+[next_word]
    return sentence
# example use    

first_k_words = np.random.choice(sets_of_k_words)

while first_k_words[0].islower() and not first_k_words[0].isalpha():
    first_k_words = np.random.choice(sets_of_k_words)

print(stochastic_chain(first_k_words.capitalize(), 25, 3))