from TwitterAPI import TwitterAPI
import datetime
import csv
import sys
import pandas as pd
from time import sleep
 


################# set up the API #################
filename = 'twitter_credentials.csv'
f = open(filename,'r')
reader = csv.reader(f)

credentials = {}
for line in reader:
  credentials[line[0]] = line[1]


class TwitterTimelineParser(object):

    def __init__(self,credentials):
        self.min_date = datetime.datetime(2015, 3, 25)
        self.params = {'count': 200}
        self.calls_limit_period = datetime.timedelta(minutes=15)
        self.cols = ['created_at', 'favorite_count', 'id', 'retweet_count', 'text']
        self.api = TwitterAPI(credentials['consumer_key'],credentials['consumer_secret'],credentials['access_token_key'],credentials['access_token_secret'])
        self.handles = []

    def get_timeline(self,handle):
     print "obtaining tweets for user {}".format(handle)
     self.params.update({'screen_name': handle})
     res = self.api.request('statuses/user_timeline', self.params)
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

    def get_timelines(self):
        return pd.concat(map(lambda x: self.get_timeline(x), handles))

    def set_handles(self,handles):
        self.handles = handles


party = 'labour'
input_file = party +"_mp_twitter_ids.csv"
handles = pd.read_csv(input_file)['twitter_id']

#should pass all other params in an object
parser = TwitterTimelineParser(credentials)
parser.set_handles(handles)
result = parser.get_timelines()