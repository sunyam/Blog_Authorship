# Train a word2vec model and save it for later use

import gensim
from bs4 import BeautifulSoup

import os
import re
from nltk.corpus import stopwords
from string import punctuation
from nltk.tokenize import word_tokenize, sent_tokenize

# The dataset is ready (19320 .txt files containing all posts from each blogger, free from any useless tags <post> <blog> etc) - Code in the 'parseBlogs.py' file

# For more info on gensim and its usage: http://rare-technologies.com/deep-learning-with-word2vec-and-gensim/

class BlogSentences(object):

    def __init__(self, directory):
        # To keep a count
        self.i = 0
        
        # directory is the path to the .txt files/blogs
        self.directory = directory

    # Iterator for the class
    # Returns a list of words (a sentence)
    def __iter__(self):
        for blog in os.listdir(self.directory):
            for line in file(self.directory+'/'+blog, 'rb'):
                for sentence in line_to_sents(line):
                    words = sent_to_words(sentence)
                    if self.i % 1000 == 0:
                        print self.i
                    self.i += 1
                    
                    # Ignore really short sentences
                    if len(words) > 3:
                        yield words


# Converts line to sentences
def line_to_sents(line):

    # Remove <html> tags (if any)
    line = BeautifulSoup(line).get_text()

    sentences = sent_tokenize(line)
    
    for s in sentences:
        # Remove weird characters
        s = re.sub(r'[^a-zA-Z]', " ", s)
        yield s

# Converts sentences to words
def sent_to_words(sentence):
    # Make lowercase
    sentence = sentence.lower()

    words = word_tokenize(sentence)

    my_stopwords = stopwords.words('english') + list(punctuation)
    # Filter stopwords
    
    words_output = []
    for w in words:
        if w not in my_stopwords:
            words_output.append(w)
    
    return words_output

path = '/Users/sunyambagga/Desktop/MinorProjects/7th_Sem/txt_blogs'
s = BlogSentences(path)
model = gensim.models.Word2Vec(s, size=300, workers=8, min_count=40)
model.save('/Users/sunyambagga/Github/Blog_Authorship/blogs_model.word2vec')