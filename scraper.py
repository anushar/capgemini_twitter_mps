import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
url = "http://tweetminster.co.uk/mps/party/labour/page:"


def get_info(tweeter, counter):
    costituency = tweeter.find("h3").get_text()
    tmp = re.sub("\s", "", tweeter.find("p").get_text()).split("Labour")
    return pd.DataFrame({'costituency': costituency,
                         'name': tmp[0],
                         'twitter_id': tmp[1],
                         'party': 'Labour'}, index=[counter])


def scrape(page=1, counter=0):
    res = requests.get(url + str(page))
    soup = BeautifulSoup(res.text)
    tweeters = soup.findAll('div', {'class': 'tweeters'})
    output = pd.DataFrame(columns=["name", "twitter_id", "party",
                                   "costituency"])
    for tweeter in tweeters:
        output = pd.concat([output, get_info(tweeter, counter)])
        counter += 1
    if page > 17:
        return output
    else:
        page += 1
        return pd.concat([output, scrape(page, counter=counter)])
