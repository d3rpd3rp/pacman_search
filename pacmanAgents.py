# pacmanAgents.py
# ---------------
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


from pacman import Directions
from game import Agent
from heuristics import *
import random
import math

class Node:
    def __init__ (self, state, parent = None, prevAction = None):
        self.state = state
        self.parent = parent
        self.prevAction = prevAction
        self.score = scoreEvaluation(state)
    
    def traceback(self):
        sequence = []
        #only root (start node) should have this quality
        if self.parent == None:
            return (sequence)
        sequence.append(self.prevAction)
        nextNode = self.parent
        if nextNode.prevAction is not None:
            sequence.append(nextNode.prevAction)
            while nextNode.parent is not None:
                nextNode = nextNode.parent
                if nextNode.prevAction is not None:
                    sequence.append(nextNode.prevAction)
            return (sequence)
        else:
            return (sequence)

class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class RandomSequenceAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = []
        for i in range(0,10):
            self.actionList.append(Directions.STOP)
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        possible = state.getAllPossibleActions()
        for i in range(0,len(self.actionList)):
            self.actionList[i] = possible[random.randint(0,len(possible)-1)]
        tempState = state
        for i in range(0,len(self.actionList)):
            if tempState.isWin() + tempState.isLose() == 0:
                tempState = tempState.generatePacmanSuccessor(self.actionList[i])
            else:
                break
        # returns random action from all the valide actions
        return self.actionList[0]

class GreedyAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(scoreEvaluation(state), action) for state, action in successors]
        # get best choice
        bestScore = max(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)

def hillClimber(state, sequence):
    #consider the request the root of search and create root (start) node
    print ('sequence at beginning of hillClimber is {}'.format(sequence))
    for index in range(0, (len(sequence) - 1)):
        nextState = state.generatePacmanSuccessor(sequence[index])
        if random.choice((True, False)):
            if nextState.isWin():
                    return(nextState, sequence) 
            elif nextState.isLose():
                while nextState.isLose():
                    sequence[index] = random.choice(nextState.getAllPossibleActions())
                    nextState = nextState.generatePacmanSuccessor(sequence[index])
                    print('found losing state in hillclimber.')
            else:
                    sequence[index] = random.choice(nextState.getAllPossibleActions())
                    nextState = nextState.generatePacmanSuccessor(sequence[index])
        else:
            nextState = state.generatePacmanSuccessor(sequence[index])
            continue
    print ('sequence at the end of hillClimber is {}'.format(sequence))  
    return (nextState, sequence)

def ReturnDirections(move):
    if move == 'East':
        return Directions.EAST 
    elif move == 'West':
        return Directions.WEST
    elif move == 'North':
        return Directions.NORTH
    elif move == 'South':
        return Directions.SOUTH
    else:
        print('returning STOP. move passed was {}'.format(move))
        return Directions.STOP

def findHighScoreKey(nodeDict):
    items = [(v, k) for k, v in nodeDict.items()]
    items.sort()
    items = [(k, v) for v, k in items]
    #print('items is of type: {}'.format(type(items)))
    #print('sorted list is: {}'.format(items))
    maxValue = 0
    for key, value in items:
        if value > maxValue:
            maxValue = value
            maxKey = key
        elif value == maxValue:
            if random.choice([True, False]):
                maxValue = value
                maxKey = key
            else:
                continue
        else:
            continue
    return (maxKey)

class HillClimberAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        #consider the request the root of search and create root (start) node
        initRandomSequence = [ ]
        initRandomSequence.append(random.choice(state.getAllPossibleActions()))
        firstAction = initRandomSequence[0]
        #print ('initRandomSequence is {}'.format(initRandomSequence))
        nextState = state.generatePacmanSuccessor(firstAction)
        #win return next direction to win NOW
        if nextState.isWin():
            return initRandomSequence[0]
        #lose need to keep testing AllPossibleActions, could endlessly loop?
        elif nextState.isLose():
            while nextState.isLose():
                print('found losing state in second state of agent call.')
                initRandomSequence.pop()
                initRandomSequence.append(random.choice(state.getAllPossibleActions()))
                nextState = state.generatePacmanSuccessor(initRandomSequence[0])         
        else:
            while len(initRandomSequence) < 5:
                initRandomSequence.append(random.choice(nextState.getAllPossibleActions()))
                nextState = nextState.generatePacmanSuccessor(initRandomSequence[len(initRandomSequence) - 1])
                if nextState.isWin():
                    continue 
                elif nextState.isLose():
                    while nextState.isLose():
                        print('found losing state in random sequence building of agent call.')
                        initRandomSequence.pop()
                        initRandomSequence.append(random.choice(nextState.getAllPossibleActions()))
                        nextState = state.generatePacmanSuccessor(initRandomSequence[len(initRandomSequence) - 1])
            #print ('initRandomSequence is after generating full sequence {}'.format(initRandomSequence))
            sequence = initRandomSequence
            hillClimberState, hillClimberSequence = hillClimber(state, sequence)
            if scoreEvaluation(hillClimberState) > scoreEvaluation(nextState):
                print('choosing hillClimber with score of {}'.format(scoreEvaluation(hillClimberState)))
                return(hillClimberSequence[0])
            else:
                print('choosing default sequence with score of {}'.format(scoreEvaluation(nextState)))
                return(sequence[0])

        """
                    function HILL-CLIMBING(pmblem) 
                    returns a state that is a local maximum
                    current = MAKE-NODE(problem.lNITIAL-STATE)
                    loop do
                        neighbor = a highest-valued successor of curTent
                        if neighbor.VALUE <= current.VALUE then return current.STATE
                        current = neighbor
        """      
                 


class GeneticAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write Genetic Algorithm instead of returning Directions.STOP
        return Directions.STOP

class MCTSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write MCTS Algorithm instead of returning Directions.STOP
        return Directions.STOP
