import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.basemap import Basemap as Basemap
import networkx as nx
from connections import *

data = {}
dataH = {}

full_data = {2: {('BOSTON', 'MONTREAL'): 164,
  ('BOSTON', 'NEW YORK'): 171,
  ('CALGARY', 'SEATTLE'): 86,
  ('CHARLESTON', 'ATLANTA'): 157,
  ('CHARLESTON', 'MIAMI'): 24,
  ('CHICAGO', 'DULUTH'): 125,
  ('CHICAGO', 'PITTSBURGH'): 45,
  ('CHICAGO', 'SAINT LOUIS'): 182,
  ('DALLAS', 'EL PASO'): 140,
  ('DALLAS', 'OKLAHOMA CITY'): 181,
  ('DENVER', 'HELENA'): 124,
  ('DENVER', 'OKLAHOMA CITY'): 85,
  ('DENVER', 'SALT LAKE CITY'): 251,
  ('DENVER', 'SANTA FE'): 89,
  ('DULUTH', 'WINNIPEG'): 13,
  ('EL PASO', 'LOS ANGELES'): 64,
  ('EL PASO', 'OKLAHOMA CITY'): 70,
  ('HELENA', 'CALGARY'): 273,
  ('HELENA', 'DENVER'): 77,
  ('HELENA', 'DULUTH'): 101,
  ('HELENA', 'SALT LAKE CITY'): 200,
  ('HELENA', 'SEATTLE'): 201,
  ('HELENA', 'WINNIPEG'): 22,
  ('HOUSTON', 'DALLAS'): 500,
  ('HOUSTON', 'EL PASO'): 124,
  ('HOUSTON', 'NEW ORLEANS'): 208,
  ('KANSAS CITY', 'DENVER'): 148,
  ('KANSAS CITY', 'OKLAHOMA CITY'): 232,
  ('KANSAS CITY', 'SAINT LOUIS'): 265,
  ('LAS VEGAS', 'LOS ANGELES'): 115,
  ('LAS VEGAS', 'SALT LAKE CITY'): 22,
  ('LITTLE ROCK', 'DALLAS'): 248,
  ('LITTLE ROCK', 'NEW ORLEANS'): 168,
  ('LITTLE ROCK', 'OKLAHOMA CITY'): 257,
  ('LITTLE ROCK', 'SAINT LOUIS'): 298,
  ('LOS ANGELES', 'EL PASO'): 129,
  ('LOS ANGELES', 'SAN FRANCISCO'): 257,
  ('MIAMI', 'ATLANTA'): 93,
  ('MIAMI', 'CHARLESTON'): 108,
  ('MIAMI', 'NEW ORLEANS'): 95,
  ('NASHVILLE', 'ATLANTA'): 434,
  ('NASHVILLE', 'LITTLE ROCK'): 188,
  ('NASHVILLE', 'RALEIGH'): 80,
  ('NASHVILLE', 'SAINT LOUIS'): 233,
  ('NEW ORLEANS', 'ATLANTA'): 140,
  ('NEW YORK', 'MONTREAL'): 125,
  ('OMAHA', 'CHICAGO'): 164,
  ('OMAHA', 'DENVER'): 195,
  ('OMAHA', 'DULUTH'): 391,
  ('OMAHA', 'HELENA'): 139,
  ('OMAHA', 'KANSAS CITY'): 517,
  ('PHOENIX', 'DENVER'): 157,
  ('PHOENIX', 'EL PASO'): 159,
  ('PHOENIX', 'LOS ANGELES'): 253,
  ('PHOENIX', 'SANTA FE'): 168,
  ('PITTSBURGH', 'CHICAGO'): 235,
  ('PITTSBURGH', 'NASHVILLE'): 210,
  ('PITTSBURGH', 'NEW YORK'): 375,
  ('PITTSBURGH', 'RALEIGH'): 293,
  ('PITTSBURGH', 'SAINT LOUIS'): 140,
  ('PITTSBURGH', 'WASHINGTON'): 223,
  ('PORTLAND', 'SEATTLE'): 361,
  ('RALEIGH', 'ATLANTA'): 246,
  ('RALEIGH', 'CHARLESTON'): 194,
  ('SAINT LOUIS', 'CHICAGO'): 63,
  ('SALT LAKE CITY', 'LAS VEGAS'): 82,
  ('SALT LAKE CITY', 'PORTLAND'): 108,
  ('SALT LAKE CITY', 'SAN FRANCISCO'): 114,
  ('SAN FRANCISCO', 'PORTLAND'): 230,
  ('SANTA FE', 'DENVER'): 164,
  ('SANTA FE', 'EL PASO'): 152,
  ('SANTA FE', 'OKLAHOMA CITY'): 219,
  ('SAULT ST. MARIE', 'DULUTH'): 170,
  ('SAULT ST. MARIE', 'MONTREAL'): 120,
  ('SAULT ST. MARIE', 'WINNIPEG'): 121,
  ('SEATTLE', 'PORTLAND'): 107,
  ('SEATTLE', 'VANCOUVER'): 127,
  ('TORONTO', 'CHICAGO'): 125,
  ('TORONTO', 'DULUTH'): 48,
  ('TORONTO', 'MONTREAL'): 406,
  ('TORONTO', 'PITTSBURGH'): 415,
  ('TORONTO', 'SAULT ST. MARIE'): 375,
  ('VANCOUVER', 'CALGARY'): 130,
  ('VANCOUVER', 'SEATTLE'): 269,
  ('WASHINGTON', 'NEW YORK'): 88,
  ('WASHINGTON', 'RALEIGH'): 43,
  ('WINNIPEG', 'CALGARY'): 97,
  ('WINNIPEG', 'DULUTH'): 108,
  ('WINNIPEG', 'HELENA'): 57},
 4: {('BOSTON', 'MONTREAL'): 37,
  ('BOSTON', 'NEW YORK'): 60,
  ('CALGARY', 'SEATTLE'): 82,
  ('CHARLESTON', 'ATLANTA'): 7,
  ('CHICAGO', 'DULUTH'): 153,
  ('CHICAGO', 'PITTSBURGH'): 222,
  ('CHICAGO', 'SAINT LOUIS'): 145,
  ('DALLAS', 'LITTLE ROCK'): 119,
  ('DALLAS', 'OKLAHOMA CITY'): 59,
  ('DENVER', 'HELENA'): 380,
  ('DENVER', 'OKLAHOMA CITY'): 322,
  ('DENVER', 'SALT LAKE CITY'): 178,
  ('DULUTH', 'WINNIPEG'): 34,
  ('EL PASO', 'DALLAS'): 134,
  ('EL PASO', 'LOS ANGELES'): 209,
  ('EL PASO', 'OKLAHOMA CITY'): 263,
  ('EL PASO', 'PHOENIX'): 72,
  ('HELENA', 'CALGARY'): 288,
  ('HELENA', 'DULUTH'): 350,
  ('HELENA', 'SALT LAKE CITY'): 147,
  ('HELENA', 'SEATTLE'): 238,
  ('HELENA', 'WINNIPEG'): 34,
  ('HOUSTON', 'DALLAS'): 271,
  ('HOUSTON', 'EL PASO'): 216,
  ('HOUSTON', 'NEW ORLEANS'): 71,
  ('KANSAS CITY', 'DENVER'): 150,
  ('KANSAS CITY', 'OKLAHOMA CITY'): 88,
  ('KANSAS CITY', 'SAINT LOUIS'): 158,
  ('LAS VEGAS', 'LOS ANGELES'): 55,
  ('LITTLE ROCK', 'NEW ORLEANS'): 59,
  ('LITTLE ROCK', 'OKLAHOMA CITY'): 129,
  ('LITTLE ROCK', 'SAINT LOUIS'): 182,
  ('LOS ANGELES', 'SAN FRANCISCO'): 202,
  ('MIAMI', 'ATLANTA'): 63,
  ('MIAMI', 'CHARLESTON'): 75,
  ('MIAMI', 'NEW ORLEANS'): 99,
  ('NASHVILLE', 'ATLANTA'): 231,
  ('NASHVILLE', 'LITTLE ROCK'): 217,
  ('NASHVILLE', 'RALEIGH'): 37,
  ('NASHVILLE', 'SAINT LOUIS'): 137,
  ('NEW ORLEANS', 'ATLANTA'): 95,
  ('NEW ORLEANS', 'LITTLE ROCK'): 130,
  ('NEW YORK', 'MONTREAL'): 103,
  ('OMAHA', 'CHICAGO'): 164,
  ('OMAHA', 'DENVER'): 185,
  ('OMAHA', 'DULUTH'): 232,
  ('OMAHA', 'HELENA'): 112,
  ('OMAHA', 'KANSAS CITY'): 350,
  ('PHOENIX', 'DENVER'): 207,
  ('PHOENIX', 'EL PASO'): 53,
  ('PHOENIX', 'LOS ANGELES'): 300,
  ('PHOENIX', 'SANTA FE'): 117,
  ('PITTSBURGH', 'CHICAGO'): 102,
  ('PITTSBURGH', 'NASHVILLE'): 270,
  ('PITTSBURGH', 'NEW YORK'): 253,
  ('PITTSBURGH', 'RALEIGH'): 166,
  ('PITTSBURGH', 'SAINT LOUIS'): 94,
  ('PITTSBURGH', 'WASHINGTON'): 84,
  ('PORTLAND', 'SEATTLE'): 5,
  ('RALEIGH', 'ATLANTA'): 79,
  ('RALEIGH', 'CHARLESTON'): 74,
  ('SALT LAKE CITY', 'LAS VEGAS'): 79,
  ('SALT LAKE CITY', 'PORTLAND'): 193,
  ('SALT LAKE CITY', 'SAN FRANCISCO'): 19,
  ('SAN FRANCISCO', 'PORTLAND'): 191,
  ('SAN FRANCISCO', 'SALT LAKE CITY'): 72,
  ('SANTA FE', 'DENVER'): 128,
  ('SANTA FE', 'EL PASO'): 84,
  ('SANTA FE', 'OKLAHOMA CITY'): 180,
  ('SAULT ST. MARIE', 'DULUTH'): 207,
  ('SAULT ST. MARIE', 'MONTREAL'): 91,
  ('SEATTLE', 'PORTLAND'): 250,
  ('TORONTO', 'CHICAGO'): 168,
  ('TORONTO', 'DULUTH'): 287,
  ('TORONTO', 'MONTREAL'): 325,
  ('TORONTO', 'PITTSBURGH'): 349,
  ('TORONTO', 'SAULT ST. MARIE'): 233,
  ('VANCOUVER', 'CALGARY'): 83,
  ('VANCOUVER', 'SEATTLE'): 159,
  ('WASHINGTON', 'NEW YORK'): 6,
  ('WINNIPEG', 'CALGARY'): 119,
  ('WINNIPEG', 'DULUTH'): 84,
  ('WINNIPEG', 'HELENA'): 26,
  ('WINNIPEG', 'SAULT ST. MARIE'): 495},
5: {('ATLANTA', 'MIAMI'): 20,
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
 6: {('ATLANTA', 'NASHVILLE'): 364,
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
data = full_data[2]
data2 = full_data[4]
data3 = full_data[5]
data4 = full_data[6]

x = sorted(data.values())
x2 = sorted(data2.values())
x3 = sorted(data3.values())
x4 = sorted(data4.values())

y = []
y2 = []
y3 = []
y4 = []
visited = []

#x2 = [] 

for val in x:
    for key in data:
        if val not in visited and data[key] == val:
            y.append(key)
    visited.append(val)

visited = []

for val in x2:
    for key in data2:
        if val not in visited and data2[key] == val:
            y2.append(key)
    visited.append(val)

visited = []

for val in x3:
    for key in data3:
        if val not in visited and data3[key] == val:
            y3.append(key)
    visited.append(val)

visited = []

for val in x4:
    for key in data4:
        if val not in visited and data4[key] == val:
            y4.append(key)
    visited.append(val)

z = []
z2 = []
z3 = []
z4 = []
    
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

for temp in y2:
    #temp = name.split(',')
    for k in connections:
        if temp[0] == k[0]:
            if k[2] == temp[1]:
                z2.append(str(temp) + " (" + str(k[1]) + ")")
                break
        if k[2] == temp[0]:
            if k[0] == temp[1]:
                z2.append(str(temp) + " (" + str(k[1]) + ")")
                break

for temp in y3:
    #temp = name.split(',')
    for k in connections:
        if temp[0] == k[0]:
            if k[2] == temp[1]:
                z3.append(str(temp) + " (" + str(k[1]) + ")")
                break
        if k[2] == temp[0]:
            if k[0] == temp[1]:
                z3.append(str(temp) + " (" + str(k[1]) + ")")
                break

for temp in y4:
    #temp = name.split(',')
    for k in connections:
        if temp[0] == k[0]:
            if k[2] == temp[1]:
                z4.append(str(temp) + " (" + str(k[1]) + ")")
                break
        if k[2] == temp[0]:
            if k[0] == temp[1]:
                z4.append(str(temp) + " (" + str(k[1]) + ")")
                break

#print len(y)
#print len(z)
        
#for route in y:
#    if route in dataH:
#        x2.append(dataH[route])
#    else:
#        x2.append(0)

#temp_x = x[:6] + x[-6:]
#temp_z = z[:6] + z[-6:]
temp_x = x[-6:] + x2[-6:] + x3[-6:] + x4[-6:]
temp_z = z[-6:] + z2[-6:] + z3[-6:] + z4[-6:]
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
bars = ax.bar(range(len(temp_x)), temp_x, .5, align='center')
ax.set_xticks(range(len(temp_x)))
ax.set_xticklabels(temp_z, size=20)
ax.set_yticklabels([0, 100, 200, 300, 400, 500, 600, 700], size=30)

for label in ax.get_xticklabels(): 
      label.set_horizontalalignment('center') 

figure.autofmt_xdate(rotation=45)

for x in range(6, 12):
  bars[x].set_color('r')
for x in range(12, 18):
  bars[x].set_color('y')
for x in range(18, 24):
  bars[x].set_color('g')

pylab.show()
plt.show()
