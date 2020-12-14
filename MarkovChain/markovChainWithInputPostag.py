# **
# CMPU 365 - Jason Lee, Nhan Nguyen
# Code adapted from Luciano Strika - https://www.datastuff.tech/machine-learning/markov-chains-teaching-ai-to-write-game-of-thrones/
# Markov Chain with a POS tag look up table
# works for tri-gram and above, but not useful
# **
from MarkovChain.markovChain import MarkovChain
import numpy as np
from scipy.sparse import dok_matrix
import nltk
import random
from random import random, choice
from nltk.tokenize import word_tokenize
from nltk.corpus import words

class MarkovChainWithInputPostag(MarkovChain):
    def __init__(self, userText, **kwds):
        self.userText = nltk.word_tokenize(userText)
        
        self.distinct_pos_tag_in_corpus = []
        self.pos_tag_following_dict = {}
        self.sets_of_k_pos_tags = []
        super().__init__(**kwds) 

    def handlePostag(self): 
        self.corpus_words_pos_tag = nltk.pos_tag(self.corpus_words)
  
        self.corpus_words_pos_tag = [postag[1] for postag in self.corpus_words_pos_tag]
        self.distinct_pos_tag_in_corpus = list(set([postag for postag in self.corpus_words_pos_tag]))

    def generateSubsequentPostag(self):
        for i in range(len(self.corpus_words_pos_tag) - self.k_prev -1):
            yield (self.corpus_words_pos_tag[i: i+self.k_prev], self.corpus_words_pos_tag[i+self.k_prev+1])
        
    def buildPosTagFollowingDict(self):
        self.sets_of_k_pos_tags = [ ' '.join(self.corpus_words_pos_tag[i: i+self.k_prev]) for i, _ in enumerate(self.corpus_words_pos_tag[:-self.k_prev])]
        
        for prev_k_pos_tags, next_pos_tag in self.generateSubsequentPostag():
            prev_k_pos_tags_as_str = ' '.join(prev_k_pos_tags)
            if prev_k_pos_tags_as_str in self.pos_tag_following_dict.keys():
                self.pos_tag_following_dict[prev_k_pos_tags_as_str].append(next_pos_tag)
            else:
                self.pos_tag_following_dict[prev_k_pos_tags_as_str] = [next_pos_tag]
            
    def pick_word_from_vector(self, distinct_words, weights, k_sequence_pos_tag):
        weights = np.array(weights, dtype=np.float64)
        sum_of_weights = weights.sum()
        np.multiply(weights, 1 / sum_of_weights, weights)
       
        max_prob = float("-inf")
        best_word = ""
        for i in range(len(distinct_words)):
            cur_word = distinct_words[i]
            corpus_words_pos_tag = nltk.pos_tag([cur_word])[0][1]
            if corpus_words_pos_tag in k_sequence_pos_tag:
                if weights[0, i] > max_prob:
                    max_prob = weights[0, i]
                    best_word = cur_word
        return best_word

    def chooseWordFollowingKWords(self, k_words_sequence, alpha = 0):
        k_sequence_tokens = nltk.word_tokenize(k_words_sequence)
        k_words_sequence_pos_tag  = nltk.pos_tag(k_sequence_tokens)
        k_words_sequence_pos_tag_list = [pos_tag[1] for pos_tag in k_words_sequence_pos_tag]
    
        if k_words_sequence in self.corpus_k_words_index.keys(): 
            following_word_vector = self.transition_matrix_k_words[self.corpus_k_words_index[k_words_sequence]] + alpha

            transitionProb = following_word_vector / following_word_vector.sum()
                        

            next_word = self.pick_word_from_vector(self.distinct_words_in_corpus, transitionProb.toarray(), k_words_sequence_pos_tag_list)
        else: 
            next_word = choice(self.distinct_words_in_corpus)
            if ' '.join(k_words_sequence_pos_tag_list) in self.pos_tag_following_dict.keys():
                while (nltk.pos_tag([next_word])[0][1] not in self.pos_tag_following_dict[' '.join(k_words_sequence_pos_tag_list)]):
                    # print("possible following postag: ", self.pos_tag_following_dict[' '.join(k_words_sequence_pos_tag_list)])
                    next_word = choice(self.distinct_words_in_corpus)
        return next_word
    
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
            
        return sentence