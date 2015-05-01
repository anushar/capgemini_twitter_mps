import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydot

############evaluation and cross validation###################
from sklearn.cross_validation import cross_val_score,train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn import preprocessing
from sklearn.externals.six import StringIO

###classifiers#######################################
from sklearn.linear_model import LogisticRegression,RidgeClassifier
from sklearn.svm import LinearSVC, SVC, NuSVC
from sklearn.neighbors import KNeighborsClassifier,RadiusNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier, export_graphviz
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.lda import LDA
from sklearn.qda import QDA



################various classifier models############################################################################
#model = LogisticRegression(C=1,penalty="l2",dual=False)
#model = KNeighborsClassifier(n_neighbors=9,weights="distance")
#model = LinearSVC(C=0.1,penalty="l1",loss="l2",dual=False)
#model = DecisionTreeClassifier(max_depth=8,min_samples_leaf=2,min_samples_split=2,max_features=None,criterion="entropy")
#model = ExtraTreeClassifier(max_depth=10,min_samples_leaf=5)
#model = RidgeClassifier(alpha=0.0)
#model = GaussianNB()
#model = LDA()
#model = QDA()
#model = SVC(C=1.0,gamma=3)
#model = SVC(kernel="linear", C=1.025)
############################## ensemble classifiers ###################################################################
depth = 2 #2
estimators = 200#30
max_features = 'log2'

#estimator = DecisionTreeClassifier(max_depth=depth,min_samples_leaf=5,min_samples_split=5,\
#max_features=max_features,criterion="entropy")
#model = AdaBoostClassifier(base_estimator=estimator,algorithm="SAMME.R",n_estimators=estimators,learning_rate=1.0)

#model = GradientBoostingClassifier(n_estimators=estimators, learning_rate=1.0,max_depth=1, random_state=0)




df = pd.read_csv('features_and_party_labels_grouped_by_mp.csv')


train_fraction = 0.8
msk = np.random.rand(len(df)) < train_fraction

train = df[msk]
test = df[~msk]


columns = train.columns[:-1]
train_y = train['party'].values.astype(str) ## X
train_x = train[list(columns)].values ## Y

columns = test.columns[:-1]
test_y = test['party'].values.astype(str) ## X
test_x = test[list(columns)].values ## Y

train_y,_ = pd.factorize(train_y)
test_y,_ = pd.factorize(test_y)


"""
scores = cross_val_score(model, train_x, train_y, cv=10)
print scores
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

#classification report


print(classification_report(y_true, y_pred, target_names=target_names))
"""


"""
rf = RandomForestClassifier(n_estimators=estimators,max_depth=None,criterion="entropy",min_samples_split=2,min_samples_leaf=2,n_jobs=-1,verbose=1)


y_pred = rf.fit(train_x, train_y).predict(test_x)

print classification_report(test_y, y_pred)

print rf.feature_importances_

# these values will all add up to one.  Let's call the "important" ones the ones that are above average.
important_features = []
for x,i in enumerate(rf.feature_importances_):
    if i>np.average(rf.feature_importances_):
        important_features.append((str(x), df.columns[x]))
"""
#print 'Most important features:',', '.join(important_features)
#print important_features

#clf = DecisionTreeClassifier().fit(train_x, train_y)
#export_json(clf, out_file="test.jso", feature_names=None)


#tree.export_graphviz(tr, out_file="test", feature_names=train.columns[:-1])
#with open("tree.dot", 'w') as f:
  #f = tree.export_graphviz(clf, out_file=f, feature_names=train.columns[:-1])

"""
dot_data = StringIO()
tree.export_graphviz(clf, out_file=dot_data)
graph = pydot.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf("iris.pdf")
"""
