'''
from markovChain import MarkovChain

markovChain = MarkovChain(3)

markovChain.populateCorpus('encouragement_comments.csv')
markovChain.buildTransitionMatrix()
markovChain.buildPosTagFollowingDict()

ret = markovChain.generateFromRandomStartSequence(50)
print(ret)
'''
import nltk

from nltk.tokenize import word_tokenize
from nltk.corpus import words


from markovChainWithInputText import MarkovChain
'''
userText = "Hi, would you kindly give me some encouragement? This decade has been a stretch of disaster. I need the will to keep going but don't know how."
markovChain = MarkovChain(3, userText)

markovChain.populateCorpus('encouragement_comments.csv')
markovChain.buildTransitionMatrix()
markovChain.buildPosTagFollowingDict()

ret = markovChain.generateFromRandomStartSequence(40)
print(ret)


'''
'''
from markovChainWithInput2 import MarkovChain

userText = "I've taken on a 3-year university course that is said to be really tough, but it's something I'm truly interested in. The thing about this university is that there is no project work, no presentation or participation points to help my grade- EVERYTHING is based on the results of a year-end exam. Last year, I failed ALL my modules and had to resit them, which makes me one year behind. This year, I managed to clear two of my toughest modules, but I failed the other two, which means that I now will take 5 years to graduate.My parents and friends are telling me not to beat myself up over it, but I can't help but feel so, so disappointed that I did not pass everything. I had such expectations for myself too.I guess I really feel insecure about graduating a lot later than everyone else I know. I feel really depressed that I can't do well in something that I like."
markovChain = MarkovChain(1, userText)

markovChain.populateCorpus('encouragement_comments.csv')
markovChain.buildTransitionMatrix()
# markovChain.buildPosTagFollowingDict()

ret = markovChain.generateFromRandomStartSequence(40)
print(ret)
'''

print(nltk.help.upenn_tagset('RB'))
'''
word = 'do'
print(nltk.pos_tag([word])[0][1])
'''