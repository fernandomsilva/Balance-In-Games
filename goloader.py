import pickle

filename = 'testdata.go'
f = open(filename, 'rb')
flist = []
try:
	while True:
		flist = pickle.load(f)
except:
	pass

print flist

print flist.players[1].points
print flist.players[0].hand
flist.players[0].print_destination_cards()
print flist.board.graph.nodes()
flist.printScoring(1)