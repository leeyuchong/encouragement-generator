# **
# Generate sample outputs from the LSTM model as well as Markov Chain
# using the last 10% of the parent posts in our data set.
# **
import csv
from LSTM.LSTM_Inference import give_encouragement
from MarkovChain.markovChainWithWeightedInput import MarkovChainWithWeightedInput

def markov_encouragement(input): 
    markovChain = MarkovChainWithWeightedInput(n_gram = 4, userText = input)

    markovChain.populateCorpus('encouragement_comments.csv')
    markovChain.buildTransitionMatrix()

    return markovChain.generateFromRandomStartSequence(40)

with open("splitted_data_3.csv") as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',')
    sampleInputs = []     
    start_index = 3790-301 # row_count("splitted_data_3.csv") - 300 - 1
    index = 0
    for row in csvReader:
        if index >= start_index:
            sampleInput = row[1]
           
            if sampleInput not in sampleInputs: 
                sampleInputs.append(sampleInput)
        index += 1

    outputFile = open("sampleOutputs.csv", 'w', newline='')
    writer = csv.writer(outputFile)
    writer.writerow(["Input", "LSTM Output", "Markov Chain Output"])
    for sampleInput in sampleInputs: 
        lstmOutput = give_encouragement(sampleInput)
        markovOutput = markov_encouragement(sampleInput)
        print("LSTM output: ", lstmOutput)
        print("markov output: ", markovOutput)
        print("")
        lstmOutputASCII =  lstmOutput.encode(encoding='ascii', errors='ignore').decode()
        markovOutputASCII = markovOutput.encode(encoding='ascii', errors='ignore').decode()

        sampleInputASCII = sampleInput.encode(encoding='ascii', errors='ignore').decode()

        writer.writerow([sampleInputASCII, lstmOutputASCII, markovOutputASCII])

    outputFile.close()