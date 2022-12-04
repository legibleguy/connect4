import random
import math
import copy

class Node():
# Data structure to keep track of our search
	def __init__(self, state, parent = None):
		self.visits = 1 
		self.reward = 0.0
		self.state = state
		self.children = []
		self.children_move = []
		self.parent = parent 

	def addChild( self , child_state , move ):
		child = Node(child_state,self)
		self.children.append(child)
		self.children_move.append(move)

	def update( self,reward ):
		self.reward += reward 
		self.visits += 1

	def fully_explored(self):
		if len(self.children) == len(self.state.legal_moves()):
			return True
		return False

def treePolicy( node, turn , factor ):
	while node.state.terminal() == False and node.state.winner() == 0:
		if ( node.fully_explored() == False ):
			return expand(node, turn), -turn
		else:
			node = bestChild ( node , factor )
			turn *= -1
	return node, turn

def expand( node, turn ):
	tried_children_move = [m for m in node.children_move]
	possible_moves = node.state.legal_moves()

	for move in possible_moves:
		if move not in tried_children_move:
			row = node.state.tryMove(move)
			new_state = copy.deepcopy(node.state)
			new_state.board[row][move] = turn 
			new_state.last_move = [ row , move ]
			break

	node.addChild(new_state,move)
	return node.children[-1]

# Function for selecting the child with the highest number of visits
def bestChild(node,factor):
	bestscore = -10000000.0
	bestChildren = []
	for c in node.children:
		exploit = c.reward / c.visits
		explore = math.sqrt(math.log(2.0*node.visits)/float(c.visits))
		score = exploit + factor*explore
		if score == bestscore:
			bestChildren.append(c)
		if score > bestscore:
			bestChildren = [c]
			bestscore = score 
	return random.choice(bestChildren)

def tryMove(board, move):
	# Takes the current board and a possible move specified 
	# by the column. Returns the appropiate row where the 
	# piece and be located. If it's not found it returns -1.

	# Error if move is out of bounds or if the column is full
	if ( move < 0 or move > 7 or board[0][move] != 0 ):
		return -1

	# Go through each row and check if that spot is full
	for i in range(len(board)):
		if ( board[i][move] != 0 ):
			return i-1
	return len(board)-1

def pick_random_move(board, currentPlayer):
	# Picks a random move for the current player
	board_copy = copy.deepcopy(board)
	moves = board_copy.legal_moves()
	
	if len(moves) > 0 :
		ind = random.randint(0,len(moves)-1) # Pick a random index
		chosen_move = moves[ind] # Use random index to pick a legal move

		row = tryMove(board_copy, chosen_move)
		board_copy[row][chosen_move] = currentPlayer
		board_copy.last_move = [ row, chosen_move ]
	return board_copy 

# Function for simulating a rollout
def rollout( state, turn  ):
	while state.terminal()==False and state.winner() == 0 :
		state = state.next_state( turn ) # Takes in the current player to move and makes a random move
		turn *= -1
	return  state.winner() 

def backup( node , reward, turn ):
	while node != None:
		node.visits += 1 
		node.reward -= turn*reward
		node = node.parent
		turn *= -1
	return

def MCTS( maxIter , root , factor ):
	for inter in range(maxIter):
		front, turn = treePolicy( root , 1 , factor )
		reward = rollout(front.state, turn)
		backup(front,reward,turn)

	ans = bestChild(root,0)
	return ans

def mctsMove(board ):
    # Returns the best move using MonteCarlo Tree Search
	o = Node(self.b)
	bestMove = MCTS( 3000, o, 2.0 )
	self.b = copy.deepcopy( bestMove.state )