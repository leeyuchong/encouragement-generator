import csv
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize, word_tokenize


with open('encouragement_comments.csv') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',')
    count = 0

    wordsLengthTotal = 0
    sentencesLengthToTal = 0
    countPosts = 0
    for row in csvReader:
        post = row[1]
        words_in_post = nltk.word_tokenize(post)
        sentencesInPost = sent_tokenize(post)
        numOfSentences = len(sentencesInPost)

        wordsLengthTotal += len(words_in_post)
        sentencesLengthToTal += len(sentencesInPost)
        print(post)
        print(sentencesInPost)
        if len(words_in_post) > 200: 
            new_post = sentencesInPost[math.floor(numOfSentences/2):]
            print("new_post: ", new_post)

        print("")
        countPosts += 1
        
    print("avg words: ", wordsLengthTotal / countPosts)
    print("avg sentences: ", sentencesLengthToTal / countPosts)
    
    print("count: ", count)
    '''
    if len(words_in_post) > 200: 
        count += 1
    '''
    '''
    print(post)
    sentencesInPost = sent_tokenize(post)
    print(sentencesInPost)
    print("")
    '''