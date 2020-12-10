import csv
import numpy as np

from scipy.sparse import dok_matrix
from helper import cleanText

import random
from random import random 

import nltk
nltk.download('punkt')

from nltk.tokenize import word_tokenize
from nltk.corpus import words

class MarkovChain():

    def __init__(self, k_gram, userText):
        self.k_gram = k_gram
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

        self.userText = nltk.word_tokenize(userText)

    def populateCorpus(self, filepath):
        with open(filepath) as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                self.corpus+=row[0]
        
        self.corpus = self.corpus.replace('\n',' ')
        self.corpus = self.corpus.replace('\t',' ')
        self.corpus = self.corpus.replace('“', ' " ')
        self.corpus = self.corpus.replace('”', ' " ')

        self.corpus = cleanText(self.corpus)

        for spaced in ['.','-',',','!','?','(','—',')']:
            self.corpus = self.corpus.replace(spaced, ' {0} '.format(spaced))

        self.corpus_words = self.corpus.split(' ')
        self.corpus_words = [word for word in self.corpus_words if word != '']
        print("len corpus_words: ", len(self.corpus_words))
    
        self.distinct_words_in_corpus = list(set(self.corpus_words))
        self.corpus_words_index = {word: index for index, word in enumerate(self.distinct_words_in_corpus)}
        self.distinct_words_in_corpus_count = len(self.distinct_words_in_corpus)

    def buildTransitionMatrix(self):
        self.sets_of_k_words_in_corpus = [ ' '.join(self.corpus_words[i:i+self.k_gram]) for i, _ in enumerate(self.corpus_words[:-self.k_gram])]
        print("sets of k words: ", self.sets_of_k_words_in_corpus)
        self.sets_of_k_words_count = len(list(set(self.sets_of_k_words_in_corpus)))

        self.transition_matrix_k_words = dok_matrix((self.sets_of_k_words_count, self.distinct_words_in_corpus_count))

        self.distinct_sets_of_k_words_in_corpus = list(set(self.sets_of_k_words_in_corpus))

        self.corpus_k_words_index = {word: index for index, word in enumerate(self.distinct_sets_of_k_words_in_corpus)}

        k_words_sequence_index = 0
        following_word_index = 0

        '''
        for index, word in enumerate(self.sets_of_k_words_in_corpus[:-self.k_gram]):
            
            k_words_sequence_index = self.corpus_k_words_index[word]
            following_word_index = self.corpus_words_index[self.corpus_words[index+self.k_gram]]
            self.transition_matrix_k_words[k_words_sequence_index, following_word_index] += 1
        '''
        
        for index, k_words in enumerate(self.sets_of_k_words_in_corpus[:-self.k_gram]):
            k_words_sequence_index = self.corpus_k_words_index[k_words]
            following_word_index = self.corpus_words_index[self.corpus_words[index+self.k_gram]]
            print("word: ", k_words)
            
            wordInUserText = False
            countSimilarWord = 0

            
            for word in k_words:
                if word in self.userText:
                    countSimilarWord +=1
                    wordInUserText = True
            if wordInUserText: 
                print("check point words in text")
                self.transition_matrix_k_words[k_words_sequence_index, following_word_index] += 10**(countSimilarWord)
            else: 
                self.transition_matrix_k_words[k_words_sequence_index, following_word_index] += 1
        
            


    def weighted_choice(self, objects, weights):
        weights = np.array(weights, dtype=np.float64)
        sum_of_weights = weights.sum()
        # standardization:
        np.multiply(weights, 1 / sum_of_weights, weights)
        print("weight before: ", weights[-1])
        weights = weights.cumsum()
        print("weight after: ", weights[-1])
        x = random()
        for i in range(len(weights)):
            if x < weights[i]:
                return objects[i]

    
    def chooseWordFollowingKWords(self, k_words_sequence, alpha = 0):
        following_word_vector = self.transition_matrix_k_words[self.corpus_k_words_index[k_words_sequence]] + alpha

        transitionProb = following_word_vector / following_word_vector.sum()

        return self.weighted_choice(self.distinct_words_in_corpus, transitionProb.toarray())

    def markovChainGenerator(self, prev_k_words, num_of_words_to_generate):
        prev_k_words_sequence = prev_k_words.split(' ')

        if len(prev_k_words_sequence) != self.k_gram:
            raise ValueError(f'expect {self.k_gram} for the initial sequence')

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

        while first_k_words[0].islower() and not first_k_words[0].isalpha():
            first_k_words = np.random.choice(self.sets_of_k_words_in_corpus)
        
        return self.markovChainGenerator(first_k_words, num_of_words_to_generate)