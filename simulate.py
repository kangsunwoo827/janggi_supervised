from game import Game, GameState
import MCTS as mc
cpuct=1

def buildMCTS(state):
    root = mc.Node(state)
    mcts = mc.MCTS(root, cpuct)
    return mc.MCTS(root, cpuct)

def changeRootMCTS(state):
	mcts.root = mcts.tree[state.id]

from game import Game, GameState

if __name__=='__main__':
	mcts=None
	
	state=Game().gameState
	if mcts == None or state.id not in mcts.tree:
		mcts=buildMCTS(state)
	else:
		changeRootMCTS(state)
	
	for i in range(2000):
        print(i)
		leaf, value, done, breadcrumbs = mcts.moveToLeaf()
        mcts.appendLeaf(leaf)
        mcts.backFill(leaf, value, breadcrumbs)
	