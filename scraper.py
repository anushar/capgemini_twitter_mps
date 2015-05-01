import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from ipdb import set_trace

base_url = "http://tweetminster.co.uk/mps/party/"
cols = ['costituency', 'name', 'twitter_id', 'party']


def get_info(tweeter, party="Labour"):
    costituency = tweeter.find("h3").get_text()
    tmp = re.sub("[\n\t]", "", tweeter.find("p").get_text()).split(party)
    return pd.DataFrame({'costituency': costituency,
                         'name': tmp[0].strip(),
                         'twitter_id': tmp[1].strip(),
                         'party': party}, index=[0])


def scrape(page=1, party="Labour"):
    party_url = "_".join(party.lower().split())
    url = base_url + party_url + '/page:' + str(page)
    res = requests.get(url)
    soup = BeautifulSoup(res.text)
    tweeters = soup.findAll('div', {'class': 'tweeters'})
    try:
        output = pd.concat(
            map(lambda x: get_info(x, party=party), tweeters))
    except ValueError:
        return pd.DataFrame(columns=cols)
    return pd.concat([output, scrape(page + 1, party=party)])
