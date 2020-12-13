import re
import string

def clean_text(text):
    '''
    Helper method to convert text to lower-case and remove contractions and uncommon punctuations. 
    Input: text, a string to be cleaned
    Output: the cleaned text
    '''

    text = text.lower()
    text = text.replace("i'm", "i am")
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
    # Keep the sad or happy emoji
    if text != ":)" or text != ":(": 
        text = re.sub(r"[-()\"#/@;:<>{}`+=~|]", "", text)
    # Split the text by words and punctuation
    text = re.findall(r"[\w']+|[.,!?;]", text)
    text = [x.strip() for x in text]
    return text
