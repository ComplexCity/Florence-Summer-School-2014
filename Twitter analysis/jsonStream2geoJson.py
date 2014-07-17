#!/usr/bin/python
# -*- coding: utf-8 -*-

from geojson import Feature, Point, FeatureCollection
import geojson
import json
import io

f = open('twitterFlorence.json')
rawData = f.read()
data = json.loads(rawData)

tweets = []

for tweet in data['tweets']:
	if tweet['coordinates']:
		the_point = Point((tweet['coordinates']['coordinates'][0], tweet['coordinates']['coordinates'][1]))
		the_text = tweet['text']
		the_time = tweet['created_at']
		the_language = tweet['lang']
		the_id = tweet['id']
		the_feature = Feature(id=the_id, geometry=the_point, properties={"time": the_time,"language":the_language})#,"text":the_text})
		tweets.append(the_feature)

with io.open('data/twitterFlorence.geojson', 'w', encoding='utf-8') as f:
  f.write(unicode(geojson.dumps(FeatureCollection(tweets))))