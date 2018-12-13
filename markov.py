from histogram import FrequencyGram
import re
import sys
import json
import os.path


## MAIN TO DO:
    ## COMMAND LINE ARGS are str
    ## how can we verify that the second arg is an int?
    ## can we do some kind of ASCII logic like we would do in C? 


def main():
## read args, determine if valid (sentence 30 // sentences 3)
## we probably want to do some kind of checking and saving of our model so we're not uncessarily training,
## check if file exists, if not, training, if so, use that instead
## print sentences, return true
    if valid_args(sys.argv):
        if not existing_model():
            model = load_data(TRAINING_DATA)
        else:
            model = load_model()
        OPTIONS[sys.argv[1]](sys.argv[2], model)
        return True
    else:
        print_usage()
        return False

def valid_args(args):
    print(len(args))
    print(args[1])
    print(isinstance(args[2], str))
    ## FILE_NAME <sentence(s)> <int>
    if len(args) > 3:
        if args[1] == "sentence" or args[1] == "sentences":
            if isinstance(args[2], int) and args[2] > 0:
                return True
    return False

def print_usage():
    print("Usage:")
    print("    sentence <int>  | sentence of <int> length")
    print("    sentences <int> | <int> # of sentences")

def existing_model():
    return os.path.isfile(MODEL_NAME)

def save_model(markov_model):
    with open('model.json', 'w') as f:
        json.dump(markov_model, f, indent=4)
    return True

def load_model():
    with open('model.json', 'r') as f:
        model = json.load(f)
    return model

def make_markov_model(corpus):
    markov_model = dict()
    corpus_size = 0
    for sentence in corpus:
        if "START" in markov_model:
            markov_model["START"].update(sentence[0])
        else:
            markov_model["START"] = FrequencyGram(sentence[0])

        if sentence[-1] in markov_model: #have to make it manually point to END
                markov_model[sentence[-1]].update("END")
        else:
            markov_model[sentence[-1]] = FrequencyGram("END")
        corpus_size += len(sentence)
        for i in range(0, len(sentence)-1): ## minus two because all sentence terminators point to END
                # Note, we might need to update this or the .update func
                # depending how we want it to parse the data
            if sentence[i] in markov_model:
                markov_model[sentence[i]].update(sentence[i+1])
            else:
                markov_model[sentence[i]] = FrequencyGram(sentence[i+1])

    markov_model["END"] = FrequencyGram("START") ## Since we're adding in START/END has we iterate instead of having it in the raw data,
                                                 ## we have to manually add a FrequencyGram at key END to ensure our sentences flow
    print("Corpus: {0} words".format(corpus_size))
    if save_model(markov_model):
        print("Model saved!")
    else:
        print("An error occurred saving your model")
    return markov_model

def load_data(file_path):
    """ Open and format data from file_path(s), returns a trained markov model """
    if isinstance(file_path, list):
        for path in file_path:
            corpus = []
            raw_data = get_data(path)
            corpus += split_into_sentences(raw_data)
        markov_model = make_markov_model(corpus)
    else:
        raw_data = get_data(file_path)
        corpus = split_into_sentences(raw_data)
        markov_model = make_markov_model(corpus)
    return markov_model
    ## here is where we can save the model


def generate_random_start(markov_model):
    sentence_starter = markov_model["START"].return_weighted_rand_word()
    return sentence_starter

def generate_n_length_sentence(length, markov_model):
    current_word = generate_random_start(markov_model)
    sentence = [current_word]
    for i in range(0, length):
        current_frequencygram = markov_model[current_word]
        next_word = current_frequencygram.return_weighted_rand_word()
        current_word = next_word
        if current_word == "START" or current_word == "END":
            continue
        sentence.append(current_word)
    return format_text(sentence)

def format_text(sentence_list):
    formatted = ""
    for i in range(0, len(sentence_list)):
        if sentence_list[i] not in PUNCS:
            formatted += sentence_list[i] + " "
        elif sentence_list[i] in PUNCS and i == 0:
            formatted += sentence_list[i]
        else:
            formatted = formatted[:-1] + sentence_list[i] + " "
    return formatted

def generate_n_sentences(length, markov_model):
    sentences = ["" for x in range(length)]
    for i in range(0, length):
        current_word = generate_random_start(markov_model)
        sentences[i] += (current_word)
        while True:
            current_frequencygram = markov_model[current_word]
            next_word = current_frequencygram.return_weighted_rand_word()
            if next_word == "END":
                break
            current_word = next_word
            if current_word not in PUNCS:
                sentences[i] += " " + current_word
            else:
                sentences[i] += current_word
    return " ".join(sentences)

def get_data(path):
    with open(path) as file:
        data = file.read()
    file.close()
    return data

# D Greenburg // split_into_sentences
# https://stackoverflow.com/questions/4576077/python-split-text-on-sentences

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n","").replace("\r", "")
    text = re.sub(' +',' ',text)
    text = re.sub(PREFIXES,"\\1<prd>",text)
    text = re.sub(WEBSITES,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + ALPHABETS + "[.] "," \\1<prd> ",text)
    text = re.sub(ACRONYMS+" "+STARTERS,"\\1<stop> \\2",text)
    text = re.sub(ALPHABETS + "[.]" + ALPHABETS + "[.]" + ALPHABETS + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(ALPHABETS + "[.]" + ALPHABETS + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+SUFFIXES+"[.] "+STARTERS," \\1<stop> \\2",text)
    text = re.sub(" "+SUFFIXES+"[.]"," \\1<prd>",text)
    text = re.sub(" " + ALPHABETS + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    ## Added line to split sentence lists into lists of words/punctuation
    # sentences = [ re.findall(r"[\w]+|[^\s\w]", sentence) for sentence in text ]
    for i in range(0, len(sentences)):
        sentences[i] = re.findall(r"[\w']+|[.,!?;]", sentences[i])
    return sentences

# training_set_1 = ["./fellowship_of_the_ring.txt", "./two_towers.txt", "./return_of_the_king.txt"]
# training_set_2 = "./training_data/fellowship_of_the_ring.txt"
# model_2 = load_data(training_set_2)

# # test = generate_n_length_sentence(30, model_1)
# test = generate_n_sentences(5, model_2)
# test2 = generate_n_length_sentence(30, model_2)
# print(test)

if __name__ == "__main__":
    main()


ALPHABETS= "([A-Za-z])"
PREFIXES = "(Mr|St|Mrs|Ms|Dr)[.]"
SUFFIXES = "(Inc|Ltd|Jr|Sr|Co)"
STARTERS = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
ACRONYMS = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
WEBSITES = "[.](com|net|org|io|gov)"
PUNCS = ",'.?!:;"

MODEL_NAME = "model.json"
TRAINING_DATA = ["./training_data/fellowship_of_the_ring.txt", "./training_data/two_towers.txt", "./training_data/return_of_the_king.txt"]
OPTIONS = { "sentence": generate_n_length_sentence,
            "sentences": generate_n_sentences }