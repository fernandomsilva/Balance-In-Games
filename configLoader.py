import pickle
import os

def getGameConfiguration(filename):
	configObject = {}
	with open(filename) as f:
		for line in f:
			line = line.strip('\n')
			configLine = line.split('=')
			setting = configLine[1]
			try:
				setting = int(setting)
			except ValueError as e:
				pass
			if setting == 'True':
				setting = True
			elif setting == 'False':
				setting = False
			try:
				if setting[0] == '{' or setting[0] == '(':
					setting = eval(setting)	
			except:
				pass
			configObject[configLine[0]] = setting
	return configObject