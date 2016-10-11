import os
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import accuracy_score

##############################################################################
'''
1. First Approach: 
- Using Average Word2Vec vectors for each blog (previously calculated and pickled in 'feature_extraction.py')
'''
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

gender_clf = LogisticRegression()

gs_clf = GridSearchCV(estimator=gender_clf, param_grid=parameters)

gs_clf.fit(x, y)

print "Accuracy: ", gs_clf.best_score_

print "Optimal Parameters: "
for p in sorted(parameters.keys()):
    print p, gs_clf.best_params_[p]

x_test = []
y_test = []

for d in list_of_dicts[16000:]:
    x_test.append(list(d['BlogVector']))
    y_test.append(d['Gender'])

x_test = np.array(x_test)
y_test = np.array(y_test)

#print "Newton C=1 Accuracy: ", gender_clf.score(x_test, y_test)
#print "Newton C=0.01 Accuracy: ", gender_clf_1000.score(x_test, y_test)
#print "Newton C=0.00001 Accuracy: ", gender_clf_100000.score(x_test, y_test)

y_pred = gs_clf.predict(x_test)

from sklearn.metrics import confusion_matrix
print confusion_matrix(y_test, y_pred)

print "Accuracy: "
print accuracy_score(y_test, y_pred)
##############################################################################