from textSimilarity import embed 
import numpy as np
import csv


parentPosts = []
with open('encouragement_comments.csv') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                parentPosts.append(row[1])
        
print("parent posts: ", parentPosts)

print("len parentPosts: ", len(parentPosts))

count = 0
for i in range(0, len(parentPosts) - 2):
    for j in range (i+1, len(parentPosts) - 1):
        if parentPosts[j] == parentPosts[i]: 
            countDup += 1
            print("duplicate count: ", countDup)
            parentPosts.pop(j)
        else:
            if np.inner(embed(parentPosts)[i], embed(parentPosts)[j]) > 0.5: 
                count +=1
                print(count)

# print("count: ", count)
'''
print("checkpoint")
print("check: ", np.inner(embed(messages)[1], embed(messages)[1]))
'''
'''
list = [2,3,4,5]

for i in range(0,len(list)-1): 
    if (list[i] - 1 < 3):
        list.pop(i)
print(list)
'''