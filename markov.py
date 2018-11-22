from histogram import FrequencyGram
import re

ALPHABETS= "([A-Za-z])"
PREFIXES = "(Mr|St|Mrs|Ms|Dr)[.]"
SUFFIXES = "(Inc|Ltd|Jr|Sr|Co)"
STARTERS = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
ACRONYMS = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
WEBSITES = "[.](com|net|org|io|gov)"
PUNCS = ",'.?!:;"

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
    print(f"Corpus: {corpus_size} words (punctuation included)")
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
    print(sentence)
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
    current_word = generate_random_start(markov_model)
    sentences = []
    sentences.append(current_word)
    for i in range(0, length):
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
            sentences[i].capitalize()
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

training_set_1 = ["./fellowship_of_the_ring.txt", "./two_towers.txt", "./return_of_the_king.txt"]
training_set_2 = "./fellowship_of_the_ring.txt"
model_2 = load_data(training_set_2)

# test = generate_n_length_sentence(30, model_1)
# test = generate_n_sentences(3, model_1)
test2 = generate_n_length_sentence(30, model_2)
print(test2)