import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.basemap import Basemap as Basemap
import networkx as nx
from connections import *

data = {}
dataH = {}

full_data = {2: {('ATLANTA', 'MIAMI'): 20,
  ('ATLANTA', 'NASHVILLE'): 368,
  ('ATLANTA', 'NEW ORLEANS'): 69,
  ('BOSTON', 'MONTREAL'): 242,
  ('BOSTON', 'NEW YORK'): 315,
  ('CALGARY', 'SEATTLE'): 84,
  ('CHARLESTON', 'ATLANTA'): 207,
  ('CHARLESTON', 'MIAMI'): 25,
  ('CHICAGO', 'DULUTH'): 122,
  ('CHICAGO', 'PITTSBURGH'): 332,
  ('DALLAS', 'EL PASO'): 64,
  ('DALLAS', 'LITTLE ROCK'): 82,
  ('DALLAS', 'OKLAHOMA CITY'): 204,
  ('DENVER', 'HELENA'): 172,
  ('DENVER', 'SALT LAKE CITY'): 397,
  ('DENVER', 'SANTA FE'): 82,
  ('DULUTH', 'HELENA'): 98,
  ('DULUTH', 'SAULT ST. MARIE'): 146,
  ('DULUTH', 'WINNIPEG'): 44,
  ('EL PASO', 'LOS ANGELES'): 112,
  ('EL PASO', 'OKLAHOMA CITY'): 71,
  ('EL PASO', 'SANTA FE'): 52,
  ('HELENA', 'CALGARY'): 263,
  ('HELENA', 'DULUTH'): 70,
  ('HELENA', 'SALT LAKE CITY'): 91,
  ('HELENA', 'SEATTLE'): 182,
  ('HELENA', 'WINNIPEG'): 51,
  ('HOUSTON', 'DALLAS'): 468,
  ('HOUSTON', 'EL PASO'): 80,
  ('HOUSTON', 'NEW ORLEANS'): 142,
  ('KANSAS CITY', 'DENVER'): 277,
  ('KANSAS CITY', 'OKLAHOMA CITY'): 202,
  ('KANSAS CITY', 'SAINT LOUIS'): 398,
  ('LAS VEGAS', 'LOS ANGELES'): 165,
  ('LAS VEGAS', 'SALT LAKE CITY'): 250,
  ('LITTLE ROCK', 'DALLAS'): 216,
  ('LITTLE ROCK', 'NASHVILLE'): 149,
  ('LITTLE ROCK', 'NEW ORLEANS'): 178,
  ('LITTLE ROCK', 'OKLAHOMA CITY'): 243,
  ('LITTLE ROCK', 'SAINT LOUIS'): 337,
  ('LOS ANGELES', 'SAN FRANCISCO'): 156,
  ('MIAMI', 'ATLANTA'): 161,
  ('MIAMI', 'CHARLESTON'): 85,
  ('MIAMI', 'NEW ORLEANS'): 65,
  ('NASHVILLE', 'ATLANTA'): 102,
  ('NASHVILLE', 'LITTLE ROCK'): 7,
  ('NASHVILLE', 'PITTSBURGH'): 127,
  ('NASHVILLE', 'RALEIGH'): 91,
  ('NEW ORLEANS', 'ATLANTA'): 48,
  ('NEW YORK', 'MONTREAL'): 92,
  ('OKLAHOMA CITY', 'DENVER'): 101,
  ('OMAHA', 'CHICAGO'): 141,
  ('OMAHA', 'DENVER'): 180,
  ('OMAHA', 'DULUTH'): 405,
  ('OMAHA', 'HELENA'): 148,
  ('OMAHA', 'KANSAS CITY'): 484,
  ('PHOENIX', 'DENVER'): 77,
  ('PHOENIX', 'EL PASO'): 80,
  ('PHOENIX', 'LOS ANGELES'): 155,
  ('PHOENIX', 'SANTA FE'): 137,
  ('PITTSBURGH', 'NASHVILLE'): 37,
  ('PITTSBURGH', 'NEW YORK'): 400,
  ('PITTSBURGH', 'RALEIGH'): 305,
  ('PITTSBURGH', 'SAINT LOUIS'): 157,
  ('PITTSBURGH', 'WASHINGTON'): 325,
  ('PORTLAND', 'SALT LAKE CITY'): 8,
  ('PORTLAND', 'SAN FRANCISCO'): 138,
  ('PORTLAND', 'SEATTLE'): 366,
  ('RALEIGH', 'ATLANTA'): 284,
  ('RALEIGH', 'CHARLESTON'): 233,
  ('RALEIGH', 'NASHVILLE'): 3,
  ('RALEIGH', 'WASHINGTON'): 117,
  ('SAINT LOUIS', 'CHICAGO'): 330,
  ('SAINT LOUIS', 'NASHVILLE'): 322,
  ('SALT LAKE CITY', 'DENVER'): 36,
  ('SALT LAKE CITY', 'HELENA'): 139,
  ('SALT LAKE CITY', 'LAS VEGAS'): 48,
  ('SALT LAKE CITY', 'PORTLAND'): 201,
  ('SALT LAKE CITY', 'SAN FRANCISCO'): 193,
  ('SAN FRANCISCO', 'PORTLAND'): 14,
  ('SANTA FE', 'DENVER'): 75,
  ('SANTA FE', 'EL PASO'): 2,
  ('SANTA FE', 'OKLAHOMA CITY'): 160,
  ('SAULT ST. MARIE', 'MONTREAL'): 68,
  ('SEATTLE', 'PORTLAND'): 104,
  ('SEATTLE', 'VANCOUVER'): 273,
  ('TORONTO', 'CHICAGO'): 111,
  ('TORONTO', 'DULUTH'): 67,
  ('TORONTO', 'MONTREAL'): 383,
  ('TORONTO', 'PITTSBURGH'): 392,
  ('TORONTO', 'SAULT ST. MARIE'): 394,
  ('VANCOUVER', 'CALGARY'): 103,
  ('VANCOUVER', 'SEATTLE'): 127,
  ('WASHINGTON', 'NEW YORK'): 158,
  ('WASHINGTON', 'RALEIGH'): 37,
  ('WINNIPEG', 'CALGARY'): 31,
  ('WINNIPEG', 'SAULT ST. MARIE'): 78},
 3: {('ATLANTA', 'NASHVILLE'): 338,
  ('ATLANTA', 'NEW ORLEANS'): 64,
  ('BOSTON', 'MONTREAL'): 141,
  ('BOSTON', 'NEW YORK'): 276,
  ('CALGARY', 'SEATTLE'): 79,
  ('CALGARY', 'VANCOUVER'): 68,
  ('CHARLESTON', 'ATLANTA'): 35,
  ('CHARLESTON', 'MIAMI'): 80,
  ('CHICAGO', 'DULUTH'): 137,
  ('CHICAGO', 'PITTSBURGH'): 155,
  ('CHICAGO', 'SAINT LOUIS'): 249,
  ('DALLAS', 'EL PASO'): 48,
  ('DALLAS', 'OKLAHOMA CITY'): 126,
  ('DENVER', 'HELENA'): 184,
  ('DENVER', 'KANSAS CITY'): 232,
  ('DENVER', 'OKLAHOMA CITY'): 140,
  ('DENVER', 'PHOENIX'): 44,
  ('DENVER', 'SALT LAKE CITY'): 412,
  ('DENVER', 'SANTA FE'): 72,
  ('DULUTH', 'SAULT ST. MARIE'): 129,
  ('DULUTH', 'WINNIPEG'): 58,
  ('EL PASO', 'OKLAHOMA CITY'): 45,
  ('HELENA', 'CALGARY'): 309,
  ('HELENA', 'DULUTH'): 216,
  ('HELENA', 'SALT LAKE CITY'): 266,
  ('HELENA', 'SEATTLE'): 169,
  ('HELENA', 'WINNIPEG'): 57,
  ('HOUSTON', 'DALLAS'): 377,
  ('HOUSTON', 'EL PASO'): 129,
  ('HOUSTON', 'NEW ORLEANS'): 156,
  ('KANSAS CITY', 'DENVER'): 76,
  ('KANSAS CITY', 'OKLAHOMA CITY'): 164,
  ('KANSAS CITY', 'SAINT LOUIS'): 409,
  ('LAS VEGAS', 'LOS ANGELES'): 108,
  ('LITTLE ROCK', 'DALLAS'): 186,
  ('LITTLE ROCK', 'NEW ORLEANS'): 114,
  ('LITTLE ROCK', 'OKLAHOMA CITY'): 179,
  ('LITTLE ROCK', 'SAINT LOUIS'): 273,
  ('LOS ANGELES', 'EL PASO'): 155,
  ('LOS ANGELES', 'LAS VEGAS'): 55,
  ('LOS ANGELES', 'SAN FRANCISCO'): 166,
  ('MIAMI', 'ATLANTA'): 164,
  ('MIAMI', 'CHARLESTON'): 52,
  ('MIAMI', 'NEW ORLEANS'): 30,
  ('NASHVILLE', 'ATLANTA'): 47,
  ('NASHVILLE', 'LITTLE ROCK'): 118,
  ('NASHVILLE', 'RALEIGH'): 88,
  ('NASHVILLE', 'SAINT LOUIS'): 277,
  ('NEW ORLEANS', 'ATLANTA'): 91,
  ('NEW ORLEANS', 'LITTLE ROCK'): 69,
  ('NEW ORLEANS', 'MIAMI'): 45,
  ('NEW YORK', 'MONTREAL'): 99,
  ('NEW YORK', 'WASHINGTON'): 82,
  ('OKLAHOMA CITY', 'EL PASO'): 34,
  ('OMAHA', 'CHICAGO'): 156,
  ('OMAHA', 'DENVER'): 174,
  ('OMAHA', 'DULUTH'): 337,
  ('OMAHA', 'HELENA'): 164,
  ('OMAHA', 'KANSAS CITY'): 457,
  ('PHOENIX', 'DENVER'): 54,
  ('PHOENIX', 'EL PASO'): 84,
  ('PHOENIX', 'LOS ANGELES'): 117,
  ('PITTSBURGH', 'CHICAGO'): 219,
  ('PITTSBURGH', 'NASHVILLE'): 221,
  ('PITTSBURGH', 'NEW YORK'): 452,
  ('PITTSBURGH', 'RALEIGH'): 330,
  ('PITTSBURGH', 'SAINT LOUIS'): 178,
  ('PITTSBURGH', 'WASHINGTON'): 264,
  ('PORTLAND', 'SEATTLE'): 35,
  ('RALEIGH', 'ATLANTA'): 214,
  ('RALEIGH', 'CHARLESTON'): 195,
  ('SALT LAKE CITY', 'LAS VEGAS'): 284,
  ('SALT LAKE CITY', 'PORTLAND'): 210,
  ('SALT LAKE CITY', 'SAN FRANCISCO'): 213,
  ('SAN FRANCISCO', 'PORTLAND'): 200,
  ('SANTA FE', 'DENVER'): 34,
  ('SANTA FE', 'EL PASO'): 2,
  ('SANTA FE', 'OKLAHOMA CITY'): 123,
  ('SANTA FE', 'PHOENIX'): 99,
  ('SAULT ST. MARIE', 'MONTREAL'): 57,
  ('SEATTLE', 'PORTLAND'): 365,
  ('SEATTLE', 'VANCOUVER'): 249,
  ('TORONTO', 'CHICAGO'): 131,
  ('TORONTO', 'DULUTH'): 103,
  ('TORONTO', 'MONTREAL'): 383,
  ('TORONTO', 'PITTSBURGH'): 420,
  ('TORONTO', 'SAULT ST. MARIE'): 347,
  ('VANCOUVER', 'CALGARY'): 38,
  ('WASHINGTON', 'NEW YORK'): 55,
  ('WASHINGTON', 'RALEIGH'): 160,
  ('WINNIPEG', 'CALGARY'): 58,
  ('WINNIPEG', 'SAULT ST. MARIE'): 120},
 4: {('ATLANTA', 'NASHVILLE'): 364,
  ('BOSTON', 'MONTREAL'): 65,
  ('BOSTON', 'NEW YORK'): 161,
  ('CALGARY', 'SEATTLE'): 110,
  ('CALGARY', 'VANCOUVER'): 39,
  ('CHARLESTON', 'ATLANTA'): 26,
  ('CHICAGO', 'DULUTH'): 100,
  ('CHICAGO', 'PITTSBURGH'): 124,
  ('DALLAS', 'EL PASO'): 75,
  ('DALLAS', 'LITTLE ROCK'): 135,
  ('DALLAS', 'OKLAHOMA CITY'): 95,
  ('DENVER', 'HELENA'): 182,
  ('DENVER', 'KANSAS CITY'): 233,
  ('DENVER', 'OKLAHOMA CITY'): 114,
  ('DENVER', 'SALT LAKE CITY'): 38,
  ('DENVER', 'SANTA FE'): 66,
  ('DULUTH', 'SAULT ST. MARIE'): 135,
  ('DULUTH', 'WINNIPEG'): 63,
  ('EL PASO', 'LOS ANGELES'): 137,
  ('EL PASO', 'OKLAHOMA CITY'): 100,
  ('HELENA', 'CALGARY'): 328,
  ('HELENA', 'DULUTH'): 245,
  ('HELENA', 'SALT LAKE CITY'): 189,
  ('HELENA', 'SEATTLE'): 223,
  ('HOUSTON', 'DALLAS'): 367,
  ('HOUSTON', 'EL PASO'): 133,
  ('HOUSTON', 'NEW ORLEANS'): 63,
  ('KANSAS CITY', 'DENVER'): 38,
  ('KANSAS CITY', 'OKLAHOMA CITY'): 125,
  ('LAS VEGAS', 'LOS ANGELES'): 123,
  ('LITTLE ROCK', 'NEW ORLEANS'): 196,
  ('LITTLE ROCK', 'OKLAHOMA CITY'): 112,
  ('LITTLE ROCK', 'SAINT LOUIS'): 220,
  ('LOS ANGELES', 'EL PASO'): 43,
  ('LOS ANGELES', 'SAN FRANCISCO'): 138,
  ('MIAMI', 'ATLANTA'): 128,
  ('MIAMI', 'CHARLESTON'): 102,
  ('MIAMI', 'NEW ORLEANS'): 32,
  ('NASHVILLE', 'ATLANTA'): 3,
  ('NASHVILLE', 'LITTLE ROCK'): 153,
  ('NASHVILLE', 'RALEIGH'): 82,
  ('NEW ORLEANS', 'ATLANTA'): 91,
  ('NEW ORLEANS', 'MIAMI'): 106,
  ('NEW YORK', 'MONTREAL'): 98,
  ('OMAHA', 'CHICAGO'): 119,
  ('OMAHA', 'DENVER'): 154,
  ('OMAHA', 'DULUTH'): 307,
  ('OMAHA', 'HELENA'): 150,
  ('OMAHA', 'KANSAS CITY'): 499,
  ('PHOENIX', 'DENVER'): 82,
  ('PHOENIX', 'EL PASO'): 97,
  ('PHOENIX', 'LOS ANGELES'): 152,
  ('PHOENIX', 'SANTA FE'): 114,
  ('PITTSBURGH', 'CHICAGO'): 157,
  ('PITTSBURGH', 'NASHVILLE'): 233,
  ('PITTSBURGH', 'NEW YORK'): 331,
  ('PITTSBURGH', 'RALEIGH'): 222,
  ('PITTSBURGH', 'SAINT LOUIS'): 166,
  ('PITTSBURGH', 'WASHINGTON'): 179,
  ('PORTLAND', 'SALT LAKE CITY'): 172,
  ('PORTLAND', 'SAN FRANCISCO'): 154,
  ('PORTLAND', 'SEATTLE'): 373,
  ('RALEIGH', 'ATLANTA'): 133,
  ('RALEIGH', 'CHARLESTON'): 107,
  ('SAINT LOUIS', 'CHICAGO'): 204,
  ('SAINT LOUIS', 'KANSAS CITY'): 330,
  ('SAINT LOUIS', 'NASHVILLE'): 274,
  ('SALT LAKE CITY', 'DENVER'): 365,
  ('SALT LAKE CITY', 'LAS VEGAS'): 253,
  ('SALT LAKE CITY', 'PORTLAND'): 108,
  ('SALT LAKE CITY', 'SAN FRANCISCO'): 150,
  ('SAN FRANCISCO', 'PORTLAND'): 11,
  ('SANTA FE', 'EL PASO'): 4,
  ('SANTA FE', 'OKLAHOMA CITY'): 158,
  ('SAULT ST. MARIE', 'MONTREAL'): 58,
  ('SAULT ST. MARIE', 'WINNIPEG'): 28,
  ('TORONTO', 'CHICAGO'): 134,
  ('TORONTO', 'DULUTH'): 251,
  ('TORONTO', 'MONTREAL'): 382,
  ('TORONTO', 'PITTSBURGH'): 463,
  ('TORONTO', 'SAULT ST. MARIE'): 318,
  ('VANCOUVER', 'CALGARY'): 46,
  ('VANCOUVER', 'SEATTLE'): 232,
  ('WASHINGTON', 'NEW YORK'): 41,
  ('WASHINGTON', 'RALEIGH'): 63,
  ('WINNIPEG', 'CALGARY'): 137,
  ('WINNIPEG', 'HELENA'): 56,
  ('WINNIPEG', 'SAULT ST. MARIE'): 327}}


