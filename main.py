import os

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

print len(list_of_dicts)

# Calculating vectors for each blog from the word2vec model
import gensim
from nltk.tokenize import word_tokenize

path_to_model = '/Users/sunyambagga/GitHub/Blog_Authorship/blogs_model.word2vec'
model = gensim.models.Word2Vec.load(path_to_model)

# Maps blog-ID to blog-vector
id_blogVector_map = {}

i = 0
for blog_dict in list_of_dicts:
    if i % 100 == 0:
	print i
    i += 1
    post = blog_dict['Posts']
    words = word_tokenize(post.decode('utf8'))
    
    # Filter words if there are in our word2vec model
    my_words = []
    for w in words:
        if w in model:
            my_words.append(w)
    
    blog_vector = [0.0]*300
    numberOfWords = 0
    
    for w in my_words:
        numberOfWords += 1
        vec = model[w]
        blog_vector += vec
    
    blog_vector = blog_vector/numberOfWords
    
    id_blogVector_map[blog_dict['ID']] = blog_vector
    
print len(id_blogVector_map)    # prints 19,320