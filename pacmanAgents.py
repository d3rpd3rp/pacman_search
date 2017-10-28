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

class HillClimberAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return
    
    def searchNeighbors(neighbor):
        bestScoreNode = neighbor
        legal = neighbor.state.getAllPossibleActions()
        for action in legal:
            secondNeighborNode = Node(state.generatePacmanSuccessor(action), neighbor, action)
            if secondNeighborNode.score > bestScoreNode.score:
                bestScoreNode = secondNeighborNode
            #already took two actions to get second neighbor, so only need a depth of 3 to return a max seq length of 4
            secondNeighborBestNode = depthLimitedDFS(neighborNode, 0, 3)
            if secondNeighborSearchSequenceBestNode.score > bestScoreNode.score:
                bestScoreNode = secondNeighborSearchSequenceBestNode
            
    def depthLimitedDFS (neighbor, depth, limit, bestScoreNode):
        legal = neighbor.state.getAllPossibleActions()
        for action in legal:
            nextNode = Node(state.generatePacmanSuccessor(action), neighbor, action)
            if nextNode.state.isLose():
                if nextNode.score > bestScoreNode.score:
                    bestScoreNode = nextNode
                continue
            elif nextNode.state.isWin():
                if nextNode.score > bestScoreNode.score:
                    bestScoreNode = nextNode 
                continue
            else:
                if depth <= limit:
                    if nextNode.score > bestScoreNode.score:
                        bestScoreNode = nextNode
                    depth += 1
                    DFS(nextNode, depth, limit)
                else:
                    if nextNode.score > bestScoreNode.score:
                        bestScoreNode = nextNode
                    print('returning node with score {} as bestScoreNode from DFS.'.format(bestScoreNode.score))
                    return (bestScoreNode)


    # GetAction Function: Called with every frame
    def getAction(self, state):
        #consider the request the root of search and create root (start) node
        startNode = Node(state)
        #initialize the bestNeighborNodes list (small dictionary of score, stop node)
        bestNeighborNodes = { }
        legal = state.getAllPossibleActions()
        for action in legal:
            neighborNode = Node(state.generatePacmanSuccessor(action), startNode, action)
            #not sure if test is going to break something...
            if neighborNode.state.isLose():
                #do I need to consider if this node has a high score on it's path somewhere?
                continue
            else:
                searchNeighbors(neighborNode)

        return Directions.STOP

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
