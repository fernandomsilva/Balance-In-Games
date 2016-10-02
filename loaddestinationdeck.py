import re

class DestinationCard:
	def __init__(self, dest1, dest2, points):
		self.destinations = [dest1, dest2]
		self.points = points
	
	def __getstate__(self): return self.__dict__
	def __setstate__(self, d): self.__dict__.update(d)

	def __str__(self):
		return str(self.destinations) + " " + str(self.points)

def loaddestinationdeckfromfile(filename):
	file = open(filename, 'r')

	deck = []

	line = file.readline()
	while len(line.strip()) > 0:
		index = re.search('\d', line).start()
		index_space = line[index:].index(' ')

		deck.append(DestinationCard(line[:index-1], line[index+index_space+1:].strip(), int(line[index:index+index_space])))

		line = file.readline()

	return deck

def destinationdeckdict(dest_list):
	result = {}
	for dest in dest_list:
		result[dest] = 1
	
	return result