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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        print("successorGameState: ", successorGameState)
        print("newPos: ", newPos) 
        print("newFood: ", newFood) 
        print("newGhost: ", newGhostStates) 
        print("new Scared times: ", newScaredTimes) 


        #The point of this reflex agent is to make a pacman can look far distance and detect 
        #between a ghost and the pallets which are the food
        #we need to convert the food as list to get the actual coordinates
        listNewFood = newFood.asList()
        #getting the ghost every ghost position  
        ghostPositions = successorGameState.getGhostPositions() 
        minimum_foodList = float("inf")

        #iterating through the food list 
        #then find the minimum of manhattan distance to get the fastest search lookup for food
        for food in listNewFood:
            if (food[0] > 0) and (food[1] > 0): 
                manhattan_distance_food = manhattanDistance(newPos, food)
                if (minimum_foodList > manhattan_distance_food): 
                    minimum_foodList = manhattan_distance_food
            else: 
                print("there is no food!")
          

        #iterating through the ghost list 
        #then find the minimum of manhattan distance for the ghost
        #however, we need to detect between a pacman and a ghost when a ghost gets closer
        for ghost in ghostPositions:
            if (ghost[0] > 0.0) and(ghost[1] > 0.0): 
                manhattan_distance_ghost = manhattanDistance(newPos, ghost)
                if (2 > manhattan_distance_ghost): 
                    return -1 * (manhattan_distance_ghost) 
            else: 
                print("ghost is not moving!")
        #using reciprocal to calculate the getting the get score. 
        calculate_result = successorGameState.getScore() + 1 / float(minimum_foodList)

        return calculate_result

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
    def minimax(self, agent, depth, gameState):
        #We need to find the best score and action 
        finalBest_Score = None
        finalBest_Action = None
        next_agent = 0 

        #increasing the depth and agent set to zero when the number of agents is smaller then the current agent
        if gameState.getNumAgents() <= agent:
            agent = 0
            depth += 1
        #checking if the state of the game is either win, lost, or the same current depth 
        #then we return that actual evaluation function and stop that direction. 
        if (gameState.isWin() or gameState.isLose() or depth == self.depth):
            return [ Directions.STOP, self.evaluationFunction(gameState) ]
        
        #When the agent is 0, we need to have the game state of the legal actions of an agent 
        #when iterating through the legal actions, we increase the step of the agent 
        #then recursively do the minimax function 
        #after that, we need to find the cuurent max score than the best score. 
        if agent == 0:  
            agentLegal_actions = gameState.getLegalActions(agent)

            if not agentLegal_actions: 
                return [ Directions.STOP, self.evaluationFunction(gameState) ]

            for action in agentLegal_actions: 
                next_agent = agent + 1
                direction_score = self.minimax(next_agent, depth, gameState.generateSuccessor(agent, action))
                direction = direction_score[0]
                score = direction_score[1]

                if direction is "None": 
                    continue
                if finalBest_Score is None or score > finalBest_Score:
                    finalBest_Action = action
                    finalBest_Score = score

        #same performance from agent is 0 
        #but we need to find the max best score than the current score
        else: 
            agentLegal_actions = gameState.getLegalActions(agent)

            if not agentLegal_actions: 
                return [ Directions.STOP, self.evaluationFunction(gameState) ]

            for action in agentLegal_actions: 
                next_agent = agent + 1
                direction_score = self.minimax(next_agent, depth, gameState.generateSuccessor(agent, action))
                direction = direction_score[0]
                score = direction_score[1]
                
                if direction_score[0] is "None": 
                    continue
                if finalBest_Score is None or score < finalBest_Score:
                    finalBest_Action = action
                    finalBest_Score = score
               
        #we want to return the finalBest_Action for the getAction function 
        output = [finalBest_Action, finalBest_Score] 
        return output

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        #starting the agent and depth are zero and use the minimax algorithm to make a high decision game moves. 
        agent = 0 
        depth = 0 
        action = self.minimax(agent, depth, gameState)  
        return action[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    
    def expectiMax(self, agent, depth, gameState):
        #We need to find the best score and action 
        finalBest_Score = None
        finalBest_Action = None
        next_agent = 0 
        #initialize the probability for expectimax
        probability = 0.00
        max_probability = 1.00

        #increasing the depth and agent set to zero when the number of agents is smaller then the current agent
        if gameState.getNumAgents() <= agent:
            agent = 0
            depth += 1
        #checking if the state of the game is either win, lost, or the same current depth 
        #then we return that actual evaluation function and stop that direction. 
        if (gameState.isWin() or gameState.isLose() or depth == self.depth):
            return [ Directions.STOP, self.evaluationFunction(gameState) ]
        
        #When the agent is 0, we need to have the game state of the legal actions of an agent 
        #when iterating through the legal actions, we increase the step of the agent 
        #then recursively do the minimax function 
        #after that, we need to find the cuurent max score than the best score. 
        if agent == 0:  
            agentLegal_actions = gameState.getLegalActions(agent)

            if not agentLegal_actions: 
                return [ Directions.STOP, self.evaluationFunction(gameState) ]

            for action in agentLegal_actions: 
                next_agent = agent + 1
                direction_score = self.expectiMax(next_agent, depth, gameState.generateSuccessor(agent, action))
                direction = direction_score[0]
                score = direction_score[1]

                if direction is "None": 
                    continue
                if finalBest_Score is None or score > finalBest_Score:
                    finalBest_Action = action
                    finalBest_Score = score

        #same performance from agent is 0 
        #but we need to find the max best score than the current score
        else: 
            agentLegal_actions = gameState.getLegalActions(agent)
            sizeAgentLegal_actions = len(agentLegal_actions) 

            if not agentLegal_actions: 
                return [ Directions.STOP, self.evaluationFunction(gameState) ]

            #When the size of agent legal actions is more than zero
            #We need to divide between maximum probability and the size of agent legal actions 
            if sizeAgentLegal_actions > 0: 
                probability = max_probability / sizeAgentLegal_actions 

            for action in agentLegal_actions: 
                next_agent = agent + 1
                direction_score = self.expectiMax(next_agent, depth, gameState.generateSuccessor(agent, action))
                direction = direction_score[0]
                score = direction_score[1]

                if direction_score[0] is "None": 
                    continue

                #multiplying the probability and score and adding them together 
                #to get the probability best score for the expectimax 
                if finalBest_Score is None: 
                    finalBest_Score = 0.00 

                if finalBest_Score is not None: 
                    computeProbScore = probability * score
                    finalBest_Score += computeProbScore 
                    finalBest_Action = action
                
        
        if finalBest_Score is None: 
            return  [ Directions.STOP, self.evaluationFunction(gameState) ]
        print("Score probability: ", finalBest_Score)
        #we want to return the finalBest_Action for the getAction function  
        output = [finalBest_Action, finalBest_Score] 
        return output
      

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        agent = 0 
        depth = 0 
        action = self.expectiMax(agent, depth, gameState)  
        return action[0]
        

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)


    newPos = currentGameState.getPacmanPosition()
    listNewFood = currentGameState.getFood().asList()
    ghostPositions = currentGameState.getGhostPositions() 
    minimum_foodList = float('inf')
    manhattan_distance_ghost = 0
    currentnumFood = currentGameState.getNumFood()
    currentCaps = len(currentGameState.getCapsules())

    #this will help to multiply the score whenever the food, capsules, and the distance of the food 
    leftFood = 100000
    leftCaps = 10000
    leftFoodDistance = 1000

    for food in listNewFood:
        if (food[0] > 0) and (food[1] > 0): 
            manhattan_distance_food = manhattanDistance(newPos, food)
            if (minimum_foodList > manhattan_distance_food): 
                minimum_foodList = manhattan_distance_food 
            else: 
                pass
                #print("there is no food!")

        

    for ghost in ghostPositions:
        if (ghost[0] > 0.0) and (ghost[1] > 0.0): 
            manhattan_distance_ghost = manhattanDistance(newPos, ghost)
            if (manhattan_distance_ghost < 2):
                return -1 * (minimum_foodList) 
            else: 
                pass
                #print("ghost is not moving!")

    leftFood += manhattan_distance_ghost

    #compute each probability for the food, distance food, and capsules for the better evaluation 
    scoreResult_1 = 1.0 / (currentnumFood + 1) * leftFood
    scoreResult_2 = 1.0 / (minimum_foodList + 1) * leftFoodDistance
    scoreResult_3 = 1.0 / (currentCaps + 1) * leftCaps

    if (scoreResult_1 is not 0) and (scoreResult_2 is not 0) and (scoreResult_3 is not 0): 
        finalScore_result = (scoreResult_1 + scoreResult_2 + scoreResult_3) 
    else: 
        raise Exception("cannot compute final score")

    return finalScore_result 

   

# Abbreviation
better = betterEvaluationFunction
