# **
# CMPU 365 - Jason Lee, Nhan Nguyen
# Code adapted from Luciano Strika - https://www.datastuff.tech/machine-learning/markov-chains-teaching-ai-to-write-game-of-thrones/

# Markov Chain n-gram model with user text input
# Add more weights to the words in the corpus which are also in the user text input
# **
from MarkovChain.markovChain import MarkovChain

from scipy.sparse import dok_matrix
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import words

class MarkovChainWithWeightedInput(MarkovChain):
    def __init__(self, userText, **kwds):
        self.userText = nltk.word_tokenize(userText)
        super().__init__(**kwds)
        
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
            for word in k_words:
                if word in self.userText:
                    countSimilarWord +=1
                    wordInUserText = True

            if wordInUserText: 
                # **
                # If word is in user input
                # Increment its frequency in the matrix by 10^(number of words in the k-word sequence that are also in user input)
                # **
                self.transition_matrix_k_words[k_words_sequence_index, following_word_index] += 10**(countSimilarWord)
            else: 
                self.transition_matrix_k_words[k_words_sequence_index, following_word_index] += 1
        

