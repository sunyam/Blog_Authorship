'''
Identifying the Most important words in a Blog.
Saving the results for future-use in a JSON file (Useful in calculating Bag-of-Words features).
'''

from nltk.tokenize import word_tokenize, sent_tokenize
from collections import defaultdict
from heapq import nlargest
from nltk.corpus import stopwords
from string import punctuation

# Adding self-created stopwords to the "default_stopwords" list:
file_path = "/Users/sunyambagga/my_stopwords.txt"

with open(file_path, 'rb') as file:
    lines = file.readlines()
    # To remove \r tags
    my_stopwords = []
    for line in lines:
        my_stopwords.append(line.rstrip())

default_stopwords = set(stopwords.words('english') + list(punctuation) + my_stopwords)


import gensim
# Loading Word2Vec model
path_to_model = '/Users/sunyambagga/GitHub/Blog_Authorship/blogs_model.word2vec'
model = gensim.models.Word2Vec.load(path_to_model)

def calculate_frequencies(sentences_ll, user_stopwords=None):  # sentences_ll is a list of lists
    frequency = defaultdict(int)    # default value : 0
    
    if user_stopwords is not None:
        stopwords = set(user_stopwords).union(default_stopwords)
    else:
        stopwords = default_stopwords
    
    for sentence in sentences_ll:
        for word in sentence:
            word = word.lower()
            # Word not in stopwords and no punctuation in words ("'s")
            if word not in stopwords and punctuation[6] not in word and word in model:
                frequency[word] += 1

    return frequency

def get_features(article, n, user_stopwords=None):  # n is the desired no. of features
    text = article
    sentences = sent_tokenize(text.decode('utf8'))
    
    sentences_ll = []
    for s in sentences:
        words = word_tokenize(s)
        sentences_ll.append(words)

    frequency = calculate_frequencies(sentences_ll, user_stopwords)

    return nlargest(n, frequency, key=frequency.get)

import os
path = '/Users/sunyambagga/Desktop/MinorProjects/7th_Sem/txt_blogs/'

# List of dictionaries where each dictionary represents a blog
list_of_dicts = []

counter = 0
for blog in os.listdir(path)[1:]:
#     print blog
    [ID, gender, age] = blog.split('.')[:-1]

    with open(path+blog, 'rb') as f:
        posts = f.read()
    
    dict_df = {}
    dict_df['Age'] = age
    dict_df['Gender'] = gender
    dict_df['ID'] = ID
    dict_df['Imp_words'] = get_features(posts, 40)

    list_of_dicts.append(dict_df)

    if counter % 600 == 0:
        print counter
    counter += 1

print "\nWe have captured " + str(len(list_of_dicts)) + " blogs.\n"

# Pickling the dictionary:
print "Saving Results...."
import json

with open('/Users/sunyambagga/Desktop/MinorProjects/7th_Sem/bow_features40.json', 'wb') as f:
    json.dump(list_of_dicts, f)

print "Done."