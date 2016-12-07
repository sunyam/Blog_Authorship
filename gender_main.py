import os
import numpy as np
import pickle
import json
from sklearn.linear_model import LogisticRegression
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn import svm

##############################################################################
'''
1. First Approach: 
- Using Average Word2Vec vectors for each blog (previously calculated and pickled in 'feature_extraction.py')
'''
print "\nFIRST APPROACH (word2vec)...."

word2vec_path = '/Users/sunyambagga/Desktop/MinorProjects/7th_Sem/feature_vectors.pickle'

# Load the feature-vectors
with open(word2vec_path, 'rb') as f:
    list_of_dicts = pickle.load(f)

x = []
y = []

for dict in list_of_dicts[:16000]:
    x.append(list(dict['BlogVector']))
    y.append(dict['Gender'])

x = np.array(x)
y = np.array(y)
#print x
#print y

parameters = {'C':[0.00001, 0.001, 1.0, 1000.0, 100000.0], 'solver':['newton-cg', 'lbfgs', 'liblinear']}

gs_clf = LogisticRegression()
gs_clf.fit(x, y)

#lr1_g_clf = LogisticRegression()
#gs_clf = GridSearchCV(estimator=lr1_g_clf, param_grid=parameters)
#gs_clf.fit(x, y)
#print "Accuracy: ", gs_clf.best_score_
#print "Optimal Parameters: "
#for p in sorted(parameters.keys()):
#    print p, gs_clf.best_params_[p]

x_test = []
y_test = []

for d in list_of_dicts[16000:]:
    x_test.append(list(d['BlogVector']))
    y_test.append(d['Gender'])

x_test = np.array(x_test)
y_test = np.array(y_test)

y_pred = gs_clf.predict(x_test)

print confusion_matrix(y_test, y_pred)
print "LogReg Accuracy: ", accuracy_score(y_test, y_pred)


svm_gender_clf = svm.LinearSVC(verbose=1, max_iter=2000)
svm_gender_clf.fit(x, y)
print "SVM: ", svm_gender_clf.score(x_test, y_test)


##############################################################################

##############################################################################
'''
2. Second Approach:
- Using Bag-of-Words feature-vectors for each blog (previously calculated and pickled in 'feature_extraction.py')
'''
print "\n\n\n\n\n\nSECOND APPROACH (n-grams)...."
bow_path = '/Users/sunyambagga/Desktop/MinorProjects/7th_Sem/bow_features40.json'

# Load Important_Words
with open(bow_path, 'rb') as f:
    _2_list_of_dicts = json.load(f)

print "Loaded " + str(len(_2_list_of_dicts)) + " blogs."

# Prepare x_train/test and y_train/test
x_training = []
y_training = []
x_test = []
y_test = []

for dict in _2_list_of_dicts[:16000]:
    words = dict['Imp_words']
    sentence = " ".join(words)
    x_training.append(sentence)
    y_training.append(dict['Gender'])

for dict in _2_list_of_dicts[16000:]:
    words = dict['Imp_words']
    sentence = " ".join(words)
    x_test.append(sentence)
    y_test.append(dict['Gender'])

#print len(x_training)
#print len(y_training)
#print "\n\n"
#print len(x_test)
#print len(y_test)

vectorizer = CountVectorizer(min_df=1)
X = vectorizer.fit_transform(x_training)
X = X.toarray()

nb2_g_clf = MultinomialNB()
lr2_g_clf = LogisticRegression(C=1.0, solver='liblinear')

# Training Naive Bayes classifier for Gender:
nb2_g_clf.fit(X, y_training)

# Training LogReg classifier for Gender:
lr2_g_clf.fit(X, y_training)

X_test = vectorizer.transform(x_test)

print "NB Accuracy: ", nb2_g_clf.score(X_test, y_test)
print "LogReg Accuracy: ", lr2_g_clf.score(X_test, y_test)


svm_gender2_clf = svm.LinearSVC(verbose=1, max_iter=2000)
svm_gender2_clf.fit(X, y_training)
print "SVM: ", svm_gender2_clf.score(X_test, y_test)

##############################################################################