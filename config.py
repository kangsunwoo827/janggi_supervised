#### SELF PLAY
EPISODES = 3#25
MCTS_SIMS = 200 #논문 = 800
MEMORY_SIZE = 30000 # 30000
TURNS_UNTIL_TAU0 = 30 # turn on which it starts playing deterministically
CPUCT = 1 #A hyperparameter determining the level of exploration.
EPSILON = 0.2 # 원래 0.2
ALPHA = 0.15


#### RETRAINING
BATCH_SIZE = 256
EPOCHS = 1
REG_CONST = 0.0001
LEARNING_RATE = 0.1
MOMENTUM = 0.9
TRAINING_LOOPS = 10

HIDDEN_CNN_LAYERS = [
	{'filters':256, 'kernel_size': (3,3)}
	 , {'filters':256, 'kernel_size': (3,3)}
	 , {'filters':256, 'kernel_size': (3,3)}
	 , {'filters':256, 'kernel_size': (3,3)}
	 , {'filters':256, 'kernel_size': (3,3)}
	 , {'filters':256, 'kernel_size': (3,3)}
	 , {'filters':256, 'kernel_size': (3,3)}
	 , {'filters':256, 'kernel_size': (3,3)}
	 , {'filters':256, 'kernel_size': (3,3)}
	 , {'filters':256, 'kernel_size': (3,3)}
	 , {'filters':256, 'kernel_size': (3,3)}
	 , {'filters':256, 'kernel_size': (3,3)}
	 , {'filters':256, 'kernel_size': (3,3)}
	 , {'filters':256, 'kernel_size': (3,3)}
	 , {'filters':256, 'kernel_size': (3,3)}
	 , {'filters':256, 'kernel_size': (3,3)}
	 , {'filters':256, 'kernel_size': (3,3)}
	 , {'filters':256, 'kernel_size': (3,3)}
	 , {'filters':256, 'kernel_size': (3,3)}
	 , {'filters':256, 'kernel_size': (3,3)}
	]

#### EVALUATION
EVAL_EPISODES = 10
SCORING_THRESHOLD = 1.3