# **
# CMPU 365 - Jason Lee, Nhan Nguyen
# Code adapted from Luciano Strika - https://www.datastuff.tech/machine-learning/markov-chains-teaching-ai-to-write-game-of-thrones/
# Basic Markov Chain n-gram model with no input
# **

import csv
import numpy as np

from scipy.sparse import dok_matrix

import random
from random import random 
import sys 
sys.path.append('..')
from helper import cleanText

class MarkovChain():

    def __init__(self, n_gram, **kwds):
        self.k_prev = n_gram-1 # k = n-1
        self.corpus = ""
        self.corpus_words = []
        self.distinct_words_in_corpus = []
        self.corpus_words_index = {}
        self.distinct_words_in_corpus_count = 0
        self.sets_of_k_words_in_corpus = []
        self.sets_of_k_words_count = 0
        self.distinct_sets_of_k_words_in_corpus = []
        self.corpus_k_words_index = {}
        self.transition_matrix_k_words = dok_matrix((0,0))

        super().__init__(**kwds)
        
    def populateCorpus(self, filepath):
        with open(filepath) as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                self.corpus+=row[0]
        
        self.corpus = cleanText(self.corpus)

        # treat these punctuation as tokens
        for punctuation in ['.','-',',','!','?','(','—',')']:
            self.corpus = self.corpus.replace(punctuation, ' {0} '.format(punctuation))

        self.corpus_words = self.corpus.split(' ')
        self.corpus_words = [word for word in self.corpus_words if word != '']
    
        self.distinct_words_in_corpus = list(set(self.corpus_words))
        self.corpus_words_index = {word: index for index, word in enumerate(self.distinct_words_in_corpus)}
        self.distinct_words_in_corpus_count = len(self.distinct_words_in_corpus)

    # **
    # We learned the use of dok_matrix from Luciano Strika's implementation
    # **
    def buildTransitionMatrix(self):
        self.sets_of_k_words_in_corpus = [ ' '.join(self.corpus_words[i:i+self.k_prev]) for i, _ in enumerate(self.corpus_words[:-self.k_prev])]
        self.sets_of_k_words_count = len(list(set(self.sets_of_k_words_in_corpus)))

        self.transition_matrix_k_words = dok_matrix((self.sets_of_k_words_count, self.distinct_words_in_corpus_count))

        self.distinct_sets_of_k_words_in_corpus = list(set(self.sets_of_k_words_in_corpus))

        self.corpus_k_words_index = {word: index for index, word in enumerate(self.distinct_sets_of_k_words_in_corpus)}

        k_words_sequence_index = 0
        following_word_index = 0

        for index, word in enumerate(self.sets_of_k_words_in_corpus[:-self.k_prev]):
            k_words_sequence_index = self.corpus_k_words_index[word]
            following_word_index = self.corpus_words_index[self.corpus_words[index+self.k_prev]]
            self.transition_matrix_k_words[k_words_sequence_index, following_word_index] += 1


    def chooseBestWord(self, distinctWords, weightsVector):
        weights = np.array(weightsVector, dtype=np.float64)
        sum_of_weights = weights.sum()
        # normalize the weights vector
        np.multiply(weights, 1 / sum_of_weights, weights)
        weights = weights.cumsum()
        x = random()
        # choose next words given the corresponding weights
        for i in range(len(weights)):
            if x < weights[i]:
                return distinctWords[i]

    
    def chooseWordFollowingKWords(self, k_words_sequence, alpha = 0): 
        # alpha - Laplace smoothing - keep it at 0 since our vocabulary is too small 
        # and thus would generate new k-word-sequence that would not be in our transition matrix
        following_word_vector = self.transition_matrix_k_words[self.corpus_k_words_index[k_words_sequence]] + alpha

        transitionProb = following_word_vector / following_word_vector.sum()

        return self.chooseBestWord(self.distinct_words_in_corpus, transitionProb.toarray())

    def markovChainGenerator(self, prev_k_words, num_of_words_to_generate):
        prev_k_words_sequence = prev_k_words.split(' ')

        if len(prev_k_words_sequence) != self.k_prev:
            raise ValueError(f'expect {self.k_prev} for the initial sequence')

        sentence = prev_k_words

        for i in range(num_of_words_to_generate): 
            sentence += ' '
            following_word = self.chooseWordFollowingKWords(' '.join(prev_k_words_sequence))
            sentence += following_word
            prev_k_words_sequence = prev_k_words_sequence[1:]+[following_word]

        following_word = self.chooseWordFollowingKWords(' '.join(prev_k_words_sequence))
        
        while (following_word != '.'): 
            sentence += ' '
            following_word = self.chooseWordFollowingKWords(' '.join(prev_k_words_sequence))
            sentence += following_word
            prev_k_words_sequence = prev_k_words_sequence[1:]+[following_word]
        return sentence
        
    def generateFromRandomStartSequence(self, num_of_words_to_generate): 
        first_k_words = np.random.choice(self.sets_of_k_words_in_corpus)

        while not first_k_words[0].isalpha():
            first_k_words = np.random.choice(self.sets_of_k_words_in_corpus)
        return self.markovChainGenerator(first_k_words, num_of_words_to_generate)