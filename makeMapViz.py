import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.basemap import Basemap as Basemap
import networkx as nx
from loadgraphfile import *
from mapCoord import *

data2 = {}

data2['PESHAWAR'] = 271
data2['LUCKNOW'] = 30
data2['BHATINDA'] = 9
data2['DHUBRI'] = 171
data2['WADI'] = 128
data2['MANGALORE'] = 14
data2['AGRA'] = 34
data2['QUILON'] = 1
data2['JODHPUR'] = 32
data2['RATIAM'] = 80
data2['BEZWADA'] = 37
data2['BILASPUR'] = 2
data2['WALTAIN'] = 4
data2['LAHORE'] = 11
data2['BAREILLY'] = 4
data2['MANMAD'] = 14
data2['GUNTAKAL'] = 49
data2['POONA'] = 82
data2['PATNA'] = 4
data2['JARHAT'] = 200
data2['MORMUGAU'] = 65
data2['JAIPUR'] = 44
data2['DELHI'] = 14
data2['JACOBABAD'] = 7
data2['RAIPUR'] = 6
data2['AMBALA'] = 7
data2['KHANDWA'] = 4
data2['AHMADABAD'] = 18
data2['KATNI'] = 10
data2['INDUR'] = 305
data2['ROHRI'] = 116
data2['BHOPAL'] = 63
data2['BOMBAY'] = 0
data2['KARACHI'] = 0
data2['CALICUT'] = 0
data2['ERODE'] = 0
data2['MADRAS'] = 0
data2['CALCUTTA'] = 0
data2['CHITTAGONG'] = 0

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
m = Basemap(
			projection='merc',
			llcrnrlon=65,
			llcrnrlat=8,
			urcrnrlon=96,
			urcrnrlat=35,
			lat_ts=0,
			resolution='i',
			suppress_ticks=True)


A = loadgraphfromfile('india.txt')

map_coord = map_coord_india

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
