import pickle
import os

def aggregateData(folder):
	gameobjects = []
	for (dirname, dirs, files) in os.walk(folder):
		for filename in files:
			print 'filename'
			if filename.endswith('.go'):
				filename = 'testdata.go'
				f = open(filename, 'rb')
				flist = []
				try:
					while True:
						flist = pickle.load(f)
				except:
					pass

				print flist

				gameobjects.append(flist)

	pscores = []
	for x in range(0, gameobjects[0].number_of_players):
		pscores.append([])
	
	for go in gameobjects:
		for p in range(0, go.number_of_players):
			pscores[p].append(go.players[p].points)

	print 'averages:'
	pnum = 1
	for scores in pscores:
		print 'player' + str(pnum) + ': ' + str(sum(scores) / len(scores))
		pnum = pnum + 1
	
	print ''

	wins = [0] * len(pscores)
	print 'winratios:'
	for go in gameobjects:
		best = -500
		bplayer = -1
		for p in range(0, go.number_of_players):
			if go.players[p].points > best:
				bplayer = p
				best = go.players[p].points
		wins[bplayer] = wins[bplayer] + 1

	pnum = 1
	for wincount in wins:
		print 'player' + str(pnum) + ': ' + str(wincount) + '/' + str(len(gameobjects))
		pnum = pnum + 1