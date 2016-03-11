import re

class DestinationCard:
	def __init__(self, dest1, dest2, points):
		self.destinations = [dest1, dest2]
		self.points = points

def loaddestinationdeckfromfile(filename):
	file = open(filename, 'r')

	deck = []

	#while len(line.strip()) > 0:
	#	print line.strip()
	#	line = file.readline()

	line = file.readline()
	while len(line.strip()) > 0:
		index = re.search('\d', line).start()
		index_space = line[index:].index(' ')

		deck.append(DestinationCard(line[:index-1], line[index+index_space+1:].strip(), line[index:index+index_space]))

		line = file.readline()

	for d in deck:
		print d.destinations[0] + " " + str(d.points) + " " + d.destinations[1]

	return deck
