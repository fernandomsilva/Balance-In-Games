import Queue

class Action:
	def __init__(self, city1, city2, size):
		self.destination = [city1, city2]
		self.size = size

class Node:
	def __init__(self, action, points):
		self.action = action
		self.points = points
	
	def __cmp__(self, other):
		return cmp(self.points, other.points)
		
q = Queue.PriorityQueue()
q.put(Node(Action('A', 'B', -4), 7))
q.put(Node(Action('A', 'C', -2), 2))
q.put(Node(Action('B', 'C', -3), 4))

while not q.empty():
	n = q.get()
	print n.destination