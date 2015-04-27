import pandas as pd
import nlp_utils
import numpy as np
import pickle
import nltk
from nltk.corpus import stopwords


#read the keywords list and clean, i.e. strip newlines, and convert to lower case
keywords  = map(lambda kw : kw.strip(), open('political_keywords.txt','r').readlines())

keywords = map(lambda kw : kw.lower(),keywords)

print "we have " + str(len(keywords)) + " keywords."

#read the labour and conservative tweets csvs
labour_tweets = pd.read_csv('labour_tweets.csv')
conservative_tweets = pd.read_csv('conservative_tweets.csv')

#set party and concat
labour_tweets['party'] = 'labour'
conservative_tweets['party'] = 'conservative'
tweets = pd.concat([labour_tweets,conservative_tweets],ignore_index=True)

#clean
tweets['text'] = tweets['text'].apply(lambda tweet : nlp_utils.clean_tweet(tweet) if not isinstance(tweet,float) else 'nan')



#compute the word frequency distribution by
#first pasting all tweets together
all_words = []
for tweet in tweets['text']:
    tweets.extend(tweet.split())

print nltk.FreqDist(tweets).most_common(10)




#dict with key:user, value tupe of features and party label
#features get updated every time a new tweet by the user is encountered

features_and_labels_dict = {}


for idx,row in tweets.iterrows():

    features  = nlp_utils.document_features(row['text'].split(),keywords)

    if row['user'] not in features_and_labels_dict:
        features_and_labels_dict[user] = []
        features_and_labels_dict[user].append((features,row['party']))
    else:
        for k,v in features.items():

            features_and_labels_dict[user][0][0][k] += v


#serialize
pickle.dump(features_and_labels_dict.values(),open('features_and_labels','wb'))

#write as csv
"""
n_row = 0
f = open("features_and_labels.csv",'wb')
for (features,label) in features_and_labels:
    if n_row == 0:
        for k in features.keys():
            f.write(k)
            f.write(',')
        f.write('\n')
    n_row += 1
    for val in features.values():
        f.write(str(val))
        f.write(',')
    f.write(label)
    f.write('\n')
"""
