"""
information

What's difference btw stemming and Lemmatization?

e.g.,) studies
stemming : studi

lemmatization: study

to improve recall, use lemmatization
"""

import os
import re

from toolz.curried import *

import nltk

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')
nltk.download("punkt")

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer

BASE_DIR = "stories"

CONTRADICTION_DICT = { "ain’t": "are not", "’s":" is", "aren’t": "are not", "can’t": "cannot", "can’t’ve": "cannot have", "‘cause": "because", "could’ve": "could have", "couldn’t": "could not", "couldn’t’ve": "could not have", "didn’t": "did not", "doesn’t": "does not", "don’t": "do not", "hadn’t": "had not", "hadn’t’ve": "had not have", "hasn’t": "has not", "haven’t": "have not", "he’d": "he would", "he’d’ve": "he would have", "he’ll": "he will", "he’ll’ve": "he will have", "how’d": "how did", "how’d’y": "how do you", "how’ll": "how will", "I’d": "I would", "I’d’ve": "I would have", "I’ll": "I will", "I’ll’ve": "I will have", "I’m": "I am", "I’ve": "I have", "isn’t": "is not", "it’d": "it would", "it’d’ve": "it would have", "it’ll": "it will", "it’ll’ve": "it will have", "let’s": "let us", "ma’am": "madam", "mayn’t": "may not", "might’ve": "might have", "mightn’t": "might not", "mightn’t’ve": "might not have", "must’ve": "must have", "mustn’t": "must not", "mustn’t’ve": "must not have", "needn’t": "need not", "needn’t’ve": "need not have", "o’clock": "of the clock", "oughtn’t": "ought not", "oughtn’t’ve": "ought not have", "shan’t": "shall not", "sha’n’t": "shall not", "shan’t’ve": "shall not have", "she’d": "she would", "she’d’ve": "she would have", "she’ll": "she will", "she’ll’ve": "she will have", "should’ve": "should have", "shouldn’t": "should not", "shouldn’t’ve": "should not have", "so’ve": "so have", "that’d": "that would", "that’d’ve": "that would have", "there’d": "there would", "there’d’ve": "there would have", "they’d": "they would", "they’d’ve": "they would have","they’ll": "they will",
 "they’ll’ve": "they will have", "they’re": "they are", "they’ve": "they have", "to’ve": "to have", "wasn’t": "was not", "we’d": "we would", "we’d’ve": "we would have", "we’ll": "we will", "we’ll’ve": "we will have", "we’re": "we are", "we’ve": "we have", "weren’t": "were not","what’ll": "what will", "what’ll’ve": "what will have", "what’re": "what are", "what’ve": "what have", "when’ve": "when have", "where’d": "where did", "where’ve": "where have",
 "who’ll": "who will", "who’ll’ve": "who will have", "who’ve": "who have", "why’ve": "why have", "will’ve": "will have", "won’t": "will not", "won’t’ve": "will not have", "would’ve": "would have", "wouldn’t": "would not", "wouldn’t’ve": "would not have", "y’all": "you all", "y’all’d": "you all would", "y’all’d’ve": "you all would have", "y’all’re": "you all are", "y’all’ve": "you all have", "you’d": "you would", "you’d’ve": "you would have", "you’ll": "you will", "you’ll’ve": "you will have", "you’re": "you are", "you’ve": "you have"}

def load_data(fn):
    with open(os.path.join(BASE_DIR, fn), 'r', encoding='utf-8') as f:
        doc_data = f.read()
    return doc_data

"""
todo: construct inverted index by spimi algorithm.
"""
# inverted index construction by spimi algorithm
def spimi(docs_fns):
    ...

"""
contraction : words or combinations, but one of the most straight forward  
"""
def rm_contraction(s):
    contractions_re = re.compile('(%s)'%'|'.join(CONTRADICTION_DICT.keys()))
    replace = lambda match: CONTRADICTION_DICT[match.group(0)]
    return contractions_re.sub(replace, s)

def tokenize(sentence):
    return word_tokenize(sentence, language='english')

# remove punctutation, number, stop words
def rm_etcs(tokens):
    stw = set(stopwords.words('english'))
    # remove puncutation
    punctuation_re = re.compile('[^a-zA-z]')

    rm_punc = map(lambda word: punctuation_re.sub('', word))
    # remove number
    regex = re.compile(r'[\d`]+')
    rm_num = map(lambda word: regex.sub('', word))
    # remove stop words
    rm_stopword = filter(lambda x: x.lower() not in stw)
    rm_empty = filter(identity)

    return pipe(tokens, rm_punc, rm_num, rm_stopword, rm_empty)

# stemming process
stemmer = SnowballStemmer('english')
stemize = map(stemmer.stem)


# lammatizing process
lemmatizer = WordNetLemmatizer()
lemmatize = map(lemmatizer.lemmatize)

# preprocess runner
sent_preprocess = compose(stemize, rm_etcs, tokenize, rm_contraction)


if __name__ == "__main__":
    test_file_name = "3gables.txt"
    run = compose(list, stemize, rm_etcs, tokenize, rm_contraction, load_data)
    print(run(test_file_name), sep="\n")