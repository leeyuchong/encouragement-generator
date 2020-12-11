import csv
import numpy as np
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize, word_tokenize
import math
import string
import random
'''
with open('encouragement_comments.csv') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',')
    count = 0

    wordsLengthTotal = 0
    sentencesLengthToTal = 0
    countPosts = 0

    outputFile = open("splitted_posts.csv", 'w', newline='') 
    writer = csv.writer(outputFile)
    writer.writerow(["Comment", "Parent Post"])

    for row in csvReader:
        post = row[1]
        comment = row[0]
        commentASCII = comment.encode(encoding='ascii', errors='ignore').decode()
        words_in_post = nltk.word_tokenize(post)
        sentencesInPost = sent_tokenize(post)
        numOfSentences = len(sentencesInPost)

        wordsLengthTotal += len(words_in_post)
        sentencesLengthToTal += len(sentencesInPost)
     
        numOfSplitPosts = math.floor(len(words_in_post)/200)
        if numOfSplitPosts > 1: 
            splittedPostsArray = np.array_split(sentencesInPost, numOfSplitPosts)
            print("split posts array: ", splittedPostsArray)

            for splittedPost in splittedPostsArray: 
                print("slittedPost: ", splittedPost)
                newPost = "".join(" "+sentence if not sentence[0].startswith("'") and sentence[0] not in string.punctuation else sentence for sentence in splittedPost).strip()
                newPostASCII = newPost.encode(encoding='ascii', errors='ignore').decode()
                writer.writerow([commentASCII, newPostASCII])

        else: 
            postASCII = post.encode(encoding='ascii', errors='ignore').decode()
            writer.writerow([commentASCII, postASCII])
    
    outputFile.close()
'''
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
                print("check bot")
                continue
        
            commentASCII = comment.encode(encoding='ascii', errors='ignore').decode()
            words_in_post = nltk.word_tokenize(post)
            sentencesInPost = sent_tokenize(post)
            numOfSentences = len(sentencesInPost)

            wordsLengthTotal += len(words_in_post)
            sentencesLengthToTal += len(sentencesInPost)
        
            numOfSplitPosts = math.floor(len(words_in_post)/maxNumOfWords)

            if numOfSplitPosts > 1: 
                splittedPostsArray = np.array_split(sentencesInPost, numOfSplitPosts)
                print("split posts array: ", splittedPostsArray)

                for splittedPost in splittedPostsArray: 
                    print("slittedPost: ", splittedPost)
                    newPost = "".join(" "+sentence if not sentence[0].startswith("'") and sentence[0] not in string.punctuation else sentence for sentence in splittedPost).strip()
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
                print("split comments array: ", splittedCommentsArray)

                for splittedComment in splittedCommentsArray: 
                    print("splittedComment: ", splittedComment)
                    newComment = "".join(" "+sentence if not sentence[0].startswith("'") and sentence[0] not in string.punctuation else sentence for sentence in splittedComment).strip()
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
            comment = row[0]

            postASCII = post.encode(encoding='ascii', errors='ignore').decode()
            commentASCII = comment.encode(encoding='ascii', errors='ignore').decode()
            writer.writerow([commentASCII, postASCII])
        
        outputFile.close()

splitPosts("encouragement_comments.csv", "splitted_posts.csv", 200)
splitComments("splitted_posts.csv", "splitted_comments.csv", 90)

shuffle("splitted_comments.csv", "splitted_data.csv")

'''    
for i in range (1, numOfSplitPosts):
    new_post = sentencesInPost[math.ceil(numOfSentences/2):]

if len(words_in_post) > 200: 
    old_post = sentencesInPost[:math.ceil(numOfSentences/2)]
    new_post = sentencesInPost[math.ceil(numOfSentences/2):]
    print("new_post: ", new_post)
    newPostStr = "".join(" "+sentence if not sentence[0].startswith("'") and sentence[0] not in string.punctuation else sentence for sentence in sentencesInPost).strip()
    print("new_post string: ", newPostStr)
print("")   
countPosts += 1
'''
'''    
print("avg words: ", wordsLengthTotal / countPosts)
print("avg sentences: ", sentencesLengthToTal / countPosts)

print("count: ", count)
'''
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
