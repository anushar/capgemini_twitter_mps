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
libdem_tweets = pd.read_csv('conservative_tweets.csv')

#set party and concat
labour_tweets['party'] = 'labour'
conservative_tweets['party'] = 'conservative'
tweets = pd.concat([labour_tweets,conservative_tweets],ignore_index=True)

#clean
tweets['text'] = tweets['text'].apply(lambda tweet : nlp_utils.clean_tweet(tweet) if not isinstance(tweet,float) else 'nan')



def features_and_labels_group_by_mp(tweets,header_string="number of",target='party'):

    features_and_labels_dict = {}

    for idx,row in tweets.iterrows():

        features  = nlp_utils.document_features(row['text'].split(),keywords,header_string)


        if row['user'] not in features_and_labels_dict:
            features_and_labels_dict[row['user']] = []
            features_and_labels_dict[row['user']].append((features,row[target]))
        else:
            for k,v in features.items():
                features_and_labels_dict[row['user']][0][0][k] += v

    features_and_labels = [item for sublist in features_and_labels_dict.values() for item in sublist]
    for item in features_and_labels:
        item[0].update({target:item[1]})


    df = pd.DataFrame([item[0] for item in features_and_labels])

    df.to_csv('features_and_'+target+'_labels_grouped_by_mp.csv',ignore_index=True,index=False)


def features_and_labels(tweets,header_string="contains",target='party'):

    features_and_labels = []

    for idx,row in tweets.iterrows():

        features  = nlp_utils.document_features(row['text'].split(),keywords,header_string)

        features_and_labels.append((features,row[target]))


    for item in features_and_labels:
        item[0].update({target:item[1]})


    df = pd.DataFrame([item[0] for item in features_and_labels])

    df.to_csv('features_and_'+target+'_labels.csv',ignore_index=True,index=False)
    #pickle.dump(features_and_labels,open('features_and_party_labels','wb'))

header_string = ["number_of","contains"]
targets = ['party','favorite_count','retweet_count']
#features_and_labels_group_by_mp(tweets,"number of")
#features_and_labels(tweets,"contains")

for target in targets:
    features_and_labels(tweets)
    features_and_labels_group_by_mp(tweets)