#for key in dataH:
#    if key not in data:
#        data[key] = dataH[key]
#    else:
#        data[key] += dataH[key]
data = full_data[4]

x = sorted(data.values())

y = []
visited = []

#x2 = [] 

for val in x:
    for key in data:
        if val not in visited and data[key] == val:
            y.append(key)
    visited.append(val)

z = []
    
for temp in y:
    #temp = name.split(',')
    for k in connections:
        if temp[0] == k[0]:
            if k[2] == temp[1]:
                z.append(str(temp) + " (" + str(k[1]) + ")")
                break
        if k[2] == temp[0]:
            if k[0] == temp[1]:
                z.append(str(temp) + " (" + str(k[1]) + ")")
                break

#print len(y)
#print len(z)
        
#for route in y:
#    if route in dataH:
#        x2.append(dataH[route])
#    else:
#        x2.append(0)

temp_x = x[:6] + x[-6:]
temp_z = z[:6] + z[-6:]
#print temp_x
#print temp_z


#widthscale = len(data)/4 
widthscale = len(temp_x)/4
figsize = (2*widthscale,15) # fig size in inches (width,height)
figure = pylab.figure(figsize = figsize) # set the figsize

ax = figure.add_subplot(1,1,1)

#ax.bar(range(len(data)), x, .5, align='center')
#ax.set_xticks(range(len(data)))
#ax.set_xticklabels(z)
ax.bar(range(len(temp_x)), temp_x, .5, align='center')
ax.set_xticks(range(len(temp_x)))
ax.set_xticklabels(temp_z, size=20)
ax.set_yticklabels([0, 100, 200, 300, 400, 500], size=30)

for label in ax.get_xticklabels(): 
      label.set_horizontalalignment('center') 

figure.autofmt_xdate(rotation=45)

pylab.show()
plt.show()
