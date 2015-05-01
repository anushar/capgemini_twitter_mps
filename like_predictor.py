import pandas as pd
import numpy as np
from sklearn.pipeline import TransformerMixin

df = pd.read_csv('features_and_favorite_count_labels.csv')

#print df['favorite_count'].value_counts()

#df2 = pd.get_dummies(df['contains(ahead)'])






train_fraction = 0.8
msk = np.random.rand(len(df)) < train_fraction

train = df[msk]
test = df[~msk]


columns = train.columns[:-1]
train_y = train['favorite_count'].values
train_x = train[list(columns)].values ## Y

#dummy encode
train_x_dummy = pd.concat([pd.get_dummies(train_x[col]) for col in train_x], axis=1, keys=train_x.columns)

columns = test.columns[:-1]
test_y = test['favorite_count'].values
test_x = test[list(columns)].values ## Y

train_y,_ = pd.factorize(train_y)
test_y,_ = pd.factorize(test_y)

