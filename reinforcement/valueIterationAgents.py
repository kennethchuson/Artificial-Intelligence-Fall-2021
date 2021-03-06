# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        #after implementing both computeQValueFromValues and computeActionFromValues function. 
        #we need to run the iterations of every states, then run the equation.
        #equation of iteration state update
       #and this will have for Vk + 1(s) 
        for iteration in range(0, self.iterations):
            copyValues = self.values.copy()
            states = self.mdp.getStates()
            for state in states:
                if self.mdp.isTerminal(state): 
                    self.values[state] = 0
                if not self.mdp.isTerminal(state): 
                    self.values[state] = -float('inf')
                    actions = self.mdp.getPossibleActions(state) 
                    for action in actions:
                        valueResult = 0 
                        #made a copy for the compute Q value from values 
                        TransStatesProbs = self.mdp.getTransitionStatesAndProbs(state,action)
                        for [nextStateTrans, transProbability] in TransStatesProbs:
                            # sum( T(s, a, s') * [R(s, a, s') + vVk(s')] ) 
                            valueResult += transProbability * (self.mdp.getReward(state, action, nextStateTrans) + self.discount * copyValues[nextStateTrans])
                        #made a copy for the compute action from values 
                        #max (self.values[state]) -> Vk + 1(s) 
                        self.values[state] = max(self.values[state], valueResult)
                    
                

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"

        #should return None when state is terminal 
        #the QValue from values will calculate the the forumla of sum(T(s, a, s') [R(s, a, s') + vVk(s')])
        #which using transition state, reward, discount, and values of the next state 
        if self.mdp.isTerminal(state): 
            return None

        calculate = 0
        getTransStatesProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        for [nextStateTrans, transProbability] in getTransStatesProbs:
            calculate += transProbability * (self.mdp.getReward(state, action, nextStateTrans) + self.discount * self.values[nextStateTrans])
        return calculate

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        #should return None when state is terminal 
        #the action from values will compute the best action. 
        #when getting all the possible actions, we need to find the maximum values from the QValue from values function 
        if self.mdp.isTerminal(state): 
            return None

        actions = self.mdp.getPossibleActions(state)
        max_val = -float('inf')
        final_action = None
   
        for action in actions:
            actionValue = self.computeQValueFromValues(state, action)
            if actionValue > max_val:
                max_val = actionValue
                final_action = action
        return final_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

