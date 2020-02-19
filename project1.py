import copy 

# Helper Functions vvv ===============================================================

# def printPuzz8( puzz )
# prints a 3x3 puzzle
def printPuzz8 ( puzz ):
	for i in range(3):
		print (puzz[(3*i)+0], puzz[(3*i)+1], puzz[(3*i)+2])

# def switch(puzz, a, b)
# switches two positions in an array, returns a new copy
def switch(puzz, a, b): 
	aVal = puzz[a]
	bVal = puzz[b]
	newPuzz = copy.deepcopy(puzz)
	newPuzz[a] = bVal
	newPuzz[b] = aVal
	return newPuzz

# def find(puzz, x = 0)
# returns index of a value in an array, returns -1 if not found
def find(puzz, x = 0):
	for i in range(len(puzz)):
		if puzz[i] == x:
			return i;
	return -1;
# Helper Functions ^^^ ===============================================================

# Node Class vvv ===============================================================
class puzz8:
	def __init__(self, g = 0, puzz = [0,0,0,0,0,0,0,0,0], h = 0):
		self.g = g #dist from initial
		self.puzz = puzz
		self.h = h

	def print(self):
		printPuzz8(self.puzz)
# Node Class ^^^  ===============================================================

# Heuristic Functions vvv ===============================================================

# def returnZero()
# returns 0 for Uniform Cost Search, or no heuristic
def returnZero():
	return 0

# def misplacedTiles( puzz )
# returns amount of misplaced tiles in a puzzle
def misplacedTiles( puzz ):
	cnt = 0
	for i in range(1,9): # checks each of 8 tiles, compares to loc it should be at
		if (puzz[i-1] != i): # if loc does not have right number add 1
			cnt+=1
	return cnt

# def manhattanDist( puzz )
# returns manhattan dist for a puzzle
def manhattanDist( puzz ):
	cnt = 0
	for i in range(1,9): # checks each of 8 tiles, compares to loc it should be at
		if (puzz[i-1] != i): # compare loc to tile
			ncnt = 0 
			loc = find(puzz, i) # find where tile is
			if ( loc%3 != (i-1)%3 ): #checks dist horizontal
				ncnt+= abs(loc%3 - (i-1)%3)
				# print ("horizontal", abs(loc%3 - (i-1)%3), loc%3, (i-1)%3)
			if ( (int)(loc/3) != (int)((i-1)/3) ): #checks dist horizontal
				ncnt+= abs(((int)(loc/3) - (int)((i-1)/3) ))
				# print ("vert", abs(((int)(loc/3) - (int)((i-1)/3) )), (int)(loc/3), (int)((i-1)/3))
			cnt+=ncnt
	return cnt

# Heuristic Functions ^^^ ===============================================================

# Search Functions vvv ===============================================================

# def expand(choice, frontier, alg, explored)
# expands the node as long as not in explored
# adds possible moves to frontier if not in explored
# calculates cost of node
def expand(choice, frontier, alg, explored):
	p = choice.puzz
	g = choice.g
	x = find(p, 0)

	if ( tuple(p) not in explored):
		print ("Expanding this node...")
		i = 0
		if (x+1)%3 != 0: # if not in right column
			temp = switch(p, x, x+1)
			if tuple(temp) not in explored:
				frontier.append( puzz8(g+1, temp, alg(temp)) ) # to the right of space
			i+=1
		if x > 2: # if not in top row
			temp = switch(p, x, x-3)
			if tuple(temp) not in explored:
				frontier.append( puzz8(g+1, temp, alg(temp)) ) # to the top of space
			i+=1
		if x < 6: # if not in bottom row
			temp = switch(p, x, x+3)
			if tuple(temp) not in explored:
				frontier.append( puzz8(g+1, temp, alg(temp)) ) # to the bottom of space
			i+=1
		if (x+1)%3 != 1: # if not in left column
			temp = switch(p, x, x-1)
			if tuple(temp) not in explored:
				frontier.append( puzz8(g+1, temp, alg(temp)) ) # to the left of space
			i+=1
		print ( i, "nodes added")
	else:
		print ("Node already explored, moving on.")
	print()

# def choose(frontier)
# chooses the lowest cost node from frontier
def choose( frontier ): 
	state = 0
	minCost = frontier[0].g + frontier[0].h
	i = 1
	for i in range(1,len(frontier)):
		w = frontier[i].g + frontier[i].h
		if w < minCost:
			minCost = w
			state = i
	return state

# def graphSearch (puzz, alg = returnZero, maxNodes = 100000)
# initial state, heuristic func, maxNodes
def graphSearch (puzz, alg = returnZero, maxNodes = 100000):
	puzz.h = alg(puzz.puzz) # add heuristic cost to initial state
	frontier = [ puzz ]; # initialize frontier to a list
	maxQ = len(frontier) # initialize max queue size
	explored = set(); # initialize explored set

	print ("initial state")
	puzz.print()
	print()
	
	# loop until maxNodes default 100,000 , so no infinite loop
	for i in range(maxNodes):
		choice = choose(frontier) # choose lowest cost node

		print ("The best state to expand with g(n) =", frontier[choice].g, "and h(n) =", frontier[choice].h, "is")
		frontier[choice].print()

		if (frontier[choice].puzz == goal): #compares selected puzz to goal state
			print ("goal found")
			print ("To solve this problem the search algorithm expanded a total of", len(explored), "nodes.")
			print ("The maximum number of nodes in the queue at any one time was", maxQ, ".")
			return frontier[choice] #returns

		explored.add(tuple(frontier[choice].puzz)) # add puzzle instance to explored since objs will be different
		expand(frontier[choice], frontier, alg, explored) # expand node
		if maxQ < len(frontier): # updates max queue size 
			maxQ = len(frontier)
		frontier.pop(choice) # remove choice from frontier

	print ("Did not find a solution in", maxNodes, "nodes.")
	return puzz8() # if no solution found return empty puzzle

# Search Functions ^^^ ===============================================================

# test states vvv ===============================================================
goal = 		[1,2,3,4,5,6,7,8,0]
veryeasy = 	[1,2,3,4,5,6,7,0,8]
easy = 		[1,2,0,4,5,3,7,8,6]
doable = 	[0,1,2,4,5,3,7,8,6]
ohboy = 	[8,7,1,6,0,2,5,4,3]
imp = 		[1,2,3,4,5,6,8,7,0]

cases = [ [1,2,3,4,5,6,7,8,0], [1,2,3,4,5,6,7,0,8], [1,2,0,4,5,3,7,8,6], [0,1,2,4,5,3,7,8,6], [8,7,1,6,0,2,5,4,3], [1,2,3,4,5,6,8,7,0] ]
# test states ^^^ ===============================================================

def main():
	print ("Welcome to 861287993 / jlee434's 8-puzzle solver.")


	graphSearch(init, manhattanDist)

main();


























