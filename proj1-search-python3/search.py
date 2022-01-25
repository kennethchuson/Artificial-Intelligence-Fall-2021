# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"


    #initialize variables: 
    #visited to keep track of explore node
    visited = []
    #getting the list of dicretion action states
    listState_Actions = [] 
    stack_util = util.Stack()

    #push the begin starting state and the list of direction action states
    stack_util.push((problem.getStartState(), listState_Actions))
    
    #check if the stack is empty  
    if (stack_util.isEmpty()): 
        print("stack is empty")
   
    while stack_util:
        #perform a dfs search using stacks iteratively 
        #successors: (x,y) 
        #stateActions: directions = [East, West, South, North]
        (successors, stateActions) = stack_util.pop()
        
        #check if it reaches the goal state
        if problem.isGoalState(successors):
            return stateActions
        else: 
        #while is not visited, mark visited for the successors and stateActions 
            if not successors in visited:
                visited.append(successors)
                list_successors = problem.getSuccessors(successors) 
                #using reverse() to get a fastest search route to the end goal 
                for index in reversed(list_successors): 
                #adding all the stateActions of each directions
                #index[0] = list of successors 
                #index[1] = list of directions 
                        stack_util.push((index[0], stateActions + [index[1]]))


    return stateActions     
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    visited = [] 
    listState_Actions = [] 
    #same as Depth First Search (DFS) algorithm formation, but using a Queue data structure 
    queue_util = util.Queue()

    
    queue_util.push((problem.getStartState(), listState_Actions))

    if (queue_util.isEmpty()): 
        print("queue is empty")

    while queue_util:
        (successors, stateActions) = queue_util.pop()
            
        if problem.isGoalState(successors):
            return stateActions
        else: 
            if not successors in visited:
                visited.append(successors)
                list_successors = problem.getSuccessors(successors) 
                for index in reversed(list_successors): 
                        queue_util.push((index[0], stateActions + [index[1]]))
    
    return stateActions 

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    visited = []
    listState_Actions = []
    #Initialize the costs and the priority costs
    list_costs = 0 
    priority_costs = 0
    #Use a priority queue data structure
    PriorityQueue_util = util.PriorityQueue()

    #takes the start state, list of actions, and listcosts
    #then take the priority cost 
    #takes push(<item>, <priority>)
    PriorityQueue_util.push((problem.getStartState(), listState_Actions, list_costs), priority_costs)

    if (PriorityQueue_util.isEmpty()): 
        print("priority queue is empty")

    while PriorityQueue_util:
        (successors, stateActions, Costs) = PriorityQueue_util.pop()
            
        if problem.isGoalState(successors):
            return stateActions
        else: 
            if not successors in visited:
                visited.append(successors)
                list_successors = problem.getSuccessors(successors) 
                for index in reversed(list_successors): 
                    #adding all action states of each directions and increase the number of costs and priority costs. 
                    #index[0] = list of successors 
                    #index[1] = list of directions 
                    #index[2] = list of cost 
                            PriorityQueue_util.push((index[0], stateActions + [index[1]], Costs + index[2]), Costs + index[2])
    
    return stateActions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited = []
    listState_Actions = []
    list_costs = 0 
    priority_costs = 0 
    #add the priority costs of the heuristic node
    priority_Heuristic = priority_costs + heuristic(problem.getStartState(), problem)
    PriorityQueue_util = util.PriorityQueue()

    PriorityQueue_util.push((problem.getStartState(), listState_Actions, list_costs), priority_Heuristic)

    if (PriorityQueue_util.isEmpty()): 
        print("priority queue is empty")

    while PriorityQueue_util:
        (successors, stateActions, Costs) = PriorityQueue_util.pop()
            
        if problem.isGoalState(successors):
            return stateActions
        else: 
            if not successors in visited:
                visited.append(successors)
                list_successors = problem.getSuccessors(successors) 
                for index in reversed(list_successors): 
                    #add the costs and heuristics nodes together 
                    #compute heuristic (costs + heuristic(successors, problem))
                            PriorityQueue_util.push((index[0], stateActions + [index[1]], Costs + index[2]), Costs + index[2] + heuristic(index[0], problem))
    
    return stateActions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
