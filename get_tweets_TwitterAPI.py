from TwitterAPI import TwitterAPI
import datetime
import csv
import sys
import pandas as pd
from time import sleep
from ipdb import set_trace

################# set up the API #################
credentials = pd.read_csv("twitter_credentials.csv",
                          header=-1, index_col=0).to_dict()[1]
api = TwitterAPI(**credentials)

################# set up the query params #################
party = "conservative"
min_date = datetime.datetime(2015, 2, 25)
params = {'count': 200}
cols = ['created_at', 'favorite_count', 'id', 'retweet_count', 'text']


def get_timeline(handle):
    print "obtaining tweets for user {}".format(handle)
    params.update({'screen_name': handle})
    res = api.request('statuses/user_timeline', params)
    if res.get_rest_quota()['remaining'] == 0:
        sleep(res.get_rest_quota()['reset'] - datetime.datetime.now())
    if res.status_code != 200:
        return
    try:
        df = pd.DataFrame(res.json())[cols]
    except:
        return
    df['user'] = handle
    df['created_at'] = pd.tseries.tools.to_datetime(df['created_at'])
    df = df[df['created_at'] >= min_date]
    return df.sort(columns="created_at", ascending=False)


def get_timelines(file_path):
    handles = pd.read_csv(file_path)['twitter_id']
    return pd.concat(map(lambda x: get_timeline(x), handles))

res = get_timelines('libdem_mp_twitter_ids.csv')
