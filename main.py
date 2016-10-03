import os
import numpy as np

path = '/Users/sunyambagga/Desktop/MinorProjects/7th_Sem/txt_blogs/'

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

print "We have captured " + str(len(list_of_dicts)) + " blogs."

# Calculating average-vectors for each blog
import gensim
from nltk.tokenize import word_tokenize

# Loading Word2Vec model
path_to_model = '/Users/sunyambagga/GitHub/Blog_Authorship/blogs_model.word2vec'
model = gensim.models.Word2Vec.load(path_to_model)

# Maps blog-ID to blog-vector
id_blogVector_map = []

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
    if i % 50 == 0:
        print i
    i += 1


print len(id_blogVector_map)    # prints 19,320
print len(list_of_dicts)

# Merge the two dictionaries i.e. add another field in list_of_dicts that contains the average_vector

# Sorting the two lists of dictionaries according to ID
import operator

key = operator.itemgetter("ID")

list_of_dicts = sorted(list_of_dicts, key=key)
#print list_of_dicts
#print "\n\n\n\n\n\n\n\n\n"

id_blogVector_map = sorted(id_blogVector_map, key=key)
#print id_blogVector_map
#print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"

for (i,j) in zip(list_of_dicts, id_blogVector_map):
    i.update(j)

#print "B is still the same:\n", id_blogVector_map
#print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
#print list_of_dicts
#print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"

for dict in list_of_dicts:
    del dict['Posts']
#print list_of_dicts
#print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"