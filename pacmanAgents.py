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

def searchNeighbors(neighbor):
    global sequence 
    bestScoreNode = neighbor
    legal = neighbor.state.getLegalPacmanActions()
    for action in legal:
        secondNeighborNode = Node(neighbor.state.generatePacmanSuccessor(action), neighbor, action)
        if secondNeighborNode.state.isWin():
            #need to field this in the return somewhere
            return secondNeighborNode
        elif secondNeighborNode.state.isLose():
            continue
        if secondNeighborNode.score > bestScoreNode.score:
            bestScoreNode = secondNeighborNode
            lastAction = action
        #already took two actions to get second neighbor, so only need a depth of 3 to return a max seq length of 4
        secondNeighborSearchBestNode = depthLimitedDFS(secondNeighborNode, 2, 5, bestScoreNode)
        if secondNeighborSearchBestNode.score > bestScoreNode.score:
            bestScoreNode = secondNeighborSearchBestNode
            lastAction = action
    print ('search Neighbors returns Node is now of type {} and has score {}'.format(type(bestScoreNode), bestScoreNode.score))
    sequence.append(secondNeighborNode.prevAction)
    sequence.append(lastAction)
    print('sequence from searchNeighbors is now {}'.format(sequence))
    return (bestScoreNode)

def depthLimitedDFS (nextNeighbor, depth, limit, bestScoreNode):
    legal = nextNeighbor.state.getLegalPacmanActions()
    for action in legal:
        nextState = nextNeighbor.state.generatePacmanSuccessor(action)
        if nextState is not None: 
            nextNode = Node(nextState, nextNeighbor, action)
            if nextNode.state.isLose():
                continue
            elif nextNode.state.isWin():
                bestScoreNode = nextNode 
                #winning state is terminal
                return (bestScoreNode)
            else:
                if depth <= limit:
                    if nextNode.score > bestScoreNode.score:
                        bestScoreNode = nextNode
                    depth += 1
                    depthLimitedDFS(nextNode, depth, limit, bestScoreNode)
                else:
                    if nextNode.score > bestScoreNode.score:
                        bestScoreNode = nextNode
        else:
            continue
    return (bestScoreNode)

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
    #some global counters
    global sequence
    #must initialize to keep slots for sequence open
    sequence = [ ]
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        global sequence
        while sequence:
            directions = state.getAllPossibleActions()
            randomSequence = random.sample(directions, len(directions))
            if random.choice((True, False)):
                move = sequence.pop()
                randomSequence.pop()
            else:
                print('choosing random action.')
                move = randomSequence.pop()
                sequence.pop()
            print('sequence in while loop is {}'.format(sequence))
            return(ReturnDirections(move))

        #consider the request the root of search and create root (start) node
        startNode = Node(state)
        #initialize the bestNeighborNodes list (small dictionary of score, stop node)
        bestNeighborNodes = { }
        firstActions = { }
        legal = state.getLegalPacmanActions()
        for action in legal:
            nextState = state.generatePacmanSuccessor(action)
            if nextState:
                neighborNode = Node(state.generatePacmanSuccessor(action), startNode, action)
                if neighborNode.state.isLose():
                    #do I need to consider if this node has a high score on it's path somewhere?
                    continue
                else:
                    #must initialize to keep slots for sequence open
                    directions = state.getAllPossibleActions()
                    randomSequence = random.sample(directions, len(directions))
                    bestScoreNode = searchNeighbors(neighborNode)
                    sequence.append(action)
                    lastKnownActions = bestScoreNode.traceback()
                    for k in lastKnownActions:
                        sequence.append(k)
                    list(reversed(sequence))
                    print('sequence in else init is {}'.format(sequence))
                    if random.choice((True, False)):
                        move = sequence.pop()
                        randomSequence.pop()
                    else:
                        print('choosing random action.')
                        move = randomSequence.pop()
                        sequence.pop()
                    return(ReturnDirections(move))


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
