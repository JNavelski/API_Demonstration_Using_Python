#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 07:31:04 2021

@author: JosephNavelski
"""

# Setting Directory
import os
path = "/Users/JosephNavelski/Desktop/SocInteractionsResearch/Python code/"
os.chdir(path)
print(os.getcwd())

# This is where I store the keys needed in order to get varified by the API
from api_keys import bearer_token

# Import Packages
import requests
import os
import json
import time
import pandas as pd
import numpy as np

########################################################################
# Example 1: Full Archive Search
########################################################################

search_url = "https://api.twitter.com/2/tweets/search/all"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': '(from:twitterdev -is:retweet) OR #twitterdev',
                'max_results': '10',
                'tweet.fields': 'author_id,created_at,text,geo',
                'start_time': '2010-01-01T00:00:01.00Z',
                'end_time': '2019-01-08T00:00:01.00Z',
                'user.fields': 'username,location',
                'expansions': 'author_id',
                'next_token': None
                }

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", search_url, headers=headers, params=params)
    print('Current Status Code: ',response.status_code)
    print('Current Rate Limit: ', response.headers['x-rate-limit-remaining'])
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(search_url, headers, query_params)
    json.dumps(json_response, indent=4, sort_keys=True)
    print(json.dumps(json_response, indent=4, sort_keys=True))
    return(json_response)


if __name__ == "__main__":
    results = main()

df0 = pd.DataFrame(results['data'])
df0 = df0.rename(columns={'id': 'tweet_id'})
df1 = pd.DataFrame(results['includes'])
df1 = df1.join(pd.DataFrame(df1.pop('users').values.tolist()))

df = pd.concat([df0, df1], axis=1)


names = df['username']



########################################################################
# Example 2: Get Users Using their username
########################################################################

user_names = ','.join(names)

def create_url():
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    usernames = "usernames=TwitterDev,TwitterAPI"
    user_fields = "user.fields=description,created_at,location,verified,public_metrics"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    print(response.status_code)
    print('Current Rate Limit: ', response.headers['x-rate-limit-remaining'])
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()



# This is your "main" function, where your queries are executed
def main():
    url = create_url()
    json_response = connect_to_endpoint(url)
    print(json.dumps(json_response, indent=4, sort_keys=True))
    return(json_response)
    
if __name__ == "__main__":
    results = main()

df = pd.DataFrame(results['data'])
# un-nested dictionaries into series
df = df.join(pd.DataFrame(df.pop('public_metrics').values.tolist()))

########################################################################
# Example 3: ACS Data
########################################################################

import pandas as pd
import censusdata

sample = censusdata.search('acs5', 2015,'concept', 'transportation')

data = censusdata.download('acs5', 2015,
           censusdata.censusgeo([('state', '36'),
                                 ('county', '081'),
                                 ('block group', '*')]),
          ['B23025_001E', 'B23025_002E', 'B23025_003E',
           'B23025_004E', 'B23025_005E',
           'B23025_006E', 'B23025_007E'])

data
