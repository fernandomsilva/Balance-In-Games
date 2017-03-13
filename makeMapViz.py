import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.basemap import Basemap as Basemap
import networkx as nx
from loadgraphfile import *
from mapCoord import *

data2 = {}

data2['SOFIA'] = 251
data2['PALERMO'] = 25
data2['MADRID'] = 82
data2['ATHINA'] = 128
data2['SMYRNA'] = 34
data2['KOBENHAVN'] = 98
data2['BERLIN'] = 1
data2['CONSTANTINOPLE'] = 50
data2['LONDON'] = 305
data2['STOCKHOLM'] = 31
data2['LISBOA'] = 496
data2['ANGORA'] = 307
data2['MARSEILLE'] = 51
data2['ROSTOV'] = 265
data2['WIEN'] = 14
data2['EDINBURGH'] = 441
data2['BUDAPEST'] = 6
data2['WILNO'] = 38
data2['BUCURESTI'] = 58
data2['KHARKOV'] = 331
data2['BRUXELLES'] = 198
data2['MUNCHEN'] = 267
data2['SARAJEVO'] = 368
data2['ROMA'] = 34
data2['BREST'] = 327
data2['WARSZAWA'] = 28
data2['ESSEN'] = 55
data2['DANZIG'] = 47
data2['ERZURUM'] = 344
data2['ZAGRAB'] = 132
data2['BRINDISI'] = 133
data2['ZURICH'] = 161
data2['CADIZ'] = 505
data2['SOCHI'] = 519
data2['BARCELONA'] = 229
data2['PETROGRAD'] = 21
data2['AMSTERDAM'] = 133
data2['FRANKFURT'] = 8
data2['MOSKVA'] = 286
data2['PAMPLONA'] = 79
data2['SEVASTOPOL'] = 128
data2['RIGA'] = 332
data2['DIEPPE'] = 168
data2['KYIV'] = 10
data2['VENEZIA'] = 128
data2['SMOLENSK'] = 212
data2['PARIS'] = 1

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
			suppress_ticks=True)
'''
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
m = Basemap(
			projection='merc',
			llcrnrlon=-11,
			llcrnrlat=34,
			urcrnrlon=43,
			urcrnrlat=61,
			lat_ts=0,
			resolution='i',
			suppress_ticks=True)


A = loadgraphfromfile('europe.txt')

for key in A.nodes():
	if key not in data2:
		data2[key] = 0

map_coord = map_coord_europe

pos = {}
pos_label = {}
for x in map_coord:
	pos[x] = m(map_coord[x]['y'], map_coord[x]['x'])
	pos_label[x] = (pos[x][0], pos[x][1] + 100000.0)

m.drawcoastlines()
m.drawcountries()
#m.drawstates()

# nodes
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
        
nx.draw_networkx_edges(A,pos,edgelist=A.edges(),width=2,edge_color='#0000ff')
nx.draw_networkx_labels(A,pos=pos_label,font_size=20,font_family='sans-serif')

plt.show()
