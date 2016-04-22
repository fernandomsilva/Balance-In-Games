import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap

def show_graph(A):
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

	A['TORONTO']['PITTSBURGH'][0]['owner'] = 0
	A['HELENA']['OMAHA'][0]['owner'] = 1

	#elarge=[(u,v) for (u,v,d) in A.edges(data=True) if d['weight'] >3]
	#esmall=[(u,v) for (u,v,d) in A.edges(data=True) if d['weight'] <=3]
	egray = [(u,v) for (u,v,d) in A.edges(data=True) if d['color'] == 'GRAY' and d['owner'] == -1]
	ered = [(u,v) for (u,v,d) in A.edges(data=True) if d['color'] == 'RED' and d['owner'] == -1]
	eblue = [(u,v) for (u,v,d) in A.edges(data=True) if d['color'] == 'BLUE' and d['owner'] == -1]
	eyellow = [(u,v) for (u,v,d) in A.edges(data=True) if d['color'] == 'YELLOW' and d['owner'] == -1]
	eorange = [(u,v) for (u,v,d) in A.edges(data=True) if d['color'] == 'ORANGE' and d['owner'] == -1]
	eblack = [(u,v) for (u,v,d) in A.edges(data=True) if d['color'] == 'BLACK' and d['owner'] == -1]
	ewhite = [(u,v) for (u,v,d) in A.edges(data=True) if d['color'] == 'WHITE' and d['owner'] == -1]
	epink = [(u,v) for (u,v,d) in A.edges(data=True) if d['color'] == 'PINK' and d['owner'] == -1]
	egreen = [(u,v) for (u,v,d) in A.edges(data=True) if d['color'] == 'GREEN' and d['owner'] == -1]
	eplayer1 = [(u,v) for (u,v,d) in A.edges(data=True) if d['owner'] == 0]
	eplayer2 = [(u,v) for (u,v,d) in A.edges(data=True) if d['owner'] == 1]
	eplayer3 = [(u,v) for (u,v,d) in A.edges(data=True) if d['owner'] == 2]

	#pos=nx.spring_layout(A) # positions for all nodes
	pos = {}
	pos_label = {}
	for x in map_coord:
		pos[x] = m(map_coord[x]['y'], map_coord[x]['x'])
		pos_label[x] = (pos[x][0], pos[x][1] + 100000.0)

	# nodes
	nx.draw_networkx_nodes(A,pos,node_size=200, node_color='red')

	# edges
	nx.draw_networkx_edges(A,pos,edgelist=egray,width=6,edge_color='#888888')
	nx.draw_networkx_edges(A,pos,edgelist=ered,width=6,edge_color='#ff0000')
	nx.draw_networkx_edges(A,pos,edgelist=eblue,width=6,edge_color='#00fbff')
	nx.draw_networkx_edges(A,pos,edgelist=eyellow,width=6,edge_color='#ffff00')
	nx.draw_networkx_edges(A,pos,edgelist=eorange,width=6,edge_color='#ff7700')
	nx.draw_networkx_edges(A,pos,edgelist=eblack,width=6,edge_color='#000000')
	nx.draw_networkx_edges(A,pos,edgelist=ewhite,width=6,edge_color='#ffffff')
	nx.draw_networkx_edges(A,pos,edgelist=epink,width=6,edge_color='#ff00dd')
	nx.draw_networkx_edges(A,pos,edgelist=egreen,width=6,edge_color='#00ff00')
	nx.draw_networkx_edges(A,pos,edgelist=eplayer1,width=6,edge_color='#0000ff',style='dashed')
	nx.draw_networkx_edges(A,pos,edgelist=eplayer2,width=6,edge_color='#84ff00',style='dashed')
	nx.draw_networkx_edges(A,pos,edgelist=eplayer3,width=6,edge_color='#c71414',style='dashed')
	#nx.draw_networkx_edges(A,pos,edgelist=elarge,width=6,edge_color='#00ff00')
	#nx.draw_networkx_edges(A,pos,edgelist=esmall,width=6,alpha=0.5,edge_color='#0000ff',style='dashed')
	# labels
	nx.draw_networkx_labels(A,pos=pos_label,font_size=20,font_family='sans-serif')
	#plt.text(pos['TORONTO'][0],pos['TORONTO'][1]+3.0,s='TORONTO', bbox=dict(facecolor='red', alpha=0.5), horizontalalignment='center')

	plt.axis('off')
	m.drawcountries()
	m.drawstates()
	#m.drawlsmask(land_color='coral',ocean_color='white',lakes=True)
	m.drawlsmask(land_color='coral',ocean_color='aqua',lakes=True)
	#m.drawcoastlines()
	#m.drawmapboundary(fill_color='aqua')
	#m.fillcontinents(lake_color='aqua')
	#plt.savefig("weighted_graph.png") # save as png
	plt.show() # display