import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.basemap import Basemap as Basemap
import networkx as nx
from loadgraphfile import *
from mapCoord import *

data2 = {}

data2["TORONTO"] = 7
data2["OMAHA"] = 14
data2["BOSTON"] = 241
data2["PITTSBURGH"] = 0
data2["HELENA"] = 0
data2["LITTLE ROCK"] = 112
data2["SAINT LOUIS"] = 22
data2["NEW YORK"] = 35
data2["SALT LAKE CITY"] = 9
data2["RALEIGH"] = 52
data2["HOUSTON"] = 36
data2["DALLAS"] = 68
data2["DENVER"] = 4
data2["WINNIPEG"] = 53
data2["EL PASO"] = 66
data2["LAS VEGAS"] = 209
data2["LOS ANGELES"] = 96
data2["CHARLESTON"] = 220
data2["ATLANTA"] = 22
data2["SEATTLE"] = 34
data2["SAULT ST. MARIE"] = 15
data2["CHICAGO"] = 23
data2["MIAMI"] = 165
data2["SANTA FE"] = 472
data2["WASHINGTON"] = 176
data2["KANSAS CITY"] = 4
data2["VANCOUVER"] = 245
data2["CALGARY"] = 111
data2["SAN FRANCISCO"] = 214
data2["PORTLAND"] = 56
data2["PHOENIX"] = 312
data2["NASHVILLE"] = 12
data2["DULUTH"] = 5
data2["NEW ORLEANS"] = 76
data2["OKLAHOMA CITY"] = 106
data2["MONTREAL"] = 98

max_val = 0

for key in data2:
    if max_val < data2[key]:
        max_val = data2[key]

color_data = {}

for key in data2:
    color_data[key] = float(data2[key]) / float(1000)

#print color_data

#USA
'''m = Basemap(
			projection='merc',
			llcrnrlon=-130,
			llcrnrlat=24,
			urcrnrlon=-60,
			urcrnrlat=53,
			lat_ts=0,
			resolution='i',
			suppress_ticks=True)'''

#India
'''m = Basemap(
			projection='merc',
			llcrnrlon=65,
			llcrnrlat=8,
			urcrnrlon=96,
			urcrnrlat=35,
			lat_ts=0,
			resolution='i',
			suppress_ticks=True)
'''
#Europe
'''
m = Basemap(
			projection='merc',
			llcrnrlon=-11,
			llcrnrlat=34,
			urcrnrlon=43,
			urcrnrlat=61,
			lat_ts=0,
			resolution='i',
			suppress_ticks=True)
'''

#Japan
m = Basemap(
			projection='merc',
			llcrnrlon=126,
			llcrnrlat=24,
			urcrnrlon=144,
			urcrnrlat=45,
			lat_ts=0,
			resolution='i',
			suppress_ticks=True)

#Brazil
'''m = Basemap(
			projection='merc',
			llcrnrlon=-73,
			llcrnrlat=-32,
			urcrnrlon=-33,
			urcrnrlat=4,
			lat_ts=0,
			resolution='i',
			suppress_ticks=True)'''

A = loadgraphfromfile('japan.txt')

for key in A.nodes():
	if key not in data2:
		data2[key] = 0

map_coord = map_coord_japan
keys = map_coord.keys()
for key in keys:
	map_coord[key.upper()] = map_coord[key]

pos = {}
pos_label = {}
for x in map_coord:
	pos[x] = m(map_coord[x]['y'], map_coord[x]['x'])
	pos_label[x] = (pos[x][0], pos[x][1] + 100000.0)

m.drawcoastlines()
m.drawcountries()
#m.drawstates()

# nodes
'''
for node in A:
    G = nx.Graph()
    if node in color_data:
        G.add_node(node)
        color = pylab.cm.OrRd(color_data[node])
        c = [color[0], color[1], color[2], color[3]]
        nx.draw_networkx_nodes(G,pos,node_size=1000, node_color=c)
    else:
        G.add_node(node)
        nx.draw_networkx_nodes(G,pos,node_size=1000, node_color='#ff0000')
'''
nx.draw_networkx_nodes(A,pos,node_size=1000, node_color='#ff0000')
nx.draw_networkx_edges(A,pos,edgelist=A.edges(),width=2,edge_color='#0000ff')
nx.draw_networkx_labels(A,pos=pos_label,font_size=20,font_family='sans-serif')

plt.show()
