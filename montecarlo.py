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

def defaultPolicy( state, turn  ):
	while state.terminal()==False and state.winner() == 0 :
		state = state.next_state( turn )
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
		reward = defaultPolicy(front.state, turn)
		backup(front,reward,turn)

	ans = bestChild(root,0)
	return ans

def findBestMove(self , factor ):
    # Returns the best move using MonteCarlo Tree Search
    	o = Node(self.b)
        bestMove = MCTS( 3000, o, factor )
        self.b = copy.deepcopy( bestMove.state )

        self.reloadBoard()