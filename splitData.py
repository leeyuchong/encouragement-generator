# **
# Split the posts and comments in the data sets by sentences
# So that the least words will be truncated by the LTSM's input layer while still maintain meaning from sentences
# **

import csv
import numpy as np
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize, word_tokenize
import math
import string
import random

def splitPosts(inputFileName, outputFileName, maxNumOfWords):
    with open(inputFileName) as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',')
        count = 0

        wordsLengthTotal = 0
        sentencesLengthToTal = 0
        countPosts = 0

        outputFile = open(outputFileName, 'w', newline='') 
        writer = csv.writer(outputFile)

        for row in csvReader:
            post = row[1]
            comment = row[0]
            if "I'm a bot" in comment: 
                continue
        
            commentASCII = comment.encode(encoding='ascii', errors='ignore').decode()
            words_in_post = nltk.word_tokenize(post)
            sentencesInPost = sent_tokenize(post)
            numOfSentences = len(sentencesInPost)

            wordsLengthTotal += len(words_in_post)
            sentencesLengthToTal += len(sentencesInPost)
        
            numOfSplitPosts = math.ceil(len(words_in_post)/maxNumOfWords)

            if numOfSplitPosts > 1: 
                splittedPostsArray = np.array_split(sentencesInPost, numOfSplitPosts)

                for splittedPost in splittedPostsArray: 
                    newPost = "".join(" "+sentence if not sentence[0].startswith("'") and sentence[0] not in string.punctuation else sentence for sentence in splittedPost).strip()
                    
                    if (len(nltk.word_tokenize(newPost)) > maxNumOfWords):
                        sumWords = 0
                        extraPosts = []

                        for sentence in splittedPost:
                            sumWords += len(nltk.word_tokenize(sentence))
                            if sumWords > maxNumOfWords:
                                newExtraPost = "".join(" "+sentence if not sentence[0].startswith("'") and sentence[0] not in string.punctuation else sentence for sentence in extraPosts).strip()
                                
                                extraPosts = []
                                sumWords = 0
                                newExtraPostASCII = newExtraPost.encode(encoding='ascii', errors='ignore').decode()
                                writer.writerow([commentASCII, newExtraPostASCII])  
                            extraPosts.append(sentence)
                        
                        newExtraPost = "".join(" "+sentence if not sentence[0].startswith("'") and sentence[0] not in string.punctuation else sentence for sentence in extraPosts).strip()
                        newExtraPostASCII = newExtraPost.encode(encoding='ascii', errors='ignore').decode()
                        writer.writerow([commentASCII, newExtraPostASCII]) 
                        
                    else: 
                        newPostASCII = newPost.encode(encoding='ascii', errors='ignore').decode()
                        writer.writerow([commentASCII, newPostASCII])

            else: 
                postASCII = post.encode(encoding='ascii', errors='ignore').decode()
                writer.writerow([commentASCII, postASCII])
        
        outputFile.close()

def splitComments(inputFileName, outputFileName, maxNumOfWords):
    with open(inputFileName) as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',')
        count = 0

        wordsLengthTotal = 0
        sentencesLengthToTal = 0
        countPosts = 0

        outputFile = open(outputFileName, 'w', newline='') 
        writer = csv.writer(outputFile)
        for row in csvReader:
            post = row[1]
            comment = row[0]

            postASCII = post.encode(encoding='ascii', errors='ignore').decode()
            
            words_in_comment = nltk.word_tokenize(comment)
            sentencesInComment = sent_tokenize(comment)
            numOfSentences = len(sentencesInComment)

            numOfSplitComments = math.floor(len(words_in_comment)/maxNumOfWords)

            if numOfSplitComments > 1: 
                splittedCommentsArray = np.array_split(sentencesInComment, numOfSplitComments)

                for splittedComment in splittedCommentsArray: 
                    newComment = "".join(" "+sentence if not sentence[0].startswith("'") and sentence[0] not in string.punctuation else sentence for sentence in splittedComment).strip()

                    if (len(nltk.word_tokenize(newComment)) > maxNumOfWords):
                        
                        sumWords = 0
                        extraComments = []
                        lastSentence = ''
                        for sentence in splittedComment:
            
                            sumWords += len(nltk.word_tokenize(sentence))
                            if sumWords > maxNumOfWords:
                                newExtraComment = "".join(" "+sentence if not sentence[0].startswith("'") and sentence[0] not in string.punctuation else sentence for sentence in extraComments).strip()
                                extraComments = []
                                sumWords = 0
                                newExtraCommentASCII = newExtraComment.encode(encoding='ascii', errors='ignore').decode()
                                writer.writerow([newExtraCommentASCII, postASCII])  
                            lastSentence = sentence
                            extraComments.append(sentence)
                            
                        newExtraComment = "".join(" "+sentence if not sentence[0].startswith("'") and sentence[0] not in string.punctuation else sentence for sentence in extraComments).strip()
                        newExtraCommentASCII = newExtraComment.encode(encoding='ascii', errors='ignore').decode()
                        writer.writerow([newExtraCommentASCII, postASCII]) 

                    else: 
                        newCommentASCII = newComment.encode(encoding='ascii', errors='ignore').decode()
                        writer.writerow([newCommentASCII, postASCII])

            else: 
                commentASCII = comment.encode(encoding='ascii', errors='ignore').decode()
                writer.writerow([commentASCII, postASCII])
        outputFile.close()

def shuffle(inputFileName, outputFileName):
     with open(inputFileName) as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',')
        
        outputFile = open(outputFileName, 'w', newline='') 
        writer = csv.writer(outputFile)

        rows = []
        for row in csvReader:
            rows.append(row)
        
        random.shuffle(rows)

        for row in rows: 
            post = row[1]

            postASCII = post.encode(encoding='ascii', errors='ignore').decode()
            commentASCII = comment.encode(encoding='ascii', errors='ignore').decode()
            writer.writerow([commentASCII, postASCII])
            
        outputFile.close()

splitPosts("encouragement_comments.csv", "splitted_posts.csv", 200)
splitComments("splitted_posts.csv", "splitted_comments.csv", 60)

shuffle("splitted_comments.csv", "splitted_data_2.csv")
