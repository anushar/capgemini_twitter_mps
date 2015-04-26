from TwitterAPI import TwitterAPI
import pandas as pd
import datetime
from time import sleep
api = TwitterAPI('4Mn71tKklQQrIcxHiauceJLTr',
                 'clnwXEDX1JgzPDnesNwRNK98kcWpl1sQtLqiVkHfHwZBHlbz3c',
                 '363153981-9e4t4xlcmNE9hAPqaqWXHz5Nupxm29jidTh8gBoY',
                 'BaewMtWhngkXloKxN07iAe38NrYhj5TXhcVChkntD69Y5')

min_date = datetime.datetime(2015, 3, 25)
params = {'count': 200}
calls_limit_period = datetime.timedelta(minutes=15)
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


def get_timelines(file_path="labour_mp_twitter_ids.csv"):
    handles = pd.read_csv(file_path)['twitter_id']
    return pd.concat(map(lambda x: get_timeline(x), handles))