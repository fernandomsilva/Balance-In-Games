from script import *

record = [0, 0]

for i in range(0, 100):
	x = run(0, "usa")
	max_points = None
	winning_player = None
	for i in range(0, len(x.players)):
		if max_points == None or x.players[i].points > max_points:
			max_points = x.players[i].points
			winning_player = i

	record[winning_player] += 1

print record
#t.printScoring(0)
#t.printScoring(1)
