from histogram import FrequencyGram
def make_markov_model(data):
    markov_model = dict()

    for i in range(0, len(data)-1):
        if data[i] in markov_model:
            # Note, we might need to update this or the .update func
            # depending how we want it to parse the data
            markov_model[data[i]].update(data[i+1])
        else:
            markov_model[data[i]] = FrequencyGram(data[i+1])
    return markov_model

