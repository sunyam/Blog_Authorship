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

print "\n\nPREDICTING AGE.."
print "\nAll bloggers in our dataset have ages b/w " + df.min() + " years and " + df.max() + " years."


###############################################################################
'''
1. First Approach: 
- Using Average Word2Vec vectors for each blog (previously calculated and pickled in 'feature_extraction.py')
'''
print "\nFIRST APPROACH: Word2Vec.."

x = []
y = []

# Min Age- 13 & Max Age- 48
# Divide into Teens, 20s, 30s, 40s
#c13 = 0
#c20 = 0
#c30 = 0
#c40 = 0

for dict in list_of_dicts:
    age = ''
    
    if 13 <= int(dict['Age']) <= 19:
        age = 'teens'
#        c13 += 1

    elif 20 <= int(dict['Age']) <= 29:
        age = 'twenties'
#        c20 += 1

    elif 30 <= int(dict['Age']) <= 39:
        age = 'thirties'
#        c30 += 1

    elif 40 <= int(dict['Age']) <= 49:
        age = 'forties'
#        c40 += 1

    x.append(list(dict['BlogVector']))
    y.append(age)

#print c13, c20, c30, c40

x_train = x[:16000]
y_train = y[:16000]
x_test = x[16000:]
y_test = y[16000:]

#print len(x)
#print len(y)

lr1_age_clf = LogisticRegression()

lr1_age_clf.fit(x_train, y_train)

blog = ""

print lr1_age_clf.predict([blog])

#y_pred = lr1_age_clf.predict(x_test)

from sklearn import metrics

print "\nLogistic Regression Accuracy: ", lr1_age_clf.score(x_test, y_test)
print "\nConfusion Matrix:\n", metrics.confusion_matrix(y_test, y_pred, labels=['teens', 'twenties', 'thirties', 'forties'])

print "\nClassification Report:\n", metrics.classification_report(y_test, y_pred, labels=['teens', 'twenties', 'thirties', 'forties'])


svm_age_clf = svm.LinearSVC()
svm_age_clf.fit(x_train, y_train)
print "\nSVM: ", svm_age_clf.score(x_test, y_test)
print "\n\n-------------------------------------------------------------------------------------------------------------------------"

##############################################################################
'''
2. Second Approach:
- Using Bag-of-Words feature-vectors for each blog (previously calculated and pickled in 'feature_extraction.py')
'''
print "\n\nSECOND APPROACH: Bag-of-Words.."
bow_path = '/Users/sunyambagga/Desktop/MinorProjects/7th_Sem/bow_features40.json'

# Load Important_Words
with open(bow_path, 'rb') as f:
    _2_list_of_dicts = json.load(f)

#print "Loaded " + str(len(_2_list_of_dicts)) + " blogs."

# Prepare x_train/test and y_train/test
x_training = []
y_training = []
x_test = []
y_test = []

for dict in _2_list_of_dicts[:16000]:
    words = dict['Imp_words']
    sentence = " ".join(words)
    x_training.append(sentence)

    age = ''
    
    if 13 <= int(dict['Age']) <= 19:
        age = 'teens'
    
    elif 20 <= int(dict['Age']) <= 29:
        age = 'twenties'
    
    elif 30 <= int(dict['Age']) <= 39:
        age = 'thirties'
    
    elif 40 <= int(dict['Age']) <= 49:
        age = 'forties'

    y_training.append(age)

for dict in _2_list_of_dicts[16000:]:
    words = dict['Imp_words']
    sentence = " ".join(words)
    x_test.append(sentence)

    age = ''
    
    if 13 <= int(dict['Age']) <= 19:
        age = 'teens'
    
    elif 20 <= int(dict['Age']) <= 29:
        age = 'twenties'
    
    elif 30 <= int(dict['Age']) <= 39:
        age = 'thirties'
    
    elif 40 <= int(dict['Age']) <= 49:
        age = 'forties'

    y_test.append(age)

#print len(x_training)
#print len(y_training)
#print "\n\n"
#print len(x_test)
#print len(y_test)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(x_training)
X = X.toarray()

nb2_g_clf = MultinomialNB()
lr2_g_clf = LogisticRegression()

# Training Naive Bayes classifier for Gender:
nb2_g_clf.fit(X, y_training)

# Training LogReg classifier for Gender:
lr2_g_clf.fit(X, y_training)

X_test = vectorizer.transform(x_test)

print "\nNaive Bayes Accuracy: ", nb2_g_clf.score(X_test, y_test)
print "\nLogistic Regression Accuracy: ", lr2_g_clf.score(X_test, y_test)

svm_gender2_clf = svm.LinearSVC()
svm_gender2_clf.fit(X, y_training)
print "\nSVM Accuracy: ", svm_gender2_clf.score(X_test, y_test)
print "\n\n\n\n"
##############################################################################
