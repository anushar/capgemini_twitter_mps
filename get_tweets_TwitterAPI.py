from TwitterAPI import TwitterAPI
from TwitterAPI import TwitterConnectionError
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
    try:
        res = api.request('statuses/user_timeline', params)
    except TwitterConnectionError:
        return
    if res.get_rest_quota()['remaining'] == 0:
        time = (res.get_rest_quota()['reset'] -
                datetime.datetime.now()).seconds + 10
        print "sleeping {} seconds".format(time)
        sleep(time)
    if res.status_code == 404:
        print [x['message'] for x in res.json()['errors']]
        return
    elif res.status_code == 401:
        print res.json()['error']
        return
    elif res.status_code == 429:
        sleep(15 * 60)
    elif res.status_code != 200:
        set_trace()
        return
    try:
        df = pd.DataFrame(res.json())[cols]
    except:
        return
    df['user'] = handle
    df['created_at'] = pd.tseries.tools.to_datetime(df['created_at'])
    #df = df[df['created_at'] >= min_date]
    return df.sort(columns="created_at", ascending=False)


def get_timelines(file_path):
    handles = pd.read_csv(file_path)['twitter_id']
    return pd.concat(map(lambda x: get_timeline(x), handles))
<<<<<<< HEAD

res = get_timelines('libdem_mp_twitter_ids.csv')
res.to_csv('libdem_tweets.csv',encoding='utf-8')
=======
>>>>>>> a59494c141883b09b040573acfee547a3dabe223
