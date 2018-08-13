import os
import sys
import random

def idx(items, item):
	try:
		idx = items.index(item)
	except ValueError:
		idx = -1
	return idx 


class baseEnv:
	def __init__(self, isShow=False):
		self.isShow = isShow 
		self.motion = {}
		self.actions = []
		self.status = []


	def act(self, statu, action):
		if statu not in self.status:
			raise BaseException("No such statu")
		try:
			return self.motion[action](statu)
		except KeyError:
			raise BaseException("No such action")

	

class env1(baseEnv):	
	def __init__(self, isShow=False):
		baseEnv.__init__(self, isShow)
		self.statuReward = [-1, -1, -1, -1, -1,
							-1, -10,-1, -1, -1,
							-1, -1, -10,-1, -1,
							-1, -1, -1, -1, -1,
							-1, -1, -1, -10, 10]
		self.status = [(int(i/5), i%5) for i in range(25)]
		self.reward = dict(zip(self.status, self.statuReward))
		self.actions = ["up", "right", "down", "left"]
		self.motion = {"up":self.up, "right":self.right, "down":self.down, "left":self.left}

	def up(self, statu):
		newStatu = statu if statu[0]==0 else (statu[0]-1, statu[1])
		self.show(newStatu)
		return newStatu, self.reward[newStatu]
	
	def right(self, statu):
		newStatu = (statu if statu[1]==4 else (statu[0], statu[1]+1))
		self.show(newStatu)
		return newStatu, self.reward[newStatu]
	
	def down(self, statu):
		newStatu = (statu if statu[0]==4 else (statu[0]+1, statu[1]))
		self.show(newStatu)
		return newStatu, self.reward[newStatu]
	
	def left(self, statu):
		newStatu = (statu if statu[1]==0 else (statu[0], statu[1]-1))
		self.show(statu)
		return newStatu, self.reward[newStatu]

	def is_end(self, statu, val):
		if statu == (4,4):
			return True
		else:
			return False
	
	def get_avaliable_actions(self, statu):
		actions = self.actions[:]
		if statu[0] == 0:
			actions.remove("up")
		if statu[0] == 4:
			actions.remove("down")
		if statu[1] == 0:
			actions.remove("left")
		if statu[1] == 4:
			actions.remove("right")
		return actions
		

	def show(self, statu):
		if not self.isShow:
			return
		os.system("clear")
		for x in range(5):
			for y in range(5):
				if (x, y) == statu:
					print("#", end="")
				elif self.reward[(x,y)]==-1:
					print("O", end="")
				elif self.reward[(x,y)]==-10:
					print("*", end="")
				elif self.reward[(x,y)]==10:
					print("T", end="")
			print("")

	def start(self):
		self.show((0,0))
		return (0,0)
	
	


class env2(baseEnv):
	def __init__(self, isShow=False):
		baseEnv.__init__(self, isShow)
		self.status = [i for i in range(6)]
		self.reward = dict(zip(self.status, [1, -1, -1, -1, -1, -1, -1]))
		self.actions = ["left", "right"]
		self.motion = {"right":self.right, "left":self.left}

	def show(self, statu):
		if not self.isShow:
			return 
		pic = ("o-----" if statu==0 else "T" + "-"*(statu-1) + "o" + "-"*(5-statu))
		print("\r" + pic)


	def right(self, statu):
		newStatu = statu if statu==5 else statu+1
		self.show(newStatu)
		return newStatu, self.reward[newStatu]

	def left(self, statu):
		newStatu = statu if statu==0 else statu-1
		self.show(newStatu)
		return newStatu, self.reward[newStatu]
	
	def is_end(self, statu, val):
		return True if statu==0 else False
	
	def get_avaliable_actions(self, statu):
		if statu==0:
			return ["right"]
		elif statu==5:
			return ["left"]
		elif statu>0 and statu<5:
			return self.actions 
		else:
			raise BaseException("No such statu")

	def start(self):
		self.show(self.status[5])
		return self.status[5]


class env3(baseEnv):
	def __init__(self, isShow=False):
		baseEnv.__init__(self, isShow)
		self.status = []
		self.items = ["T", "*"]
		for myPlace in range(5):
			for line1Type in self.items:
				for line1Place in range(5):
					for line2Type in ["T", "*"]:
						for line2Place in range(5):
							for line3Type in ["T", "*"]:
								for line3Place in range(5):
									for line4Type in ["T", "*"]:
										for line4Place in range(5):
											for line5Type in ["T", "*"]:
												for line5Place in range(5):
													self.status.append((myPlace,
															(line1Type, line1Place),
															(line2Type, line2Place),
															(line3Type, line3Place),
															(line4Type, line4Place),
															(line5Type, line5Place)))
		self.actions = ["left", "right", "stop"]
		self.motion = {"left":self.left, "right":self.right, "stop":self.stop}
		self.reward = dict(zip(self.items, [10, -10]))


	def show(self, statu):
		if not self.isShow:
			return 
		os.system("clear")
		for y in range(5):
			for x in range(5):
				if statu[y+1][1] != x:
					print(" ", end="")
				else:
					print(statu[y+1][0], end="")
			print("")
		for x in range(5):
			if x == statu[0]:
				print("Y", end="")
			else:
				print("-", end="")
		print("")

	def start(self):
		statu = self.status[random.randint(0, len(self.status)-1)]
		self.show(statu)
		return statu

	def right(self, statu):
		if statu[0]+1 == statu[5][1]:
			reward = self.reward[statu[5][0]]
		else:
			reward = -1
		newStatu = (statu[0]+1,
			(self.items[random.randint(0, len(self.items)-1)], random.randint(0, 4)),
			(statu[1][0], statu[1][1]),
			(statu[2][0], statu[2][1]),
			(statu[3][0], statu[3][1]),
			(statu[4][0], statu[4][1]))
		self.show(newStatu)
		return newStatu, reward 

	def left(self, statu):
		if statu[0]-1 == statu[5][1]:
			reward = self.reward[statu[5][0]]
		else:
			reward = -1
		newStatu = (statu[0]-1,
			(self.items[random.randint(0, len(self.items)-1)], random.randint(0, 4)),
			(statu[1][0], statu[1][1]),
			(statu[2][0], statu[2][1]),
			(statu[3][0], statu[3][1]),
			(statu[4][0], statu[4][1]))
		self.show(newStatu)
		return newStatu, reward 
	
	def stop(self, statu):
		if statu[0] == statu[5][1]:
			reward = self.reward[statu[5][0]]
		else:
			reward = -1
		newStatu = (statu[0],
			(self.items[random.randint(0, len(self.items)-1)], random.randint(0, 4)),
			(statu[1][0], statu[1][1]),
			(statu[2][0], statu[2][1]),
			(statu[3][0], statu[3][1]),
			(statu[4][0], statu[4][1]))
		self.show(newStatu)
		return newStatu, reward 
	
	def get_avaliable_actions(self, statu):
		actions = self.actions[:]
		if statu[0] == 0:
			actions.remove("left")
		elif statu[0] == 4:
			actions.remove("right")
		return actions

	def is_end(self, statu, val):
		return True if val>=50 else False

















