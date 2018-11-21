from histogram import FrequencyGram
import re

ALPHABETS= "([A-Za-z])"
PREFIXES = "(Mr|St|Mrs|Ms|Dr)[.]"
SUFFIXES = "(Inc|Ltd|Jr|Sr|Co)"
STARTERS = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
ACRONYMS = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
WEBSITES = "[.](com|net|org|io|gov)"

def make_markov_model(data):
    markov_model = dict()

    for sentence in data:
        for i in range(0, len(sentence)-1):
            if data[i] in markov_model:
                # Note, we might need to update this or the .update func
                # depending how we want it to parse the data
                markov_model[data[i]].update(data[i+1])
            else:
                markov_model[data[i]] = FrequencyGram(data[i+1])
    return markov_model


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
    sentences = [ re.findall(r"[\w]+|[^\s\w]", sentence) for sentence in test2 ]
    return sentences

test = get_data("./fellowship_of_the_ring.txt")


test2 = split_into_sentences(test)

test3 = [ re.findall(r"[\w]+|[^\s\w]", sentence) for sentence in test2 ]


print(test3)


# print(test2)
# TO-DO:
## - generate_random_start
##- generate_n_length_sentence
## data parser:
    # we probably want to remove all quotes, single and double
    # - reads line by line, putting all 