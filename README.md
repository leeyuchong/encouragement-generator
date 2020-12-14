interact.py: program to interact with our 2 models: LSTM and Markov Chain (by running 'python3 interact.py')

splitData.py: split the posts and comments in our data set so as not to be truncated by the input layer of the LSTM model

parser.py: scrap the posts and comments from r/encouragements and create our data set in .csv file

sampleOutput: using the last 10% of the parent posts in our data set to generate sample responses from the LSTM and Markov Chain model

In ./LSTM:
Embed_Model: Trained model for the regression model
One-Hot_Model: Trained model for the classification mdodel
embeddings_tokenized_embed.npy: Tokenized embedding layer for the regression model
embeddings_tokenized_embed.npy: Tokenized embedding layer for the regression model
LSTM_Inference.ipynb: Jupyter Notebook for doing inference on a loaded model
LSTM_Inference.py: Python script version of the Jupyter notebook of the same name for use in interact.py
LSTM_Model.ipynb: Jupyter Notebook for training the model. 

In the the files LSTM_Inference.ipynb, LSTM_Inference.py, LSTM_Model, there is a variable for decoder_method. Set the value to "one-hot" to use the classification model, and to "embed" for the regression model. 

In ./MarkovChain:
markovChain.py: most basic n-gram model, generate random response
markovChainWithWeightedInput.py: n-gram model with the words' weights adjusted based on user input (seemlingly working best)
markovChainWithWeightedInputParentPosts.py: n-gram model with the words' weights adjusted based on the parent posts in the data set and the user input
markovChainWithInputPostag.py: basic n-gram model generating a look-up table of suitable postags for each new word generated (not useful)

------------------------------------------------------------------------------------------------------------------------------
Work Distribution: 
- Jason Lee: mainly LSTM model, parsing from r/encouragemenets to the .csv file
- Nhan Nguyen: mainly Markov Chain model, splitting data, sample outputs