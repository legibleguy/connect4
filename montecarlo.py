import random
import math
import copy


class Board():
	def __init__(self, board, last_move = [-1,-1]) -> None:
		self.board = board[::-1]
		self.last_move = last_move
	
	def tryMove(self, move):
		# Takes the current board and a possible move specified 
		# by the column. Returns the appropiate row where the 
		# piece and be located. If it's not found it returns -1.

		if ( move < 0 or move > 7 or self.board[0][move] != 0 ):
			return -1

		for i in range(len(self.board)):
			if ( self.board[i][move] != 0 ):
				return i-1
		return len(self.board)-1
	
	def terminal(self):
       # Returns true when the game is finished, otherwise false.
		for i in range(len(self.board[0])):
			if ( self.board[0][i] == 0 ):
				return False
		return True
	
	def legal_moves(self):
		# Returns the full list of legal moves that for next player.
		legal = []
		for col in range(len(self.board[0])):
			if( self.board[0][col] == 0 ):
				legal.append(col)
			
		return legal

	def next_state(self, turn):
		# Retuns next state
		aux = copy.deepcopy(self)
		moves = aux.legal_moves()
		if len(moves) > 0 :
			ind = random.randint(0,len(moves)-1)
			row = aux.tryMove(moves[ind])
			aux.board[row][moves[ind]] = turn
			aux.last_move = [ row, moves[ind] ]
		return aux 
	
	def winner(self):
        # Takes the board as input and determines if there is a winner.
        # If the game has a winner, it returns the player number (Computer = 1, Human = -1).
        # If the game is still ongoing, it returns zero.  

		dx = [ 1, 1,  1,  0 ]
		dy = [ 1, 0,  -1,  1  ]

		x = self.last_move[0]
		y = self.last_move[1]

		if x == None:
			return 0 

		for d in range(4):

			h_counter = 0
			c_counter = 0

			for k in range(-3,4):

				u = x + k * dx[d]
				v = y + k * dy[d]

				if u < 0 or u >= 6:
					continue

				if v < 0 or v >= 7:
					continue

				if self.board[u][v] == -1:
					c_counter = 0
					h_counter += 1
				elif self.board[u][v] == 1:
					h_counter = 0
					c_counter += 1
				else:
					h_counter = 0
					c_counter = 0

				if h_counter == 4:
					return -1 

				if c_counter == 4:	
					return 1

		return 0

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
		print("added a child")
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

# # Returns true when if the board is full, otherwise false.
# # Originally called terminal
# def is_board_full(board):
# 	for i in range(len(board[0])):
# 		if ( board[0][i] == 0 ):
# 			return False
# 	return True

# Returns the best node that we can reach from the current node
def treePolicy( node, turn ):
	while node.state.terminal() == False and node.state.winner() == 0:
		print(node.fully_explored())
		if ( node.fully_explored() == False ):
			return expand(node, turn), -turn
		else:
			node = bestChild( node, 2.0 )
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
	
	node.addChild(new_state, move)
	return node.children[-1]

# Function for selecting the child with the highest number of visits
def bestChild(node, factor):
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

# Returns the full list of legal moves that for next player.
# Originally called legal_moves
def get_legal_moves(board):
	legal_moves = []

	for i in range(len(board[0])):
		if( board[0][i] == 0 ):
			legal_moves.append(i)

	return legal_moves

# Takes the current board and a possible move specified 
# by the column. Returns the appropiate row where the 
# piece and be located. If it's not found it returns -1.
def tryMove(board, move):
	# Error if move is out of bounds or if the column is full
	if ( move < 0 or move > 7 or board[0][move] != 0 ):
		return -1

	# Go through each row and check if that spot is full
	for i in range(len(board)):
		if ( board[i][move] != 0 ):
			return i-1
	return len(board)-1

# Picks a random move for the current player
# Originally called next_state
def pick_random_move(board, currentPlayer):
	board_copy = copy.deepcopy(board)
	moves = get_legal_moves(board_copy)
	
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

# Function for backpropagation
def backpropagation( node , reward, turn ):
	while node != None:
		node.visits += 1 
		node.reward -= turn*reward
		node = node.parent
		turn *= -1
	return

# Function for MCTS
def MCTS( maxIter , root ):
	for inter in range(maxIter):
		leaf, turn = treePolicy( root , 1 ) # selection/traversal step
		reward = rollout(leaf.state, turn) # simulation step
		backpropagation(leaf,reward,turn) # backpropagation step

	ans = bestChild(root,0)
	return ans

# Returns the best move using MonteCarlo Tree Search
def mctsMove(board):
	o = Node(Board(board))
	bestMove = MCTS( 3000, o )
	return bestMove.state.last_move[1]