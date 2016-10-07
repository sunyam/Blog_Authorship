'''
Extracting features from each Blog
Calculate a BlogVector for each Blog and Pickle it for future use.
'''

import pickle
import os
import numpy as np
import gensim
from nltk.tokenize import word_tokenize
import operator

# Path to the main dataset
path = '/Users/sunyambagga/Desktop/MinorProjects/7th_Sem/txt_blogs/'

# List of dictionaries where each dictionary represents a blog
list_of_dicts = []

for blog in os.listdir(path)[1:]:
#     print blog
    [ID, gender, age] = blog.split('.')[:-1]

    with open(path+blog, 'rb') as f:
        posts = f.read()
    
    dict_df = {}
    dict_df['Age'] = age
    dict_df['Gender'] = gender
    dict_df['ID'] = ID
    dict_df['Posts'] = posts

    list_of_dicts.append(dict_df)

print "\nWe have captured " + str(len(list_of_dicts)) + " blogs.\n"


# 1. Calculating average-vectors for each blog in our dataset

# Loading Word2Vec model
path_to_model = '/Users/sunyambagga/GitHub/Blog_Authorship/blogs_model.word2vec'
model = gensim.models.Word2Vec.load(path_to_model)

# Initialise a list that will map blog-IDs to their blog-vectors
id_blogVector_map = []

# Counter variable
i = 0

for blog_dict in list_of_dicts:
    
    post = blog_dict['Posts']
    words = word_tokenize(post.decode('utf8'))
#    print "Originally: ", len(words)

    # Filter words if they are not present in our word2vec model
    my_words = []
    for w in words:
        if w in model:
            my_words.append(w)

#    print "After filtering: ", len(my_words)

    blog_vector = [0.0]*300
    numberOfWords = 0

    for w in my_words:
        numberOfWords += 1
        vec = model[w]
        blog_vector = np.add(blog_vector, vec)

    blog_avg_vector = np.nan_to_num(blog_vector/numberOfWords)

    temp_dict = {}
    temp_dict['ID'] = blog_dict['ID']
    temp_dict['BlogVector'] = blog_avg_vector

    id_blogVector_map.append(temp_dict)

    # To keep track of where we are:
    if i % 600 == 0:
        print i
    i += 1


#print len(id_blogVector_map)    # prints 19320
#print len(list_of_dicts)    # prints 19320

# 2. Merge the two dictionaries i.e. add another field in "list_of_dicts" that contains the BlogVector

# Sorting the two lists of dictionaries according to ID
key = operator.itemgetter("ID")

list_of_dicts = sorted(list_of_dicts, key=key)
#print list_of_dicts
id_blogVector_map = sorted(id_blogVector_map, key=key)
#print id_blogVector_map

for (i,j) in zip(list_of_dicts, id_blogVector_map):
    i.update(j)

#print "2nd one is still the same:\n", id_blogVector_map

#print "Another key added in list_of_dicts:\n", list_of_dicts

for dict in list_of_dicts:
    del dict['Posts']

# 3. Pickle the list_of_dicts for future use:

print "\nPickling...."

# Path to where the pickle-file will be stored
pickle_path = '/Users/sunyambagga/Desktop/MinorProjects/7th_Sem/'

with open(pickle_path+'feature_vectors.pickle', 'wb') as f:
    pickle.dump(list_of_dicts, f)

print "\nSuccessfully pickled " + str(len(list_of_dicts)) + " blogs."