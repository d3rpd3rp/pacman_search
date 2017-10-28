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
    bestScoreNode = neighbor
    legal = neighbor.state.getAllPossibleActions()
    for action in legal:
        #print('neighbor has all the possible actions: {}'.format(legal))
        global successorCallCount 
        successorCallCount += 1
        secondNeighborNode = Node(neighbor.state.generatePacmanSuccessor(action), neighbor, action)
        if secondNeighborNode.score > bestScoreNode.score:
            print('in seachNeighbors, assigning best score as {}'.format(bestScoreNode.score))
            bestScoreNode = secondNeighborNode
        #already took two actions to get second neighbor, so only need a depth of 3 to return a max seq length of 4
        secondNeighborSearchBestNode = depthLimitedDFS(secondNeighborNode, 2, 5, bestScoreNode)
        if secondNeighborSearchBestNode.score > bestScoreNode.score:
            bestScoreNode = secondNeighborSearchBestNode
    print ('search Neighbors returns Node is now of type {} and has score {}'.format(type(bestScoreNode), bestScoreNode.score))
    return (bestScoreNode, neighbor.prevAction)


def depthLimitedDFS (nextNeighbor, depth, limit, bestScoreNode):
    #print('in limited DFS...bestScoreNode is of type {}'.format(type(bestScoreNode)))
    legal = nextNeighbor.state.getAllPossibleActions()
    for action in legal:
        global successorCallCount 
        successorCallCount += 1
        nextState = nextNeighbor.state.generatePacmanSuccessor(action)
        if nextState is not None: 
            nextNode = Node(nextState, nextNeighbor, action)
            if nextNode.state.isLose():
                if nextNode.score > bestScoreNode.score:
                    print('in dlDFS - lost state, assigning best score as {}'.format(bestScoreNode.score))
                    bestScoreNode = nextNode
                continue
            elif nextNode.state.isWin():
                if nextNode.score > bestScoreNode.score:
                    print('in dlDFS - win state, assigning best score as {}'.format(bestScoreNode.score))
                    bestScoreNode = nextNode 
                continue
            else:
                if depth <= limit:
                    if nextNode.score > bestScoreNode.score:
                        print('in dlDFS - win state, assigning best score as {}'.format(bestScoreNode.score))
                        bestScoreNode = nextNode
                        #print('in limited DFS...searching from node at depth {} with score {}'.format(depth, nextNode.score))
                    depth += 1
                    depthLimitedDFS(nextNode, depth, limit, bestScoreNode)
                else:
                    if nextNode.score > bestScoreNode.score:
                        print('in dlDFS - win state, assigning best score as {}'.format(bestScoreNode.score))
                        bestScoreNode = nextNode
        else:
            continue
    #print('returning node with score {} as bestScoreNode from DFS.'.format(bestScoreNode.score))
    return (bestScoreNode)

class HillClimberAgent(Agent):
    #some global counters
    global successorCallCount, knownStates
    successorCallCount = 0
    knownStates = { }


    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        #add first entry to dict of known states, for future optimization of not recomputing known state spaces
        knownStates[state] = scoreEvaluation(state)
        #consider the request the root of search and create root (start) node
        startNode = Node(state)
        #initialize the bestNeighborNodes list (small dictionary of score, stop node)
        bestNeighborNodes = { }
        legal = state.getAllPossibleActions()
        for action in legal:
            global successorCallCount 
            successorCallCount += 1
            nextState = state.generatePacmanSuccessor(action)
            if nextState:
                neighborNode = Node(state.generatePacmanSuccessor(action), startNode, action)
                #test if this state is identical to a previous state from actions loop line 162
                if knownStates[state]:
                    continue
                #not sure if test is going to break something...
                elif neighborNode.state.isLose():
                    #do I need to consider if this node has a high score on it's path somewhere?
                    continue
                else:
                    bestScoreNode, firstAction = searchNeighbors(neighborNode)
                    print('sequence from bestScoreNode traceback is {}'.format(bestScoreNode.traceback()))
                    print('back in getAction for Hill Climber first action is {}.'.format(firstAction))

        return firstAction

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
