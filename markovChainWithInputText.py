import csv
import numpy as np

from scipy.sparse import dok_matrix
from helper import cleanText
import random
from random import random, choice
import nltk
nltk.download('punkt')

from nltk.tokenize import word_tokenize
from nltk.corpus import words

class MarkovChain():

    def __init__(self, k_gram, userText):
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
        '''
        for spaced in ['.','-',',','!','?','(','—',')']:
            self.corpus = self.corpus.replace(spaced, ' {0} '.format(spaced))

        self.corpus_words = self.corpus.split(' ')
        self.corpus_words = [word for word in self.corpus_words if word != '']
        '''
        text = "cripple cripple"
        print("check words in corpus: ", text in self.corpus)
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
        self.sets_of_k_words_in_corpus = [ ' '.join(self.corpus_words[i:i+self.k_gram]) for i, _ in enumerate(self.corpus_words[:-self.k_gram])]
        print("sets of k words: ", self.sets_of_k_words_in_corpus)
        self.sets_of_k_words_count = len(list(set(self.sets_of_k_words_in_corpus)))


    def buildTransitionMatrix(self):
        self.transition_matrix_k_words = dok_matrix((self.sets_of_k_words_count, self.distinct_words_in_corpus_count))

        self.distinct_sets_of_k_words_in_corpus = list(set(self.sets_of_k_words_in_corpus))

        self.corpus_k_words_index = {word: index for index, word in enumerate(self.distinct_sets_of_k_words_in_corpus)}

        k_words_sequence_index = 0
        following_word_index = 0

        print("user text: ", self.userText)
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
        '''
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
    
    def pick_word_from_vector(self, objects, weights, k_sequence_pos_tag):
        weights = np.array(weights, dtype=np.float64)
        sum_of_weights = weights.sum()
        # standardization:
        np.multiply(weights, 1 / sum_of_weights, weights)
        # print("weight before: ", weights[-1])
        # weights = weights.cumsum()
        #print("weight after: ", weights[-1])
        print("weights: ", weights)
        print("weights type: ", type(weights))
        max_prob = float("-inf")
        best_word = ""
        for i in range(len(objects)):
            cur_word = objects[i]
            corpus_words_pos_tag = nltk.pos_tag([cur_word])[0][1]
            if corpus_words_pos_tag in k_sequence_pos_tag:
                if weights[0, i] > max_prob:
                    max_prob = weights[0, i]
                    best_word = cur_word
        
        print("best word: ", best_word)
        print("best prob: ", max_prob)
        return best_word

        
    
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
        k_sequence_tokens = nltk.word_tokenize(k_words_sequence)
        k_words_sequence_pos_tag  = nltk.pos_tag(k_sequence_tokens)
        print("k words sequence pos tag: ", k_words_sequence_pos_tag)
        k_words_sequence_pos_tag_list = [pos_tag[1] for pos_tag in k_words_sequence_pos_tag]
        print("k words sequence pos tag list: ", k_words_sequence_pos_tag_list)
    
        if k_words_sequence in self.corpus_k_words_index.keys(): 
            following_word_vector = self.transition_matrix_k_words[self.corpus_k_words_index[k_words_sequence]] + alpha

            transitionProb = following_word_vector / following_word_vector.sum()
            '''
            next_word = self.weighted_choice(self.distinct_words_in_corpus, transitionProb.toarray())
            next_word_pos_tag = self.corresponding_word_postag_dict[next_word]
            '''
            
            '''
            k_words_sequence_pos_tag = [self.corresponding_word_postag_dict[word] for word in k_words_sequence.split()]
            print("check k_words sequence: ", k_words_sequence)

            k_words_sequence_pos_tag_list = set.union(*k_words_sequence_pos_tag)
            print("k words sequence pos tag check : ", k_words_sequence_pos_tag_list)
            '''
            print("check k_words sequence: ", k_words_sequence)
            

            next_word = self.pick_word_from_vector(self.distinct_words_in_corpus, transitionProb.toarray(), k_words_sequence_pos_tag_list)
            # next_word_pos_tag = self.corresponding_word_postag_dict[next_word]
        else: 
            next_word = choice(self.distinct_words_in_corpus)
            if ' '.join(k_words_sequence_pos_tag_list) in self.pos_tag_following_dict.keys():
                while (nltk.pos_tag([next_word])[0][1] not in self.pos_tag_following_dict[' '.join(k_words_sequence_pos_tag_list)]):
                    print("possible following postag: ", self.pos_tag_following_dict[' '.join(k_words_sequence_pos_tag_list)])
                    next_word = choice(self.distinct_words_in_corpus)
        return next_word

    def markovChainGenerator(self, prev_k_words, num_of_words_to_generate):
        prev_k_words_sequence = prev_k_words.split(' ')

        if len(prev_k_words_sequence) != self.k_gram:
            raise ValueError(f'expect {self.k_gram} for the initial sequence')

        sentence = prev_k_words
    
        for i in range(num_of_words_to_generate): 
            '''
            new_prev_k_words = ""

            if ' '.join(prev_k_words_sequence) not in self.corpus_k_words_index.keys(): 
                print("k words not in corpus: ", ' '.join(prev_k_words_sequence))
                new_prev_k_words = choice(list(self.corpus_k_words_index.keys()))
                prev_k_words_sequence = new_prev_k_words.split(' ')
                print("new k words sequence", new_prev_k_words)
            '''
            sentence += ' '
            
            following_word = self.chooseWordFollowingKWords(' '.join(prev_k_words_sequence))
            print("following_word: ", following_word)
            sentence += following_word
            prev_k_words_sequence = prev_k_words_sequence[1:]+[following_word]
            
        return sentence
        
    def generateFromRandomStartSequence(self, num_of_words_to_generate): 
        first_k_words = np.random.choice(self.sets_of_k_words_in_corpus)

        while not first_k_words[0].isalpha():
            first_k_words = np.random.choice(self.sets_of_k_words_in_corpus)
        
        return self.markovChainGenerator(first_k_words, num_of_words_to_generate)