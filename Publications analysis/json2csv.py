#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
with open ('author-extract.json') as f:
	data = json.loads(f.read())


f = open('ready4cartodb.csv','w+')
f.write('id, author, latitude, longitude\n')
for record in data['records']:
	for author in record['authors']:
		if 'latitude' in author.keys(): 
			f.write(str(author['id']) + ', ' + author['author'].replace(',',' ') + ', ' + str(author['latitude'])+ ', ' + str(author['longitude'])+'\n')