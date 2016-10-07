import os
import numpy as np
import pickle

path = '/Users/sunyambagga/Desktop/MinorProjects/7th_Sem/feature_vectors.pickle'

# Load the feature-vectors
with open(path, 'rb') as f:
    list_of_dicts = pickle.load(f)

x = []
y = []

for dict in list_of_dicts[:16000]:
    x.append(list(dict['BlogVector']))
    y.append(dict['Gender'])

x = np.array(x)
y = np.array(y)

#print x
#print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
#print y


from sklearn.linear_model import LogisticRegression



#gs_clf.fit(x, y)
#
#print "\n"
#print "Accuracy: ", gs_clf.best_score_
#
#for p in sorted(parameters.keys()):
#    print p, gs_clf.best_params_[p]


gender_clf = LogisticRegression()
gender_clf.fit(x, y)

gender_clf_1000 = LogisticRegression(C=1000, solver='lbfgs')
gender_clf_1000.fit(x,y)

gender_clf_100000 = LogisticRegression(C=100000, solver='lbfgs')
gender_clf_100000.fit(x,y)

x_test = []
y_test = []

for d in list_of_dicts[16000:]:
    x_test.append(list(d['BlogVector']))
    y_test.append(d['Gender'])

x_test = np.array(x_test)
y_test = np.array(y_test)

print "Newton C=1 Accuracy: ", gender_clf.score(x_test, y_test)
print "Newton C=0.01 Accuracy: ", gender_clf_1000.score(x_test, y_test)
print "Newton C=0.00001 Accuracy: ", gender_clf_100000.score(x_test, y_test)
#
##from sklearn.linear_model import SGDClassifier
##
##sgd = SGDClassifier()
##sgd.fit(x, y)
##
##print "SGD: ", sgd.score(x_test, y_test)
##
y_pred = gender_clf.predict(x_test)
##

from sklearn.metrics import confusion_matrix
print confusion_matrix(y_test, y_pred)