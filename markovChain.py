import csv
import numpy as np

from scipy.sparse import dok_matrix

import random
from random import random 
import nltk
nltk.download('punkt')

from nltk.tokenize import word_tokenize

class MarkovChain():

    def __init__(self, k_gram):
        self.k_gram = k_gram
        self.corpus = ""
        self.corpus_words = []
        self.corpus_words_pos_tag = []
        self.distinct_words_in_corpus = []
        self.corpus_words_index = {}
        self.distinct_words_in_corpus_count = 0
        self.sets_of_k_words_in_corpus = []
        self.sets_of_k_words_count = 0
        self.distinct_sets_of_k_words_in_corpus = []
        self.corpus_k_words_index = {}
        self.transition_matrix_k_words = dok_matrix((0,0))

        self.corresponding_word_postag_dict = {}
        self.distinct_pos_tag_in_corpus = []
        self.pos_tag_following_dict = {}
        self.sets_of_k_pos_tags = []

    def populateCorpus(self, filepath):
        with open(filepath) as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                self.corpus+=row[0]
        
        self.corpus = self.corpus.replace('\n',' ')
        self.corpus = self.corpus.replace('\t',' ')
        self.corpus = self.corpus.replace('“', ' " ')
        self.corpus = self.corpus.replace('”', ' " ')
        '''
        for spaced in ['.','-',',','!','?','(','—',')']:
            self.corpus = self.corpus.replace(spaced, ' {0} '.format(spaced))

        self.corpus_words = self.corpus.split(' ')
        self.corpus_words = [word for word in self.corpus_words if word != '']
        '''
        self.corpus_words = nltk.word_tokenize(self.corpus)

        print("corpus_words: ", self.corpus_words)

        self.corpus_words_pos_tag = nltk.pos_tag(self.corpus_words)
        print("corpus_words_pos_tag: ", self.corpus_words_pos_tag)


        for word_tag_pair in self.corpus_words_pos_tag:
            if word_tag_pair[0] in self.corresponding_word_postag_dict.keys(): 
                self.corresponding_word_postag_dict[word_tag_pair[0]].add(word_tag_pair[1])
                print("check point")
            else: 
                self.corresponding_word_postag_dict[word_tag_pair[0]] = {word_tag_pair[1]}
                print("word tag pair [1]: ", word_tag_pair[1])

        print("corresponding word postag dict: ", self.corresponding_word_postag_dict)


        self.corpus_words_pos_tag = [postag[1] for postag in self.corpus_words_pos_tag]

        self.distinct_words_in_corpus = list(set(self.corpus_words))
        self.corpus_words_index = {word: index for index, word in enumerate(self.distinct_words_in_corpus)}
        self.distinct_words_in_corpus_count = len(self.distinct_words_in_corpus)


        self.distinct_pos_tag_in_corpus = list(set([postag for postag in self.corpus_words_pos_tag]))

        print("distinct pos tag: ", self.distinct_pos_tag_in_corpus)

    def buildTransitionMatrix(self):
        self.sets_of_k_words_in_corpus = [ ' '.join(self.corpus_words[i:i+self.k_gram]) for i, _ in enumerate(self.corpus_words[:-self.k_gram])]
        print("sets of k words: ", self.sets_of_k_words_in_corpus)
        self.sets_of_k_words_count = len(list(set(self.sets_of_k_words_in_corpus)))

        self.transition_matrix_k_words = dok_matrix((self.sets_of_k_words_count, self.distinct_words_in_corpus_count))

        self.distinct_sets_of_k_words_in_corpus = list(set(self.sets_of_k_words_in_corpus))

        self.corpus_k_words_index = {word: index for index, word in enumerate(self.distinct_sets_of_k_words_in_corpus)}

        k_words_sequence_index = 0
        following_word_index = 0

        for index, word in enumerate(self.sets_of_k_words_in_corpus[:-self.k_gram]):
            k_words_sequence_index = self.corpus_k_words_index[word]
            following_word_index = self.corpus_words_index[self.corpus_words[index+self.k_gram]]
            self.transition_matrix_k_words[k_words_sequence_index, following_word_index] += 1
    
    def makePairs(self): 
        for i in range(len(self.corpus_words_pos_tag) - self.k_gram -1):
            yield (self.corpus_words_pos_tag[i: i+self.k_gram], self.corpus_words_pos_tag[i+self.k_gram+1])

    def buildPosTagFollowingDict(self):
        self.sets_of_k_pos_tags = [ ' '.join(self.corpus_words_pos_tag[i: i+self.k_gram]) for i, _ in enumerate(self.corpus_words_pos_tag[:-self.k_gram])]
        
        print("sets of k pos tags: ", self.sets_of_k_pos_tags)
        
        for prev_k_pos_tags, next_pos_tag in self.makePairs():
            print("prev k pos tags: ", prev_k_pos_tags)
            prev_k_pos_tags_as_str = ' '.join(prev_k_pos_tags)
            print("prev k pos tags as string", ' '.join(prev_k_pos_tags))
            print("next pos tag: ", next_pos_tag)
            if prev_k_pos_tags_as_str in self.pos_tag_following_dict.keys():
                self.pos_tag_following_dict[prev_k_pos_tags_as_str].append(next_pos_tag)
            else:
                self.pos_tag_following_dict[prev_k_pos_tags_as_str] = [next_pos_tag]
        
        print("pos tags dict: \n", self.pos_tag_following_dict)

    def weighted_choice(self, objects, weights):
        weights = np.array(weights, dtype=np.float64)
        sum_of_weights = weights.sum()
        # standardization:
        np.multiply(weights, 1 / sum_of_weights, weights)
        # print("weight before: ", weights[-1])
        weights = weights.cumsum()
        #print("weight after: ", weights[-1])
        x = random()
        print("x: ", x)
        for i in range(len(weights)):
            if x < weights[i]:
                return objects[i]

    
    def chooseWordFollowingKWords(self, k_words_sequence, alpha = 0):
        following_word_vector = self.transition_matrix_k_words[self.corpus_k_words_index[k_words_sequence]] + alpha

        transitionProb = following_word_vector / following_word_vector.sum()

        next_word = self.weighted_choice(self.distinct_words_in_corpus, transitionProb.toarray())
        next_word_pos_tag = self.corresponding_word_postag_dict[next_word]

        '''
        k_words_sequence_pos_tag = [self.corresponding_word_postag_dict[word] for word in k_words_sequence.split()]
        print("check k_words sequence: ", k_words_sequence)

        k_words_sequence_pos_tag_list = set.union(*k_words_sequence_pos_tag)
        print("k words sequence pos tag check : ", k_words_sequence_pos_tag_list)
        '''
        print("check k_words sequence: ", k_words_sequence)
        k_sequence_tokens = nltk.word_tokenize(k_words_sequence)
        k_words_sequence_pos_tag  = nltk.pos_tag(k_sequence_tokens)
        print("k words sequence pos tag: ", k_words_sequence_pos_tag)
        k_words_sequence_pos_tag_list = [pos_tag[1] for pos_tag in k_words_sequence_pos_tag]
        print("k words sequence pos tag list: ", k_words_sequence_pos_tag_list)

        next_word = self.weighted_choice(self.distinct_words_in_corpus, transitionProb.toarray())
        next_word_pos_tag = self.corresponding_word_postag_dict[next_word]
        '''
        if ' '.join(k_words_sequence_pos_tag_list) in self.pos_tag_following_dict.keys(): 

            print("check post tag dict : ", self.pos_tag_following_dict[' '.join(k_words_sequence_pos_tag_list)])
            i = 0
            fail_count = 0

            while next_word_pos_tag not in self.pos_tag_following_dict[' '.join(k_words_sequence_pos_tag_list)]:
                next_word = self.weighted_choice(self.distinct_words_in_corpus, transitionProb.toarray())
                next_word_pos_tag = self.corresponding_word_postag_dict[next_word]
                print("next_word: ", next_word)
                print("next_word_pos_tag: ", next_word_pos_tag)
                if i>5000:
                    fail_count += 1 
                    break
                i += 1
        print("fail count: ", fail_count)
        '''
        return next_word

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
        
        return sentence
        
    def generateFromRandomStartSequence(self, num_of_words_to_generate): 
        first_k_words = np.random.choice(self.sets_of_k_words_in_corpus)

        while first_k_words[0].islower():
            first_k_words = np.random.choice(self.sets_of_k_words_in_corpus)
        
        return self.markovChainGenerator(first_k_words, num_of_words_to_generate)