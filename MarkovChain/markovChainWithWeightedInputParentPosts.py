# **
# CMPU 365 - Jason Lee, Nhan Nguyen
# Code adapted from Luciano Strika - https://www.datastuff.tech/machine-learning/markov-chains-teaching-ai-to-write-game-of-thrones/
# 
# Markov Chain n-gram model with user text input
# Add more weights to the words in the corpus which are also in the user text input
# Also add more weights (but less than the aforementioned) to the words in the corpus (the comments) which are also in the parent posts
# **
import csv
from MarkovChain.markovChain import MarkovChain

from scipy.sparse import dok_matrix
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import words
from collections import Counter 
sys.path.append('..')
from helper import cleanText

class MarkovChainWithWeightedInputParentPosts(MarkovChain):
    def __init__(self, userText, **kwds):
        self.userText = nltk.word_tokenize(userText)
        self.parentPosts = ""
        self.wordsInParentPosts = []
        self.wordsInParentPostsCounter = Counter()
        super().__init__(**kwds)
        
    def populateCorpus(self, filepath):
        with open(filepath) as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                self.corpus+=row[0]
                self.parentPosts+=row[1]
        
        self.corpus = cleanText(self.corpus)

        for punctuation in ['.','-',',','!','?','(','—',')']:
            self.corpus = self.corpus.replace(punctuation, ' {0} '.format(punctuation))

        self.corpus_words = self.corpus.split(' ')

        self.corpus_words = [word for word in self.corpus_words if word != '']
    
        self.distinct_words_in_corpus = list(set(self.corpus_words))
        self.corpus_words_index = {word: index for index, word in enumerate(self.distinct_words_in_corpus)}
        self.distinct_words_in_corpus_count = len(self.distinct_words_in_corpus)

        self.wordsInParentPosts = self.parentPosts.split(' ')
        self.wordsInParentPostsCounter = Counter(self.wordsInParentPosts)   


    def buildTransitionMatrix(self):
        self.sets_of_k_words_in_corpus = [ ' '.join(self.corpus_words[i:i+self.k_prev]) for i, _ in enumerate(self.corpus_words[:-self.k_prev])]
        self.sets_of_k_words_count = len(list(set(self.sets_of_k_words_in_corpus)))

        self.transition_matrix_k_words = dok_matrix((self.sets_of_k_words_count, self.distinct_words_in_corpus_count))

        self.distinct_sets_of_k_words_in_corpus = list(set(self.sets_of_k_words_in_corpus))

        self.corpus_k_words_index = {word: index for index, word in enumerate(self.distinct_sets_of_k_words_in_corpus)}

        k_words_sequence_index = 0
        following_word_index = 0
        
        for index, k_words in enumerate(self.sets_of_k_words_in_corpus[:-self.k_prev]):
            k_words_sequence_index = self.corpus_k_words_index[k_words]
            following_word_index = self.corpus_words_index[self.corpus_words[index+self.k_prev]]            
            wordInUserText = False
            countSimilarWord = 0

            countWordInParentPosts = 0
            for word in k_words:
                if word in self.userText:
                    countSimilarWord +=1
                    wordInUserText = True
                if word in self.wordsInParentPostsCounter.keys():
                    countWordInParentPosts +=1
              
            if wordInUserText:
                self.transition_matrix_k_words[k_words_sequence_index, following_word_index] += 10**(countSimilarWord) + 10*(countWordInParentPosts)
            else: 
                self.transition_matrix_k_words[k_words_sequence_index, following_word_index] += 10*(countWordInParentPosts) if countWordInParentPosts > 0 else 1
        

