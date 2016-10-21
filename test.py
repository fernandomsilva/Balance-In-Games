from loaddestinationdeck import *

d = loadcountrydestinationdeck('switzerland_city_country_destinations.txt', 'city')

print d[0].destinations
print d[0].points
print d[0].type
