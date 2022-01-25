# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        #initialize the q value from the util counter to return the result in getQValue function 
        self.Q_values = util.Counter()



    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        #tuple of state and action 
        state_action = (state, action) 
        #should return 0.0 if we have never seen a state 
        if state is None: 
          return 0.0 
        #returns Q(state, action) 
        return self.Q_values[state_action]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"

        #define the list of Q values we have 
        #getting the legal actions 
        list_QValues = [] 
        legal_actions = self.getLegalActions(state) 
        
        #Note that if
        #there are no legal actions, which is the case at the
        #terminal state, you should return a value of 0.0.
        if len(legal_actions) == 0: 
          return 0.0 

        #iterate through legal of actions, use getQValue and put them into a list of q values
        for action in legal_actions: 
          getQVal = self.getQValue(state, action) 
          list_QValues.append(getQVal) 
        
        #find the maximum inside the list of q values 
        result = max(list_QValues)
        
        return result

        
        


    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"

        max_action = None
        max_q_val = 0

        #getting the legal actions 
        legal_actions = self.getLegalActions(state) 
        
        # Note that if there
        # are no legal actions, which is the case at the terminal state,
        # you should return None.
        if len(legal_actions) == 0: 
          return None
        
        for action in legal_actions:
            getQVal = self.getQValue(state, action)
            #find the maximum of actions and q values
            if max_action is None or getQVal > max_q_val:
                max_q_val = getQVal
                max_action = action

        return max_action


    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"

        #Q7 Epsilon Greedy 
        #this is a simulation of binary variable with probability p of success using a flipCoin from util.py
        explore_greedy = util.flipCoin(self.epsilon)

        #return whatever action is there if there is no legal actions 
        if len(legalActions) == 0:
            return action

        #if flip coin is true, them we do random choice of legal actions 
        if explore_greedy == True:
            return random.choice(legalActions)

        #otherwise compute the action from q values 
        return self.computeActionFromQValues(state)

   

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"

        #We need these functions for the update function, to compute the update. 
        QValue_max = self.computeValueFromQValues(nextState)
        legalActions = self.getLegalActions(state) 
        getQVal = self.getQValue(state,action)
        state_action = (state, action) 
        alpha = self.alpha
        computeUpdate = 0.0

        #return the whatever reward is if there is no legal actions 
        if len(legalActions) == 0: 
          computeUpdate = reward

        #this is temporal difference learning 
        #update to V(s): Vpi(s) <- (1 - a)Vpi(s) + (a) <sample> [R(s, a, s') + vVpi(s')]
        computeUpdate = (1 - alpha) * getQVal + alpha * (reward + QValue_max * self.discount)

        self.Q_values[state_action] = computeUpdate

        return self.Q_values[state_action]


    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        #computing the Q function using the formula 
        #Q(s, a) = sum 1 to n ( fi(s,a) * wi )
        result_qVal = 0 
        features = self.featExtractor.getFeatures(state, action) 

        for i in features: 
          result_qVal += (features[i] * self.weights[i])
        
        return result_qVal 
        

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        #compute the update using the difference and r is where the experience reward
        #difference = (r + y max( Q(s', a'))) - Q(s, a) 
        difference = (reward + self.discount * self.getValue(nextState)) - self.getQValue(state, action) 
        features = self.featExtractor.getFeatures(state, action) 
        for i in features: 
          self.weights[i] += (self.alpha * difference * features[i])
        
        return self.weights[len(features)]
      
      
      

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
