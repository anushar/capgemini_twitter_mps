import nltk
from sklearn import cross_validation
import numpy as np
import pickle
import random

data = pickle.load(open('features_and_labels','rb'))

#unlist as each element is a list of size one where the element
#is a tuple with features dict as zeroth element and party label as first
features_and_labels = [item for sublist in data for item in sublist]

#randomize
random.shuffle(features_and_labels)


size = len(features_and_labels)

#train-test split
train_fraction = 0.7



#do cross-validation on the training set
#cv = cross_validation.KFold(len(train_set), n_folds = 10, indices = True, shuffle = False, random_state = None)

repeats = 10
print "---------------------cv-------------------------"
classifiers = []
cv_accuracies = []

#repeat kFold cross validation repeats times
for r in range(repeats):

    train_set, test_set = features_and_labels[int(train_fraction*size):], features_and_labels[:int(train_fraction*size)]

    cv = cross_validation.KFold(len(train_set), n_folds = 10, indices = True, shuffle = False, random_state = None)

    for train_cv, eval_cv in cv:
        classifier = nltk.NaiveBayesClassifier.train(train_set[train_cv[0]:train_cv[len(train_cv)-1]])
        accuracy = nltk.classify.accuracy(classifier,train_set[eval_cv[0]:eval_cv[len(eval_cv)-1]])
        print 'accuracy: ', accuracy
        classifiers.append(classifier)
        cv_accuracies.append(accuracy)

#test the classifiers on the test set
test_accuracies = []
print "---------------------testing-------------------------"
for classifier in classifiers:
    #print classifier
    accuracy = nltk.classify.accuracy(classifier,test_set)
    print "accuracy: " , accuracy
    test_accuracies.append(accuracy)
    print classifier.show_most_informative_features()


print "mean accuracy", np.mean(test_accuracies)
print "std accuracy", np.std(test_accuracies)


