# **
# CMPU 365 - Jason Lee, Nhan Nguyen
# Program to interact with our LSTM and Markov Chain models
# ** 

from LSTM.LSTM_Inference import give_encouragement
import sys 
from MarkovChain.markovChainWithWeightedInput import MarkovChainWithWeightedInput

def markov_encouragement(input, n_gram): 
    markovChain = MarkovChainWithWeightedInput(n_gram = n_gram, userText = input)

    markovChain.populateCorpus('encouragement_comments.csv')
    markovChain.buildTransitionMatrix()

    return markovChain.generateFromRandomStartSequence(40)

while(True):
    print("")
    user_input = input("What's bothering you? Type 'exit' to quit\n")
    user_input = user_input.lower().strip() 
    if user_input== 'exit':
        break
    else:
        user_choice = input("Type 'lstm' to try LSTM, type 'markov' to try Markov Chain. Type 'exit' to quit \n") 
        user_choice = user_choice.lower().strip()
        while (user_choice != "lstm" and user_choice != "markov" and user_choice != "exit"):
            print("")
            print("Please try an acceptable input")
            user_choice = input("Type 'lstm' to try LSTM, type 'markov' to try Markov Chain. Type 'exit' to quit \n") 
            user_choice = user_choice.lower().strip()
        if user_choice == "lstm":
            print("LSTM output: ", give_encouragement(user_input))
        elif user_choice  == "markov": 
            user_n_gram = input("What n-gram model do you want to try? (2 for bi-gram, 3 for tri-gram, etc.)\n")
            print("Markov output: ", markov_encouragement(user_input, int(user_n_gram)))
        elif user_choice == 'exit':
            break