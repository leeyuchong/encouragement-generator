import re
import string

def cleanText(text):
    '''Clean text by removing unnecessary characters and altering the format of words.'''

    text = text.lower()
    
    text = text.replace("i'm", "i am")
    # text = re.sub(r"i'm", "i am", text)
    text = text.replace("he's", "he is")
    text = text.replace("she's", "she is")
    text = text.replace("it's", "it is")
    text = text.replace("what's", "that is")
    text = text.replace("that's", "that is")
    text = text.replace("where's", "where is")
    text = text.replace("how's", "how is")
    text = text.replace("\'ll", " will")
    text = text.replace("\'re", " are")
    text = text.replace("\'ve", " have")
    text = text.replace("\'d", " would")
    text = text.replace("won't", "will not")
    text = text.replace("can't", "cannot")
    text = text.replace("n't", " not")
    text = text.replace("n'", "ng")
    text = text.replace("'bout", "about")
    text = text.replace("'til", "until")
    text = re.sub(' +', ' ', text)
    # if text != ":)" or text != ":(":
    #     text = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
    
    return text
