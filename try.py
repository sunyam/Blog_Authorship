'''
Predict the age/gender of a blog-post. The blog-post path should be stored in the 'path_to_blog'.
'''

import numpy as np
from gensim import models
import pickle
import os
from nltk.tokenize import word_tokenize
from sklearn.linear_model import LogisticRegression

path_to_model = '/Users/sunyambagga/GitHub/Blog_Authorship/blogs_model.word2vec'
model = models.Word2Vec.load(path_to_model)

path_to_blog = '/Users/sunyambagga/test.txt'
with open(path_to_blog, 'rb') as f:
    post = f.read()


#######################################################################################
# Calculating average-vector for the blog

words = word_tokenize(post.decode('utf8'))
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

#print "Vec: ", blog_avg_vector
#######################################################################################

word2vec_path = '/Users/sunyambagga/Desktop/MinorProjects/7th_Sem/feature_vectors.pickle'
# Load the feature-vectors
with open(word2vec_path, 'rb') as f:
    list_of_dicts = pickle.load(f)

x = []
y = []

for dict in list_of_dicts:
    x.append(list(dict['BlogVector']))
    y.append(dict['Gender'])

    # For predicting age, uncomment the following lines and comment the y.append(dict['Gender']) line.
#    age = ''
#    
#    if 13 <= int(dict['Age']) <= 19:
#        age = 'teens'
#
#    elif 20 <= int(dict['Age']) <= 29:
#        age = 'twenties'
#
#    elif 30 <= int(dict['Age']) <= 39:
#        age = 'thirties'
#
#    elif 40 <= int(dict['Age']) <= 49:
#        age = 'forties'
#
#    y.append(age)

x_train = x[:16000]
y_train = y[:16000]

#print len(x)
#print len(y)

lr1_age_clf = LogisticRegression()

lr1_age_clf.fit(x_train, y_train)

print "\n\n\n\n"
print lr1_age_clf.predict(blog_avg_vector)