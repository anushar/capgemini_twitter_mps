from TwitterAPI import TwitterAPI
import datetime
import csv
import pandas as pd
from time import sleep
 


################# set up the API #################
filename = 'twitter_credentials.csv'
f = open(filename,'r')
reader = csv.reader(f)

application_credentials = {}
for line in reader:
  application_credentials[line[0]] = line[1]


consumer_key = application_credentials['consumer_key']
consumer_secret = application_credentials['consumer_secret']
access_token_key = application_credentials['access_token_key']
access_token_secret = application_credentials['access_token_secret']


################# set up the query params #################
party = "labour"
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
 
def get_timelines(file_path):
    handles = pd.read_csv(file_path)['twitter_id']
    return pd.concat(map(lambda x: get_timeline(x), handles))


api = TwitterAPI(consumer_key,consumer_secret,access_token_key,access_token_secret)


input_file = party +"_mp_twitter_ids.csv"
result = get_timelines(input_file)

for line in result:
  print line