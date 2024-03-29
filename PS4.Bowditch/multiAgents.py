# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        #print newGhostStates
        "*** YOUR CODE HERE ***"
        foods = newFood.asList()
        #print foods
        #print newScaredTimes
        #print newFood#,newGhostStates,newScaredTimes
        #print successorGameState.getScore()
        #print
        
        score = 0

        for seconds_scared in newScaredTimes:
            score+=seconds_scared
            
        ghostDistances = []
        for ghost in newGhostStates:
            ghostDistances.append(manhattanDistance(newPos, ghost.getPosition()))
        score+= min(ghostDistances)
        
        foodDistances = []
        for food in foods:
            foodDistances.append(manhattanDistance(newPos,food))
            
        if (currentGameState.getNumFood() > successorGameState.getNumFood()): score += 125

        if action == Directions.STOP: score -= 5
        if(len(foodDistances)>0): score -= 5 * min(foodDistances)

        score+=successorGameState.getScore()
        
        return score
    
        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

##    def utility(self,state):
##        return self.evaluationFunction(state)
##
##    def terminal_test(self,state,depth):
##        if depth == self.depth or state.isLose() or state.isWin():
##            return True
##        return False

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        def max_value(state,depth):
            depth+=1
            if depth == self.depth or state.isLose() or state.isWin():
                return self.evaluationFunction(state)
            
            pacman_legal_actions = state.getLegalActions(0)
            value = -99999999
            for pacman_action in pacman_legal_actions:
                value = max(value,min_value(state.generateSuccessor(0, pacman_action), depth, 1))
            return value

        def min_value(state,depth,ghostCount):
            if state.isLose() or state.isWin() or depth==self.depth:
                return self.evaluationFunction(state)
            ghost_legal_actions = state.getLegalActions(ghostCount)
            value = 9999999
            for ghost_action in ghost_legal_actions:
                if ghostCount == gameState.getNumAgents()-1:
                    value = min(value,max_value(state.generateSuccessor(ghostCount,ghost_action),depth))
                else:
                    value = min(value,min_value(state.generateSuccessor(ghostCount,ghost_action),depth,ghostCount+1))
            return value
        
        final_action = ""
        pacman_legal_actions = gameState.getLegalActions(0)
        max_score = -99999
        for pacman_action in pacman_legal_actions:
            next_state = gameState.generateSuccessor(0, pacman_action)
            current_score = min_value(next_state, 0,1)
            if current_score > max_score:
                max_score = current_score
                final_action = pacman_action
        return final_action
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        
        def max_value(state,depth,alpha,beta):
            depth+=1
            if depth == self.depth or state.isLose() or state.isWin():
                return self.evaluationFunction(state)
            
            pacman_legal_actions = state.getLegalActions(0)
            value = -99999999
            for pacman_action in pacman_legal_actions:
                value = max(value,min_value(state.generateSuccessor(0, pacman_action), depth,1,alpha,beta))

                if value>beta: return value

                alpha = max(alpha,value)

            return value

        def min_value(state,depth,ghostCount,alpha,beta):
       
            if state.isLose() or state.isWin() or depth==self.depth:
                return self.evaluationFunction(state)
            
            ghost_legal_actions = state.getLegalActions(ghostCount)
            value = 9999999
            for ghost_action in ghost_legal_actions:
                next_state = state.generateSuccessor(ghostCount,ghost_action)
                if ghostCount == gameState.getNumAgents()-1:
                    value = min(value,max_value(next_state,depth,alpha,beta))
                else:
                    value = min(value,min_value(next_state,depth,ghostCount+1,alpha,beta))
                    
                if value <alpha:return value
                beta = min(beta,value)
                
            return value


        final_action = ""
        pacman_legal_actions = gameState.getLegalActions(0)
        max_score = -9999999
        alpha = -99999999
        beta = 999999999
        for pacman_action in pacman_legal_actions:
            next_state = gameState.generateSuccessor(0, pacman_action)
            current_score = min_value(next_state, 0,1,alpha,beta)
            if current_score > max_score:
                max_score = current_score
                final_action = pacman_action
            if current_score >= beta:
                return final_action
            alpha = max(alpha, current_score)
        return final_action
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

