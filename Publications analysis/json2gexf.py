#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx as nx
import json
with open ('author-extract.json') as f:
	data = json.loads(f.read())

G=nx.Graph()

for record in data['records']:
	ids=[]
	i=0
	for author in record['authors']:
		G.add_node(author['id'], name=author['author'].replace(',',' '))
		
		if 'latitude' in author.keys(): 
			G.node[author['id']]['latitude'] = author['latitude']
		if 'longitude' in author.keys(): 
			G.node[author['id']]['longitude'] = author['longitude']	

		ids.append(author['id'])

	for author in record['authors']:
		for p1 in range(len(ids)):
			for p2 in range(p1+1,len(ids)):
				G.add_edge(ids[p1],ids[p2])

nx.write_gexf(G, "author-graph.gexf")

