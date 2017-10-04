# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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

        #print "successor -->",successorGameState, "\n"
        #print "newPos --> ",newPos, "\n"
        #print "newFood --> ",newFood, "\n"
        #print "newGhostStates --> ",newGhostStates, "\n"
        #print "newScaredTimes --> ",newGhostStates, "\n" 
        "*** YOUR CODE HERE ***"

        foodlist = newFood.asList();
        newghostposition = successorGameState.getGhostPositions()

        for food_position in foodlist:
          distancefromfood = util.manhattanDistance(food_position, newPos)

        for ghost_position in newghostposition:
          distancefromghost = util.manhattanDistance(ghost_position, newPos)


        ### return when pacman stops moving###
        if currentGameState.getPacmanPosition() == newPos:
          return -100000

        if successorGameState.isWin():
          return 100000

        if successorGameState.isLose():
          return -100000
        ### save pacman from ghost ###
        ### scaredtimes if-else condition

        #for ghost_distance in distancefromghost:
        #  if ghost_distance < 2:  ## pacman dies with 3 and avg score less than 500 with 1
        #    return -100000 

        ##############################

        ### pacman went into infinite loop from 1 position away from food###

        ### pacman returned error after eating last food ###

        if len(foodlist) == 0:
          return 10000000
        else:
          min_foodlist = min(foodlist)
          

        ghost_dis = 0
        score = successorGameState.getScore()*5

        score += len(successorGameState.getCapsules())*5
        #if distancefromghost:
        #  ghost_dis= 10/min(distancefromghost)

        
        score -= distancefromfood*2            

        #score += ghost_dis
        #higher_number = 10000/len(distancefromfood)

        ## scaredtimes of ghost
        ## if pellet eaten chase ghosts else chase food and avoid ghosts



        #higher_number = 100000/len(foodlist)

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


        def MaxValue(gameState,depth):

          if depth == self.depth:
            return (self.evaluationFunction(gameState),None)

          #if gameState.isWin() or gameState.isLose():
          #  return self.evaluationFunction(gameState)

          if len(gameState.getLegalActions(0)) == 0:
            return (self.evaluationFunction(gameState),None)

          #cal_v = -(float("inf"))
          optimal_v = -(float("inf"))
          optimal_action = None
          #agentIndex = gameState.getNumAgents()
          #ghosts = 2
          for action in gameState.getLegalActions(0):
            cal_v = optimal_v
            cal_v = max(cal_v,MinValue(gameState.generateSuccessor(0,action),1,depth)[0])
            #print "204\n"
            if optimal_v < cal_v:
              optimal_v = cal_v
              optimal_action = action
          #print "direction",(optimal_v,optimal_action),"\n" 
          return (optimal_v,optimal_action)
          

        def MinValue(gameState,var,depth):
          
          if depth == self.depth:
            return (self.evaluationFunction(gameState),None)


          ## program returning exception illegal action
          ## check for legal actions

          if len(gameState.getLegalActions(var)) == 0:
            return (self.evaluationFunction(gameState),None)


          #if gameState.isWin() or gameState.isLose():
          #  return self.evaluationFunction(gameState)

          #cal_v = (float("inf"))
          optimal_v = (float("inf"))
          optimal_action = None
          #agentIndex = gameState.getNumAgents()
          #print"agentIndex",var,"\n"
          #ghosts = 2
          #print "print_gamestatelegalaction",gameState.getLegalActions(),"helloo\n"
          for action in gameState.getLegalActions(var):
            #print "235\n"
            #print "agents",gameState.getNumAgents(),"\n"
            cal_v = optimal_v
            if (var == gameState.getNumAgents() - 1):
              #print "237\n"
              cal_v = min(cal_v,MaxValue(gameState.generateSuccessor(var,action),depth+1)[0])
            else:
              #print "242\n "
              #print "cal_v----action",action,"\n"
              cal_v = min(cal_v,MinValue(gameState.generateSuccessor(var,action),var + 1,depth)[0])
              #print "cal_v----action",action,"\n"

            if optimal_v > cal_v:
              optimal_v = cal_v
              optimal_action = action
          
          return (optimal_v,optimal_action)

        #v = - (float("inf"))

        #for action in gameState.getLegalActions():

        #  v = max(v,MinValue(gameState.generateSuccessor(0,action),0,self.depth))

        #  minimax_action = action

        return MaxValue(gameState,0)[1]

        ### minimax should return action
        ### pacman is getting caught

        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        def MaxValue(gameState, alpha, beta, depth):

          if depth == self.depth:
            return(self.evaluationFunction(gameState),None)
        	

          #if gameState.isWin() or gameState.isLose():
          #  return self.evaluationFunction(gameState)

          if len(gameState.getLegalActions(0)) == 0:
            return (self.evaluationFunction(gameState),None)

        	
          optimal_v = -(float("inf"))
          optimal_action = None
          #agentIndex = gameState.getNumAgents()

          for action in gameState.getLegalActions(0):
            cal_v = optimal_v
            cal_v = max(cal_v,MinValue(gameState.generateSuccessor(0,action),1,alpha,beta,depth)[0])
        		            
            if optimal_v < cal_v:
              optimal_v = cal_v
              optimal_action = action
            if cal_v > beta:
              return (optimal_v,optimal_action)

            alpha = max(alpha,cal_v)
            #alpha = max(alpha,v)
          #print "direction",(optimal_v,optimal_action),"\n" 
          return (optimal_v,optimal_action)
        		

        def MinValue(gameState, var, alpha, beta, depth):

          if depth == self.depth:
            return (self.evaluationFunction(gameState),None)


          ## program returning exception illegal action
          ## check for legal actions

          if len(gameState.getLegalActions(var)) == 0:
            return (self.evaluationFunction(gameState),None)

          optimal_v = (float("inf"))
          optimal_action = None
          #agentIndex = gameState.getNumAgents()
          for action in gameState.getLegalActions(var):
            cal_v = optimal_v
            if (var == gameState.getNumAgents() - 1):
              #print "237\n"
              cal_v = min(cal_v,MaxValue(gameState.generateSuccessor(var,action),alpha,beta,depth+1)[0])
            else:
              #print "242\n "
              #print "cal_v----action",action,"\n"
              cal_v = min(cal_v,MinValue(gameState.generateSuccessor(var,action),var + 1,alpha,beta,depth)[0])
              #print "cal_v----action",action,"\n"
            if optimal_v > cal_v:
              optimal_v = cal_v
              optimal_action = action
            if cal_v < alpha:
              return (optimal_v,optimal_action)

            beta = min(beta,cal_v)
        		#beta = max(beta,v)
          return (optimal_v,optimal_action)

        #v = - (float("inf"))
        #alpha = - (float("inf"))
        #beta = - (float("inf"))

        #for action in gameState.getLegalActions():

        #  v = max(v,MinValue(gameState,alpha,beta,self.depth))

        #  minimax_action = action

        return MaxValue(gameState,-(float("inf")),(float("inf")),0)[1]


        #util.raiseNotDefined()

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
        #def val(gameState)
        #  if
        def MaxValue(gameState,depth):

          if depth == self.depth:
            return (self.evaluationFunction(gameState),None)

          #if gameState.isWin() or gameState.isLose():
          #  return self.evaluationFunction(gameState)

          if len(gameState.getLegalActions(0)) == 0:
            return (self.evaluationFunction(gameState),None)

          #cal_v = -(float("inf"))
          optimal_v = -(float("inf"))
          optimal_action = None
          #agentIndex = gameState.getNumAgents()
          #ghosts = 2
          for action in gameState.getLegalActions(0):
            cal_v = optimal_v
            cal_v = max(cal_v,ExpectimaxValue(gameState.generateSuccessor(0,action),1,depth)[0])
            #print "204\n"
            if optimal_v < cal_v:
              optimal_v = cal_v
              optimal_action = action
          #print "direction",(optimal_v,optimal_action),"\n" 
          return (optimal_v,optimal_action)
          

        def ExpectimaxValue(gameState,var,depth):
          
          if depth == self.depth:
            return (self.evaluationFunction(gameState),None)


          ## program returning exception illegal action
          ## check for legal actions

          if len(gameState.getLegalActions(var)) == 0:
            return (self.evaluationFunction(gameState),None)


          #if gameState.isWin() or gameState.isLose():
          #  return self.evaluationFunction(gameState)

          #cal_v = (float("inf"))
          #optimal_v = (float("inf"))
          optimal_action = None
          cal_v = []
          #agentIndex = gameState.getNumAgents()
          #print"agentIndex",var,"\n"
          #ghosts = 2
          #print "print_gamestatelegalaction",gameState.getLegalActions(),"helloo\n"
          for action in gameState.getLegalActions(var):
            #print "235\n"
            #print "agents",gameState.getNumAgents(),"\n"
            #cal_v = optimal_v
            if (var == gameState.getNumAgents() - 1):
              #print "237\n"
              cal_v.append(MaxValue(gameState.generateSuccessor(var,action),depth+1)[0])
            else:
              #print "242\n "
              #print "cal_v----action",action,"\n"
              cal_v.append(ExpectimaxValue(gameState.generateSuccessor(var,action),var + 1,depth)[0])
              #print "cal_v----action",action,"\n"
          avg = (float(sum(cal_v)/len(cal_v)))
          
          return (avg,None)

        #v = - (float("inf"))

        #for action in gameState.getLegalActions():

        #  v = max(v,MinValue(gameState.generateSuccessor(0,action),0,self.depth))

        #  minimax_action = action

        return MaxValue(gameState,0)[1]



        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    #successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


    foodlist = newFood.asList();
    newghostposition = currentGameState.getGhostPositions()
    distancefromfood = 1000
    for food in foodlist:
      temp_dist = util.manhattanDistance(food, newPos)
      distancefromfood = min(distancefromfood,temp_dist)

    distancefromghost = 1000
    for ghost in newghostposition:
      temp_ghost_distance = manhattanDistance(ghost, newPos)
      distancefromghost = min(distancefromghost,temp_ghost_distance)

    if currentGameState.isWin():
      return 1000000

    if currentGameState.isLose():
      return -1000000
    ### return when pacman stops moving###
    #if currentGameState.getPacmanPosition() == newPos:
    #  return -100000

    ### save pacman from ghost ###
    ### scaredtimes if-else condition

    #for ghost_distance in distancefromghost:
    #  if ghost_distance < 2:  ## pacman dies with 3 and avg score less than 500 with 1
    #    return -100000 

    ##############################

    ### pacman went into infinite loop from 1 position away from food###

    ### pacman returned error after eating last food ###

    if len(foodlist) == 0:
      return 10000000
    else:
      min_foodlist = min(foodlist)
          

    ghost_dis = 0
    score = currentGameState.getScore()*5

    score -= len(currentGameState.getCapsules())*5
    #if distancefromghost:
    #  ghost_dis= 10/min(distancefromghost)

    score -= distancefromfood * 2  
    #score += 1000/distancefromfood            

    #score += ghost_dis
    #higher_number = 100000/len(foodlist) + score

    ## scaredtimes of ghost
    ## if pellet eaten chase ghosts else chase food and avoid ghosts


    #higher_number = 100000/len(foodlist)

    return score
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

