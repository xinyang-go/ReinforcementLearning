import environment as env
import random
import tqdm

def getRandElement(list):
	return list[random.randint(0, len(list)-1)]


idom = [0 for i in range(len(env.status))]
V = dict(zip(env.status, idom))
r = 0.99
	
for t in tqdm.trange(100000, ncols=100, ascii=True):
	N = dict(zip(env.status, idom))
	statu = getRandElement(env.status)
	val = 0
	episodes = [(statu, val)]
	while not env.is_end(statu, val):
		action = getRandElement(env.actions)
		statu, reward = env.act(statu, action)
		episodes.append((statu, reward))
		val += reward
	for step in episodes:
		N[step[0]] += 1
		G = 0
		for [subStep,i] in zip(episodes[episodes.index(step):], range(len(episodes)-episodes.index(step))):
			G += r**i * subStep[1]
		V[step[0]] += (G-V[step[0]])/N[step[0]]

for [statu, i] in zip(env.status, range(len(env.status))):
	if (i+1)%5 == 0:
		print("%.2f" % V[statu])
	else:
		print("%.2f" % V[statu], end="\t")
	
	
		
		

