from LSTM_Inference import give_encouragement

while(True):
    user_input = input("What's bothering you? Type 'exit' to quit")
    if user_input.lower().strip() == 'exit':
        break
    else:
        print("LSTM output: ", give_encouragement(user_input))
