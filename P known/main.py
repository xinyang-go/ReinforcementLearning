R = [[-1, -1, -1, -1, -1],
	 [-1, -10,-1, -1, -1],
	 [-1, -1, -10,-1, -1],
	 [-1, -1, -1, -1, -1],
	 [-1, -1, -1, -10, 0]]

V = [[0 for i in range(5)] for j in range(5)] 
nV = [[0 for i in range(5)] for j in range(5)] 
pi = [[[0.25 for x in range(4)] for i in range(5)] for j in range(5)]

def argAmax_Q(s):
	Qas = V[s[0]-1][s[1]] if s[0]-1>=0 else V[s[0]][s[1]]
	max = Qas
	maxA= 0
	Qas = V[s[0]][s[1]+1] if s[1]+1<=4 else V[s[0]][s[1]]
	if Qas >= max:
		max = Qas
		maxA = 1
	Qas = V[s[0]+1][s[1]] if s[0]+1<=4 else V[s[0]][s[1]]
	if Qas >= max:
		max = Qas
		maxA = 2
	Qas = V[s[0]][s[1]-1] if s[1]-1>=0 else V[s[0]][s[1]]
	if Qas >= max:
		max = Qas
		maxA = 3
		
	return maxA


for j in range(100):
	for i in range(10):
		for x in range(5):
			for y in range(5):
				nV[x][y] = pi[x][y][0] * (R[x][y] + (V[x-1][y] if x-1>=0 else V[x][y])) +\
						   pi[x][y][1] * (R[x][y] + (V[x][y+1] if y+1<=4 else V[x][y])) +\
						   pi[x][y][2] * (R[x][y] + (V[x+1][y] if x+1<=4 else V[x][y])) +\
						   pi[x][y][3] * (R[x][y] + (V[x][y-1] if y-1>=0 else V[x][y]))
		V = [column[::] for column in nV]
	for x in range(5):
		for y in range(5):
			pi[x][y] = [0 for i in range(4)]
			pi[x][y][argAmax_Q((x, y))] = 1
	

for row in V:
	print(row)
print("")

for element in pi:
	print(element)
	