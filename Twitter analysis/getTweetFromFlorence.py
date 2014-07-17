#!/usr/bin/python
# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1Session


oauth_consumer_key = "YOUR_CONSUMER_KEY"
oauth_consumer_secret = "YOUR_CONSUMER_SECRET"
oauth_token = "YOUR_TOKEN"
oauth_token_secret = "YOUR_TOKEN_SECRET"

twitter = OAuth1Session(oauth_consumer_key, client_secret=oauth_consumer_secret,
                        resource_owner_key=oauth_token,
                        resource_owner_secret=oauth_token_secret)

r = twitter.get(
    'https://stream.twitter.com/1.1/statuses/filter.json?locations=10.711790,43.451248,11.752400,44.239811',
    stream=True
)



for line in r.iter_lines():
    if line:
		with open("twitterFlorence.json", "a") as myfile:
			myfile.write(line+',')