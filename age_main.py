from sklearn.linear_model import LogisticRegression
from sklearn.grid_search import GridSearchCV
import os
import numpy as np
import pickle
import json
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn import svm
from sklearn.metrics import confusion_matrix

#Analysing the Age values in the dataset using Pandas' DataFrame
import pandas as pd

word2vec_path = '/Users/sunyambagga/Desktop/MinorProjects/7th_Sem/feature_vectors.pickle'

# Load the feature-vectors
with open(word2vec_path, 'rb') as f:
    list_of_dicts = pickle.load(f)

df = pd.DataFrame(list_of_dicts)
df = df['Age']
print "\nAll bloggers in our dataset have ages b/w " + df.min() + " years and " + df.max() + " years."


###############################################################################
'''
1. First Approach: 
- Using Average Word2Vec vectors for each blog (previously calculated and pickled in 'feature_extraction.py')
'''
print "\nFIRST APPROACH (word2vec)...."

x = []
y = []

# Min Age- 13 & Max Age- 48
# Divide into Teens, 20s, 30s, 40s
for dict in list_of_dicts:
    age = ''
    
    if 13 <= int(dict['Age']) <= 19:
        age = 'teens'
    
    elif 20 <= int(dict['Age']) <= 29:
        age = 'twenties'
    
    elif 30 <= int(dict['Age']) <= 39:
        age = 'thirties'
    
    elif 40 <= int(dict['Age']) <= 49:
        age = 'forties'

    x.append(list(dict['BlogVector']))
    y.append(age)

x_train = x[:16000]
y_train = y[:16000]
x_test = x[16000:]
y_test = y[16000:]

#print len(x)
#print len(y)

lr1_age_clf = LogisticRegression()
lr1_age_clf.fit(x_train, y_train)
print "LogReg: ", lr1_age_clf.score(x_test, y_test)

svm_age_clf = svm.LinearSVC(verbose=1)
svm_age_clf.fit(x_train, y_train)
print "SVM: ", svm_age_clf.score(x_test, y_test)

