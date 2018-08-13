import environment 
import random
import time
import sys
import os
import pickle
from tqdm import *
import profile

class QTable:
	def __init__(self, env):
		self.status = env.status
		self.actions = env.actions
		self.dic = dict(zip(self.status, [dict(zip(env.get_avaliable_actions(self.status[j]), [0 for i in range(len(env.get_avaliable_actions(self.status[j])))])) for j in range(len(self.status))]))
	
	def __getitem__(self, idx):
		return self.dic[idx[0]][idx[1]]
	
	def __setitem__(self, idx, val):
		self.dic[idx[0]][idx[1]] = val
	
	def show(self):
		for statu in self.status:
			actions = [action for action,val in self.dic[statu].items()]
			i = 0
			for action in self.actions:
				if action in actions:
					print("%.3f" % self.dic[statu][action], end='\t')
				else:
					print("*", end="\t")
			print("")
			
	def choose_action(self, statu):
		for action, val in self.dic[statu].items():
			if val != 0:
				is_random = False
				break;
			else:
				is_random = True
		if random.random() <= 0.1 or is_random:
			return random_choose([action for action,val in self.dic[statu].items()])
		else:
			i = 0
			for item in self.dic[statu].items():
				if i==0:
					maxi = item
					i = 1
				elif item[1] > maxi[1]:
					maxi = item
			return maxi[0]
	
	def get_max_val(self, statu):
		i = 0
		for key, val in self.dic[statu].items():
			if i==0:
				maxVal = val
				i = 1
			elif val > maxVal:
				maxVal = val
		return maxVal
				

R = 0.9
AMOUNT = 100000
ALPHA = 0.5
SLEEP = 2


def random_choose(list):
	return list[random.randint(0, len(list)-1)]


	
def save_qtable(qtable):
	with open("qtable("+ ("env2" if len(sys.argv)==1 else sys.argv[1]) + ")", "wb") as fp:
		pickle.dump(qtable, fp)
#	print("saved")
	
def training(env, qtable, isShow=False):
	try:
		if not isShow:
			steps = trange(AMOUNT, ncols=100, ascii=True)
		else:
			steps = range(AMOUNT)
		for step in steps:
			statu = env.start()
			val = 0
			i = 0
			while not env.is_end(statu, val):
				i += 1
				action = qtable.choose_action(statu)
				statu_, reward = env.act(statu, action, val)
				val += reward
				if env.is_end(statu, val):
					q_target = reward
				else:
					q_target = reward + R * qtable.get_max_val(statu_)
				q_predict = qtable[statu, action]
				qtable[statu, action] += ALPHA * (q_target - q_predict)
				statu = statu_ 
				if isShow:
					time.sleep(SLEEP)
			if isShow:
				print("total steps: %d" % i)
				time.sleep(SLEEP)
	except KeyboardInterrupt:
		return qtable 

	return qtable
	
if __name__ == "__main__":
	isShow = False 
	if len(sys.argv) >= 3 and sys.argv[2] == "-s":
		isShow = True
	files = os.listdir()
	if len(sys.argv) >= 2:
		try:
			env = getattr(environment, sys.argv[1])(isShow)
		except AttributeError:
			print("No such environment: %s" % sys.argv[1])
			sys.exit()
	else:
		env = environment.env2(isShow)
	
	
	qtable = QTable(env)
	fileName = ("qtable("+ ("env2" if len(sys.argv)==1 else sys.argv[1]) + ")")
	if fileName in files:
		print("load tabel")
		with open(fileName, "rb") as fp:
			qtable = pickle.load(fp)
		
	qtable = training(env, qtable, isShow)
#	profile.run("training(env, qtable, isShow)", sort="tottime")

	save_qtable(qtable)
	if isShow:
		qtable.show()

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
