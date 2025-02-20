# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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

    "*** YOUR CODE HERE ***"
    return successorGameState.getScore()

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

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"


    #get action for the pacman first
    #for each ghost, get action and move on to the next

    def pac_agent(current_depth, agent_number, gameState):
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        if current_depth == self.depth:
            return self.evaluationFunction(gameState)
        max_value = -float("inf")
        pac_agent_action_list = gameState.getLegalActions(agent_number)
        
        if len(pac_agent_action_list) == 0:
            return self.evaluationFunction(gameState)
        
        #print("here")
        #print(pac_agent_action_list)
        for action in pac_agent_action_list:
            #print("enter the loop")
            next_state = gameState.generateSuccessor(agent_number, action)
            next_state_result = ghost_agent(current_depth, agent_number+1, next_state)
            #print("******************")
            #print(next_state_result)
            #print("*****************************")
            
            
            if type(next_state_result) == list:
                temp_result = next_state_result[0]
            else:
                temp_result = next_state_result
               
            
            if temp_result > max_value:
                
                max_value = temp_result
                
                max_value_action = action
                max_value_action_pair = [max_value,max_value_action]
            
        return max_value_action_pair
             
    def ghost_agent(current_depth, agent_number, gameState):
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        min_value = float("inf")
        ghost_action_list = gameState.getLegalActions(agent_number)

        if len(ghost_action_list) == 0:
            return self.evaluationFunction(gameState)

        for action in ghost_action_list:
            next_state = gameState.generateSuccessor(agent_number, action)
            if agent_number+1 == gameState.getNumAgents():
                next_state_result = pac_agent(current_depth+1, 0, next_state)
            else:
                next_state_result = ghost_agent(current_depth, agent_number+1, next_state)
            

            if type(next_state_result) == list:
                temp_result = next_state_result[0]
            else:
                temp_result = next_state_result
            if temp_result < min_value:
                min_value = temp_result
                min_value_action = action
                min_value_action_pair = [min_value,min_value_action]
        return min_value_action_pair

    function_start_from_root = pac_agent(0, 0, gameState)

    action = function_start_from_root[1]
    #print(function_start_from_root)
    return action
    

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    def pac_agent(current_depth, agent_number, gameState, alpha, beta):
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        if current_depth == self.depth:
            return self.evaluationFunction(gameState)
        max_value = -float("inf")
        pac_agent_action_list = gameState.getLegalActions(agent_number)
        
        if len(pac_agent_action_list) == 0:
            return self.evaluationFunction(gameState)
    
        #print("here")
        #print(pac_agent_action_list)
        for action in pac_agent_action_list:
            #print("enter the loop")
            next_state = gameState.generateSuccessor(agent_number, action)
            next_state_result = ghost_agent(current_depth, agent_number+1, next_state, alpha, beta)
            #print("******************")
            #print(next_state_result)
            #print("*****************************")
            
            
            if type(next_state_result) == list:
                temp_result = next_state_result[0]
            else:
                temp_result = next_state_result
            
            if temp_result > beta:
                return [temp_result,action]
            if temp_result > max_value:
                
                max_value = temp_result
            
                max_value_action = action
                max_value_action_pair = [max_value,max_value_action]
            

            alpha = max(alpha, temp_result)
        return max_value_action_pair
             
    def ghost_agent(current_depth, agent_number, gameState, alpha, beta):
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        min_value = float("inf")
        ghost_action_list = gameState.getLegalActions(agent_number)

        if len(ghost_action_list) == 0:
            return self.evaluationFunction(gameState)

        for action in ghost_action_list:
            next_state = gameState.generateSuccessor(agent_number, action)
            if agent_number+1 == gameState.getNumAgents():
                next_state_result = pac_agent(current_depth+1, 0, next_state, alpha, beta)
            else:
                next_state_result = ghost_agent(current_depth, agent_number+1, next_state, alpha, beta)
            

            if type(next_state_result) == list:
                temp_result = next_state_result[0]
            else:
                temp_result = next_state_result

            if temp_result < alpha:
                return [temp_result,action]
            if temp_result < min_value:
                min_value = temp_result
                min_value_action = action
                min_value_action_pair = [min_value,min_value_action]
            
            beta = min(beta, temp_result)
        return min_value_action_pair



    function_start_from_root = pac_agent(0, 0, gameState, -float("inf"), float("inf"))

    action = function_start_from_root[1]
    #print(function_start_from_root)
    return action

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
    def pac_agent(current_depth, agent_number, gameState):
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        if current_depth == self.depth:
            return self.evaluationFunction(gameState)
        max_value = -float("inf")
        pac_agent_action_list = gameState.getLegalActions(agent_number)
        
        if len(pac_agent_action_list) == 0:
            return self.evaluationFunction(gameState)
    
        #print("here")
        #print(pac_agent_action_list)
        for action in pac_agent_action_list:
            #print("enter the loop")
            next_state = gameState.generateSuccessor(agent_number, action)
            next_state_result = ghost_agent(current_depth, agent_number+1, next_state)
            #print("******************")
            #print(next_state_result)
            #print("*****************************")
            
            
            if type(next_state_result) == list:
                temp_result = next_state_result[0]
            else:
                temp_result = next_state_result
            
            
            if temp_result > max_value:
                
                max_value = temp_result
            
                max_value_action = action
                max_value_action_pair = [max_value,max_value_action]
            
        return max_value_action_pair
             
    def ghost_agent(current_depth, agent_number, gameState):
        init_max_prob = 0
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        
        ghost_action_list = gameState.getLegalActions(agent_number)

        if len(ghost_action_list) == 0:
            return self.evaluationFunction(gameState)

        each_action_prob = 1.0/len(ghost_action_list)
        for action in ghost_action_list:
            next_state = gameState.generateSuccessor(agent_number, action)
            if agent_number+1 == gameState.getNumAgents():
                next_state_result = pac_agent(current_depth+1, 0, next_state)
            else:
                next_state_result = ghost_agent(current_depth, agent_number+1, next_state)
            

            if type(next_state_result) == list:
                temp_result = next_state_result[0]
            else:
                temp_result = next_state_result
            #temp_result = float(temp_result)
            init_max_prob += temp_result*each_action_prob
            action_prob_pair = [init_max_prob,action]
        return action_prob_pair
            
            
        



    function_start_from_root = pac_agent(0, 0, gameState)

    action = function_start_from_root[1]
    #print(function_start_from_root)
    return action

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

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

