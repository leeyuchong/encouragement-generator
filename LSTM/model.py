import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
import csv

#samples is a list consisting of tuples (comment, parent)
samples = []
comments = []
posts = []

with open('../encouragement_comments.csv', 'r', newline='') as csv_file:
    textReader = csv.reader(csv_file)
    for row in textReader:
        # samples.append((row[0], row[1]))
        comments.append(row[0])
        posts.append(row[1])
# print(samples)
vectorizer = TextVectorization(max_tokens=20000, output_sequence_length=200)
text_ds = tf.data.Dataset.from_tensor_slices(comments).batch(128)
vectorizer.adapt(text_ds)
print(vectorizer.get_vocabulary()[:5])
output = vectorizer([["the cat sat on the mat"]])
print(output.numpy()[0, :6])

embeddings_index = {}
with open(path_to_glove_file) as f:
    for line in f:
        word, coefs = line.split(maxsplit=1)
        coefs = np.fromstring(coefs, "f", sep=" ")
        embeddings_index[word] = coefs

print("Found %s word vectors." % len(embeddings_index))