import time
import copy 

# Helper Functions vvv ===============================================================

# def printPuzz8( list:puzz )
# prints a 3x3 puzzle
def printPuzz8 ( puzz ):
	for i in range(3):
		print (puzz[(3*i)+0], puzz[(3*i)+1], puzz[(3*i)+2])

# def switch(list:puzz, int:a, int:b)
# switches two positions in an array, returns a new copy
def switch(puzz, a, b): 
	aVal = puzz[a]
	bVal = puzz[b]
	newPuzz = copy.deepcopy(puzz)
	newPuzz[a] = bVal
	newPuzz[b] = aVal
	return newPuzz

# def find(list:puzz, int:x = 0)
# returns index of a value in an array, returns -1 if not found
def find(puzz, x = 0):
	for i in range(len(puzz)):
		if puzz[i] == x:
			return i
	return -1

# def isValidPuzz8( list:puzz )
# returns 1 if 0-8 are present, and len = 9, or 0
def isValidPuzz8(puzz):
	if len(puzz) == 9:
		for i in range(9):
			if find(puzz, i) == -1:
				return 0
		return 1
	return 0

# Helper Functions ^^^ ===============================================================

# Node Class vvv ===============================================================
class puzz8:
	def __init__(self, puzz = [0,0,0,0,0,0,0,0,0], g = 0, h = 0):
		self.g = g # dist from initial
		self.puzz = puzz # array 
		self.h = h # heuristic weight

	def print(self):
		printPuzz8(self.puzz)
# Node Class ^^^  ===============================================================

# Heuristic Functions vvv ===============================================================

# def returnZero( list:puzz )
# returns 0 for Uniform Cost Search, or no heuristic
def returnZero( puzz ):
	return 0

# def misplacedTiles( list:puzz )
# returns amount of misplaced tiles in a puzzle
def misplacedTiles( puzz ):
	cnt = 0
	for i in range(1,9): # checks each of 8 tiles, compares to loc it should be at
		if (puzz[i-1] != i): # if loc does not have right number add 1
			cnt+=1
	return cnt

# def manhattanDist( list:puzz )
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

# def expand(puzz8:choice, array:frontier, func:alg, set(tuples):explored)
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
				frontier.append( puzz8( temp, g+1, alg(temp)) ) # to the right of space
				i+=1
		if x > 2: # if not in top row
			temp = switch(p, x, x-3)
			if tuple(temp) not in explored:
				frontier.append( puzz8( temp, g+1, alg(temp)) ) # to the top of space
				i+=1
		if x < 6: # if not in bottom row
			temp = switch(p, x, x+3)
			if tuple(temp) not in explored:
				frontier.append( puzz8( temp, g+1, alg(temp)) ) # to the bottom of space
				i+=1
		if (x+1)%3 != 1: # if not in left column
			temp = switch(p, x, x-1)
			if tuple(temp) not in explored:
				frontier.append( puzz8( temp, g+1, alg(temp)) ) # to the left of space
				i+=1
		print ( i, "nodes added")
	else:
		print ("Node already explored, moving on.")
	print()

# def choose(list:frontier)
# chooses the lowest cost node from frontier list
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

# def graphSearch (puzz8:puzz, func:alg = returnZero, int:maxNodes = 100000)
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
		if len(frontier) < 1:
			break;
		choice = choose(frontier) # choose lowest cost node

		print ("The best state to expand with g(n) =", frontier[choice].g, "and h(n) =", frontier[choice].h, "is")
		frontier[choice].print()

		if (frontier[choice].puzz == goal): #compares selected puzz to goal state
			print()
			print ("goal found")
			print ("To solve this problem the search algorithm expanded a total of", len(explored), "nodes.")
			print ("The maximum number of nodes in the queue at any one time was", maxQ, ".")
			return frontier[choice], len(explored), maxQ #returns

		expand(frontier[choice], frontier, alg, explored) # expand node
		explored.add(tuple(frontier[choice].puzz)) # add puzzle instance to explored since objs will be different
		if maxQ < len(frontier): # updates max queue size 
			maxQ = len(frontier)
		frontier.pop(choice) # remove choice from frontier

	print ("Did not find a solution in", len(explored), "nodes.")
	return puzz8(), len(explored), maxQ # if no solution found return empty puzzle

# Search Functions ^^^ ===============================================================

# test states vvv ===============================================================
goal = 		[1,2,3,4,5,6,7,8,0]
veryeasy = 	[1,2,3,4,5,6,7,0,8]
easy = 		[1,2,0,4,5,3,7,8,6]
doable = 	[0,1,2,4,5,3,7,8,6]
ohboy = 	[8,7,1,6,0,2,5,4,3]
imp = 		[1,2,3,4,5,6,8,7,0]

testCases = [ [1,2,3,4,5,6,7,8,0], [1,2,3,4,5,6,7,0,8], [1,2,0,4,5,3,7,8,6], [0,1,2,4,5,3,7,8,6], [8,7,1,6,0,2,5,4,3], [1,2,3,4,5,6,8,7,0] ]
testCaseNames = [ "trivial", "very easy", "easy", "doable", "ohboy", "impossible"]
algs = [ returnZero, misplacedTiles, manhattanDist ]
algNames = [ "Uniform Cost Search", "A* with the Misplaced Tile heuristic", "A* with the Manhattan distance heuristic"]
# test states ^^^ ===============================================================

