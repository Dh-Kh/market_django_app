import enchant
from nltk.corpus import wordnet
is_real_word = enchant.Dict("en_USA")

def if_word_real(word):
    return bool(wordnet.synsets(word))
            
def make_suggestion(category_word):
    if if_word_real(category_word) == False:
        if is_real_word.check(category_word) == False:
            return is_real_word.suggest(category_word)
        
