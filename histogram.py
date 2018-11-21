from random import randint, choices

class FrequencyGram(dict):
    """ dict-like object for storing a probability distribution for a specific state """
    # Probably better practice to inherit from MutableMapping but then we'd have to rewrite all 5 of those methods
    # Could we also just have a property like self.dict and access it that way?
    def __init__(self, iterable=None):
        super(FrequencyGram, self)
        self.tokens = 0 # total for specific window, not entire model
        self.types = 0 # total for specific window, not entire model
        if iterable:
            self.update(iterable)
    
    def update(self, iterable):
        for item in iterable:
            if item in self:
                self[item] += 1
                self.tokens += 1
            else:
                self[item] = 1
                self.tokens += 1
                self.types += 1
    
    def count(self, item):
        if item in self:
            return self[item]
        return 0

    def return_rand_word(self):
        return self.keys()[randint(0, self.types - 1)]

    def return_weighted_rand_word(self):    
        weights = self.create_probability_distribution()
        return choices(list(self.keys()), weights)

    def create_probability_distribution(self):
        occurences = self.values()
        distribution = []
        total = sum(occurences)
        for occurence in occurences:
                distribution.append(occurence / total)
        return distribution