# test functions vvv ===============================================================

# def testHeuristic( puzz8:puzz )
# runs heuristic on puzz8, initial state
def testHeuristic( puzz ):
	userChoice = 0
	while userChoice != "1" and userChoice != "2":
		print ("Testing only Heuristic on puzzle")
		print ("Enter your choice of heuristic (press enter to submit).")
		print ("1. Misplaced Tile heuristic.")
		print ("2. Manhattan distance heuristic.")
		userChoice = input()
	userChoice = (int)(userChoice)
	print ("Heuristic returned " + str(algs[userChoice](puzz.puzz)) + " estimated distance from the goal.")

# test functions ^^^ ===============================================================

def main():
	userChoice = 0
	init = puzz8()

	while (1):
		flag = 1
		print ()
		print ("Welcome to 861287993 / jlee434's 8-puzzle solver (ctrl+c to exit).")
		while userChoice != "1" and userChoice != "2" and userChoice != "3":
			print ("Type '1' to use a default puzzle. (press enter to submit)")
			print ("Type '2' to enter your own puzzle.")
			print ("Type '3' to run all three algorithms on all 6 default puzzles, output results to trace.txt.")
			userChoice = input()
			print()

		if userChoice == "1":
			userChoice = 0
			while userChoice != "1" and userChoice != "2" and userChoice != "3" and userChoice != "4" and userChoice != "5" and userChoice != "6":
				print ("Type the number of the default puzzle you would like (press enter to submit).")
				print ("1. trivial")
				print ("2. very easy")
				print ("3. easy")
				print ("4. doable")
				print ("5. ohboy")
				print ("6. impossible")
				userChoice = input()
				print()
			userChoice = (int)(userChoice)
			init = puzz8( testCases[userChoice-1] )



		elif userChoice == "2":
			userChoice = 0
			while(flag):
				flag = 0
				print ("Enter your puzzle (number 0 - 8), use a zero to represent the blank.")
				print ("Enter your first row, use a space or tab between numbers (press enter to submit).")
				userChoice = input()
				a = userChoice.split()
				if len(a) != 3:
					flag = 1
				print ("Enter your second row, use a space or tab between numbers (press enter to submit).")
				userChoice = input()
				a = a + userChoice.split()
				if len(a) != 6:
					flag = 1
				print ("Enter your third row, use a space or tab between numbers (press enter to submit).")
				userChoice = input()
				a = a + userChoice.split()
				if len(a) != 9:
					flag = 1

				for i in range(len(a)):
					if (a[i].isdigit()):
						a[i] = (int)(a[i])
					else:
						flag = 1
						print (a[i])

				if isValidPuzz8(a) == 0:
					flag = 1

				print()
				if flag == 1:
					print ("Something about the puzzle you entered was wrong, Please try again.")
					print()
					continue

				print ("Puzzle inputted successfully.")
				printPuzz8(a)
				print()
				init = puzz8( a )

		elif userChoice == "3":
			print ("Running all three algorithms on all 6 default puzzles, outputting to 'trace.txt'.")
			storeVals = [];
			for i in range(6):
				storeVals.append([ {}, {} ,{} ])

			
			for i in range(6):
				for j in range(3):
					sol, expanded, maxQ = graphSearch(puzz8(testCases[i]), algs[j], 1000000)
					storeVals[i][j] = {'s': sol, 'e': expanded, 'm': maxQ, 'i': puzz8(testCases[i], 0, algs[j](testCases[i]) ) }

			out = open('trace.txt','w')
			for i in range(6 ):
				for j in range(3):
					out.write( 'Test Case - ' + testCaseNames[i] + ', with Alg - ' + algNames[j] + '\n')
					out.write( 'Initial State = [' + ','.join(map(str, testCases[i])) + '] g = ' + str(storeVals[i][j]['i'].g) + ' h = ' + str(storeVals[i][j]['i'].h) + '\n')
					out.write( 'Max Queue Size = ' + str(storeVals[i][j]['m']) + '\n')
					out.write( 'Nodes Expanded = ' + str(storeVals[i][j]['e']) + '\n')
					out.write( 'Solution State = [' + ','.join(map(str, storeVals[i][j]['s'].puzz)) + '] g = ' + str(storeVals[i][j]['s'].g) + ' h = ' + str(storeVals[i][j]['s'].h) + '\n' + '\n')


		if userChoice != "3":
			userChoice = 0
			while userChoice != "1" and userChoice != "2" and userChoice != "3" and userChoice != "4":
				print ("Enter your choice of search algorithm (press enter to submit).")
				print ("1. Uniform Cost Search.")
				print ("2. A* with the Misplaced Tile heuristic.")
				print ("3. A* with the Manhattan distance heuristic.")
				print ("4. Test only Heuristic separate from search.")
				userChoice = input()

			print()
			if userChoice == "4":
				testHeuristic(init)
			else: 
				userChoice = (int)(userChoice)
				sol, expanded, maxQ = graphSearch(init, algs[userChoice - 1])
				time.sleep(3);
main();


























