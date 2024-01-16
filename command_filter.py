import nltk
from nltk.corpus import stopwords
from nltk.parse.generate import generate
#parse commands and filter them, removing unnecessary words
import json

# from nltk.parse.generate import generate

grammar = nltk.CFG.fromstring("""
    S -> NP VP
    VP -> V NP | V NP PP
    PP -> P NP
    V -> "saw" | "ate" | "walked"
    NP -> "John" | "Mary" | "Bob" | Det N | Det N PP
    Det -> "a" | "an" | "the" | "my"
    N -> "man" | "dog" | "cat" | "telescope" | "park"
    P -> "in" | "on" | "by" | "with"
    """)

grammar_names = nltk.PCFG.fromstring(""" 
    S -> nameStart nameMiddle0to2 nameEnd [1]
    nameMiddle0to2 -> "" [.30]| nameMiddle [.30]| nameMiddle nameMiddle [.40]
    nameStart -> nsCons nmVowel [.75]| nsVowel [.25]
    nameMiddle -> nmCons nmVowel [1]
    nameEnd -> neCons neVowel [.35]| neCons [.65]
    nsCons -> "J" [.1]|"M" [.1]| "P" [.1]| "N" [.1]| "Y" [.1]| "D" [.1]| "F" [.1]| "H" [.1]| "V" [.1]| "Z" [.1]
    nmCons -> "l" [.0625]| "m" [.0625]| "lm" [.0625]| "th" [.0625]| "r" [.0625]| "s" [.0625]| "ss" [.0625]| "p" [.0625]| "f" [.0625]| "mb" [.0625]| "b" [.0625]| "lb" [.0625]| "d" [.0625]| "lf" [.0625]| "kl" [.0625]| "tr" [.0625]
    neCons -> "r" [.09]| "n" [.09]| "m" [.09]| "s" [.09]| "y" [.09]| "l" [.1]| "th" [.09]| "b" [.09]| "lb" [.09]| "f" [.09]| "lf" [.09]
    nsVowel -> "A" [.2]| "Ae" [.2]| "Au" [.2]| "Ei" [.2]| "Ou" [.2]
    nmVowel -> "a" [.125]| "e" [.125]| "i" [.125]| "o" [.125]| "u" [.125]| "au" [.125]| "oa" [.125]| "ei" [.125]
    neVowel -> "e" [.25]| "i" [.25]| "a" [.25]| "au" [.25]
    """)

# for sentence in generate(grammar, n=25):
#     print(" ".join(sentence))

# names = []
# for syllable in generate(grammar_names, n=10000000):
#     names.append("".join(syllable))

# print("names: ", names)


# def generate_sentences(grammar, num_sentences=5):
#     parser = nltk.ChartParser(grammar)
#     sentences = ['a dog chased the cat']
#     parsed_sentences = []
    
#     for tree in parser.parse_sents(sentences):
#         parsed_sentences.extend(tree)

#     # Extract sentences from parsed trees and convert them to strings
#     generated_sentences = [" ".join(tree.leaves()) for tree in parsed_sentences]

#     return generated_sentences

# generated_sentences = generate_sentences(grammar, num_sentences=5)
# for sentence in generated_sentences:
#     print(sentence)

#------------------------------------------------

def remove_stopwords(tokens):
    filtered_tokens = []
    stop_words = set(stopwords.words('english'))
    for word in tokens:
        if word.casefold() not in stop_words:
            filtered_tokens.append(word)
    return filtered_tokens

#function that removes punctuation, adjectives, pronouns
def remove_adj(tokens):
    filtered_tokens = []
    banned_words = ["MD", "PRP", ",", "?", "-", ":", "!", ";", "."]
    for word in tokens:
        if word[1] not in banned_words:
            filtered_tokens.append(word[0])
    return filtered_tokens

#take filtered tokens and compose the final command
def compose_command(tokens):
    cmd = ""
    for word in tokens:
        cmd = cmd + word + " "
    return cmd


def filter_command(str):
    tokens = nltk.word_tokenize(str)
    new_tokens = remove_stopwords(tokens)
    tagged = nltk.pos_tag(new_tokens)
    final_tokens = remove_adj(tagged)
    return compose_command(final_tokens)


