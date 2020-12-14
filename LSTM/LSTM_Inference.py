# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# <h1>LSTM Inference Model for Encouragement Generator</h1>
# CMPU 365
# Jason Lee, Nhan Nguyen
# 
# We have consulted and adapted code from the following sources in the making of this model: 
# - https://stackabuse.com/python-for-nlp-neural-machine-translation-with-seq2seq-in-keras/
# - https://keras.io/examples/nlp/lstm_seq2seq/#run-inference-sampling
# - https://towardsdatascience.com/word-level-english-to-marathi-neural-machine-translation-using-seq2seq-encoder-decoder-lstm-model-1a913f2dc4a7
# 
# We converted the one-hot model from the sources above to include a word embedding output. 

# %%
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
import numpy as np
from keras.models import Model, load_model
from keras.layers import Input
from keras.losses import cosine_similarity
from keras.preprocessing.sequence import pad_sequences
import csv
from LSTM.CleanText import clean_text
import math


# %%
decoder_method = "one-hot" #embed
# Use "embed" for word embedding output

# %% [markdown]
# <h3>Load constants</h3>

# %%
start_char = "<START>"
end_char = "<END>"
post_len = 251
comment_len = 116
word_to_index = {}
with open("LSTM/word_to_index.csv", 'r', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader) # toss headers
    for word, index in csvreader:
        word_to_index.setdefault(word, int(index))
index_to_word = {v:k for k,v in word_to_index.items()}

# Load the relevant embedding matrix
embeddings_file_name = "LSTM/embeddings_tokenized_one-hot.npy" if decoder_method == "one-hot" else "LSTM/embeddings_tokenized_embed.npy"
with open(embeddings_file_name, "rb") as embeddings_file:
    embeddings_tokenized = np.load(embeddings_file)

# %% [markdown]
# <h3>Construct Inference Model</h3>

# %%
model_name = "LSTM/One-Hot_Model" if decoder_method == "one-hot" else "LSTM/Embed_Model"
model = load_model(model_name)
# Get the latent_dim from the model
latent_dim = model.layers[4].output[0].shape[1]

# Create encoder
encoder_inputs = model.input[0] #input_1
encoder_outputs, state_h_enc, state_c_enc = model.layers[4].output  # lstm_1
encoder_states = [state_h_enc, state_c_enc]
encoder_model = Model(encoder_inputs, encoder_states)

# Create decoder
decoder_inputs = Input(shape=(1,))  # input_2
decoder_state_input_h = Input(shape=(latent_dim,), name="input_3")
decoder_state_input_c = Input(shape=(latent_dim,), name="input_4")
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
dec_emb_layer = model.layers[3]
dec_emb = dec_emb_layer(decoder_inputs)
decoder_lstm = model.layers[5]
decoder_outputs, state_h_dec, state_c_dec = decoder_lstm(
    dec_emb, initial_state=decoder_states_inputs
)
decoder_states = [state_h_dec, state_c_dec]
decoder_dense = model.layers[6]
decoder_outputs = decoder_dense(decoder_outputs)
decoder_model = Model(
    [decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states
)


# %%
def give_encouragement(input_text):
    """
    Use the model to produce output given an input sequence
    Input: input_text, input that the model will generate text for
    Output: a string representing the output of the model 
    """
    # Convert string to padded sequence of integers
    input_sequence = clean_text(input_text)
    input_sequence = [word_to_index[x] for x in input_sequence]
    input_sequence = pad_sequences([input_sequence], maxlen=post_len, truncating='post')
    # Get internal state of encoder
    states_value = encoder_model.predict(input_sequence)
    target_seq = np.zeros((1,1))
    # Start output with the start symbol
    target_seq[0, 0] = word_to_index[start_char]
    stop_condition = False
    output = ""
    while not stop_condition:
        output_tokens, h_state, c_state = decoder_model.predict([target_seq] + states_value)
        
        sampled_word = ""
        sampled_token_index = 0
        if decoder_method == "one-hot":
            sampled_token_index = np.argmax(output_tokens[0, -1, :])
            sampled_word = index_to_word[sampled_token_index]
        else:
            similarity = math.inf
            for i in range(embeddings_tokenized.shape[0]):
                # Find closest word vector
                new_sim = cosine_similarity(embeddings_tokenized[i:i+1].astype('float32'), output_tokens[0, 0].astype('float32'), axis=-1)
                if new_sim < similarity:
                    similarity = new_sim
                    sampled_token_index = i
            sampled_word = index_to_word[sampled_token_index]
        if (sampled_word==end_char or len(output)>comment_len):
            stop_condition = True
        else:
            output += ' '+sampled_word
        # Reset target_seq, pass current states forward
        target_seq = np.zeros((1,1))
        target_seq[0, 0] = sampled_token_index
        states_value = [h_state, c_state]
    return output


