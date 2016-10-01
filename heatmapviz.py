import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.basemap import Basemap as Basemap
import networkx as nx
from loadgraphfile import *

data2 = {}

data2['TORONTO'] = 4039
data2['OMAHA'] = 319
data2['PITTSBURGH'] = 1169
data2['BOSTON'] = 3250
data2['LITTLE ROCK'] = 2764
data2['SAINT LOUIS'] = 2236
data2['HELENA'] = 1964
data2['NEW YORK'] = 1509
data2['SALT LAKE CITY'] = 4308
data2['RALEIGH'] = 2259
data2['HOUSTON'] = 238
data2['DALLAS'] = 818
data2['DENVER'] = 391
data2['WINNIPEG'] = 4112
data2['EL PASO'] = 1098
data2['LAS VEGAS'] = 8133
data2['LOS ANGELES'] = 1859
data2['CHARLESTON'] = 1916
data2['ATLANTA'] = 289
data2['SEATTLE'] = 817
data2['SAULT ST. MARIE'] = 4205
data2['CHICAGO'] = 1775
data2['MIAMI'] = 5062
data2['SANTA FE'] = 4029
data2['WASHINGTON'] = 8981
data2['KANSAS CITY'] = 815
data2['VANCOUVER'] = 1222
data2['CALGARY'] = 3162
data2['SAN FRANCISCO'] = 4706
data2['PORTLAND'] = 935
data2['PHOENIX'] = 2062
data2['NASHVILLE'] = 227
data2['DULUTH'] = 3062
data2['NEW ORLEANS'] = 3376
data2['OKLAHOMA CITY'] = 3104
data2['MONTREAL'] = 1344

max_val = 0

for key in data2:
    if max_val < data2[key]:
        max_val = data2[key]

color_data = {}

for key in data2:
    color_data[key] = float(data2[key]) / float(10000)

#print color_data

m = Basemap(
			projection='merc',
			llcrnrlon=-130,
			llcrnrlat=24,
			urcrnrlon=-60,
			urcrnrlat=53,
			lat_ts=0,
			resolution='i',
			suppress_ticks=True)

map_coord = {'VANCOUVER': {'x': 49.564963, 'y': -123.062702},
	'CALGARY': {'x': 51.251020, 'y': -114.026557},
	'WINNIPEG': {'x': 50.010978, 'y': -97.154732},
	'SAULT ST. MARIE': {'x': 46.791630, 'y': -84.286244},
	'MONTREAL': {'x': 45.503987, 'y': -73.568746},
	'SEATTLE': {'x': 47.589454, 'y': -122.318512},
	'TORONTO': {'x': 43.641723, 'y': -79.387558},
	'BOSTON': {'x': 42.355750, 'y': -71.055807},
	'HELENA': {'x': 46.731739, 'y': -112.027148},
	'DULUTH': {'x': 46.888493, 'y': -92.078888},
	'PORTLAND': {'x': 45.509640, 'y': -122.654604},
	'NEW YORK': {'x': 40.692428, 'y': -73.998671},
	'PITTSBURGH': {'x': 40.413313, 'y': -79.993355},
	'CHICAGO': {'x': 41.852272, 'y': -87.629942},
	'OMAHA': {'x': 41.254117, 'y': -95.997963},
	'WASHINGTON': {'x': 38.894640, 'y': -77.042346},
	'SAINT LOUIS': {'x': 38.622955, 'y': -90.200017},
	'KANSAS CITY': {'x': 39.094362, 'y': -94.586185},
	'DENVER': {'x': 39.728466, 'y': -104.989352},
	'SALT LAKE CITY': {'x': 40.751569, 'y': -111.902025},
	'SAN FRANCISCO': {'x': 37.779881, 'y': -122.428586},
	'RALEIGH': {'x': 35.775136, 'y': -78.638468},
	'NASHVILLE': {'x': 36.179663, 'y': -86.791265},
	'LITTLE ROCK': {'x': 34.755320, 'y': -92.290129},
	'OKLAHOMA CITY': {'x': 35.473889, 'y': -97.508375},
	'SANTA FE': {'x': 35.687297, 'y': -105.935572},
	'LAS VEGAS': {'x': 36.174911, 'y': -115.146240},
	'LOS ANGELES': {'x': 34.073030, 'y': -118.276788},
	'PHOENIX': {'x': 33.447244, 'y': -112.071539},
	'EL PASO': {'x': 31.751809, 'y': -106.488188},
	'DALLAS': {'x': 32.757476, 'y': -96.792232},
	'ATLANTA': {'x': 33.754522, 'y': -84.391658},
	'CHARLESTON': {'x': 32.791175, 'y': -79.935731},
	'MIAMI': {'x': 25.763988, 'y': -80.193837},
	'NEW ORLEANS': {'x': 29.985846, 'y': -90.082514},
	'HOUSTON': {'x': 29.829152, 'y': -95.365634}}

A = loadgraphfromfile('usa.txt')

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
        color = pylab.cm.Oranges(color_data[node])
        c = [color[0], color[1], color[2], color[3]]
        nx.draw_networkx_nodes(G,pos,node_size=2000, node_color=c)
    else:
        G.add_node(node)
        nx.draw_networkx_nodes(G,pos,node_size=2000, node_color='#ff0000')
        
nx.draw_networkx_edges(A,pos,edgelist=A.edges(),width=2,edge_color='#0000ff')
nx.draw_networkx_labels(A,pos=pos_label,font_size=20,font_family='sans-serif')

plt.show()