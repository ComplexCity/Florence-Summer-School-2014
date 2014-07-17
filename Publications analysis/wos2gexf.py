#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import re
from dateutil import parser
from datetime import *
import json

# 1 extraire 1 article avec auteurs et extraire affiliation city

def look4cities(haystack):
	try:
		conn = psycopg2.connect(dbname='geonames', user='postgres')
		cur = conn.cursor()

		haystack = haystack.replace(',', ' , ')
		haystack = re.sub("(\\s|,|;)??(([a-z]*?|[A-Z]*?)*?(-)??([0-9])+?)(-)??([a-z]*?|[A-Z]*?)*?(\\s|,|;){1}?", "", haystack)
		
		haystack = haystack.split(',')[::-1]
		print haystack

		for possibleLocation in haystack:
			possibleLocation = possibleLocation.strip()
			if possibleLocation.find(' ') and len(possibleLocation.split()[0]) == 2 and possibleLocation.split()[0].isupper():
				possibleLocation = possibleLocation[3:]

			cur.execute("SELECT name, latitude, longitude from geoname where name = %s order by length(alternatenames) DESC NULLS LAST", (possibleLocation,))
			row = cur.fetchone()

			if row != None:
				return row
		 
		for possibleLocation in haystack:
			possibleLocation = possibleLocation.strip()
			possibleLocation= possibleLocation.replace('=', '==').replace('%', '=%').replace('_', '=_')
			sql= "SELECT name, latitude, longitude FROM geoname WHERE alternatenames LIKE %(like)s ESCAPE '='"
			cur.execute(sql, dict(like= '%'+possibleLocation+'%'))
			row = cur.fetchone()

			if row != None:
				return row

		return ('unkown',0,0)

	except:
		print "I am unable to connect to the database"
		return ('unkown',0,0)


with open('webofscience-extract.txt') as f:
	haystack = f.readlines()

isAuthor = False
isAffiliation = False
i = 0
records = {'records':[]}

for hay in haystack:
		if hay.find('PT') == 0:
			node=[]
			print "new record" 
			record = {'authors':[], 'date':0}
			date=''

		##### the authors ######
		if hay.find('AF') == 0:
			isAuthor = True
			authors = []
			authors.append({'author':hay[3:].strip(), 'id':i})
			i+=1
			continue

		if hay.find('TI') == 0:
			isAuthor = False
		
		if isAuthor:
			authors.append({'author':hay.strip(),'id':i})
			i+=1

		##### the affiliation ######
		if hay.find('C1') == 0:
			isAffiliation = True

		if isAffiliation:
			for author in authors:
				if hay.find(author['author']) > 0:
					author['affiliation'] = hay[hay.find(']')+1:]
					city = look4cities(author['affiliation'])
					author['city'] = city[0]
					author['latitude'] = city[1]
					author['longitude'] = city[2]
		
		if hay.find('RP') == 0:
			isAffiliation = False

		if hay.find('PD') == 0:
			date = hay[3:]

		if hay.find('PY') == 0:
			date = date + ' ' + hay[3:]
			try:
				dt = parser.parse(date)
			except:
				dt = parser.parse(hay[3:])
			date = dt.date().isoformat()

		if hay.find('ER') == 0:
			record['authors'] = authors
			record['date'] = date 
			
			records['records'].append(record)

			print "end record"


with open("author-extract.json", "w+") as myfile:
			myfile.write(json.dumps(records))

# {'record' = [
# 	{'authors'=[
# 		{'author':'pouet','affiliation':'poum'},
# 		{'author':'pouet','affiliation':'poum'}
# 		]}
# 	]}

