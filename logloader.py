import pickle

class LogMove:
	def __init__(self, pnum, move, args):
		self.pnum = pnum
		self.move = move
		self.args = []
		if 'TrainCard' in move:
			self.args.append(args)
		else:
			for arg in args:
				if type(arg) == list and type(arg[0]) != str:
					for subarg in arg:
						self.args.append(str(subarg))
				else:
					self.args.append(arg)

	def __getstate__(self): return self.__dict__
	def __setstate__(self, d): self.__dict__.update(d)

filename = 'testdata.ml'
f = open(filename, 'rb')
flist = []
try:
	while True:
		flist = pickle.load(f)
except:
	pass

for p in flist:
	print p.args