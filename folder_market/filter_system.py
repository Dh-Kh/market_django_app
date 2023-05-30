from spellchecker import SpellChecker
from nltk.corpus import wordnet

spell = SpellChecker()

def if_word_real(word):
    return bool(wordnet.synsets(word))

def make_suggestion(category_word):
    if if_word_real(category_word) == False:
        if category_word not in spell:
            return spell.correction(category_word)
        
