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

class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class RandomSequenceAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = [];
        for i in range(0,10):
            self.actionList.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        possible = state.getAllPossibleActions();
        for i in range(0,len(self.actionList)):
            self.actionList[i] = possible[random.randint(0,len(possible)-1)];
        tempState = state;
        for i in range(0,len(self.actionList)):
            if tempState.isWin() + tempState.isLose() == 0:
                tempState = tempState.generatePacmanSuccessor(self.actionList[i]);
            else:
                break;
        # returns random action from all the valide actions
        return self.actionList[0];

class GreedyAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

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
        global finalSeq
        finalSeq = []
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        global finalSeq
        if len(finalSeq) < 1:
            randSeq = buildRandomSequence(state)
            hillClimbSeq = hillClimbBuildNeighborSequence(state, randSeq)
            hillClimbScore, hillClimbSeq = scoreAndTruncateActionSeq(state, hillClimbSeq)
            randScore, randSeq = scoreAndTruncateActionSeq(state, randSeq)
            if randScore > hillClimbScore:
                finalSeq = randSeq
                print('chose random sequence with score {}'.format(randScore))
            else:
                finalSeq = hillClimbSeq
                print('chose hillClimber sequence with score {}'.format(randScore))
            #reverse list to pop actions
            finalSeq.reverse()
            print('executing action {} in list.'.format(finalSeq[len(finalSeq) - 1]))
            nextAction = returnDirections(finalSeq.pop())
            return (nextAction)
        else:
            print('executing action {} in list.'.format(finalSeq[len(finalSeq) - 1]))
            nextAction = returnDirections(finalSeq.pop())
            return (nextAction)

class GeneticAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write Genetic Algorithm instead of returning Directions.STOP
        return Directions.STOP

class MCTSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write MCTS Algorithm instead of returning Directions.STOP
        return Directions.STOP

def buildRandomSequence(state):
    sequence = [None] * 5
    for index in range(0, 5):
        sequence[index] = random.choice(state.getAllPossibleActions())
    return (sequence)

def hillClimbBuildNeighborSequence(state, randSeq):
    #print ('sequence at beginning of hillClimber is {}'.format(randSeq))
    hillClimbSeq = randSeq
    for index in range(0, (len(randSeq) - 1)):
        if random.choice((True, False)):
                hillClimbSeq[index] = random.choice(state.getAllPossibleActions())
        else:
            continue
    #print ('sequence at the end of hillClimber is {}'.format(hillClimbSeq))  
    return (hillClimbSeq)

def scoreAndTruncateActionSeq(state, sequence):
    for index in range(0, len(sequence) - 1):
        nextState = state.generatePacmanSuccessor(sequence[index])
        if nextState.isLose():
            sequence = [sequence[i] for i in range(0, index)]
            score = scoreEvaluation(state)
            print('Lost in scoring computation, sequence returned is {}'.format(sequence))
            return (score, sequence)
        elif nextState.isWin():
            score = scoreEvaluation(state)
            return (score, sequence)
        else:
           continue
    score = scoreEvaluation(nextState)
    return (score, sequence)
    
def returnDirections(move):
    if move == ('East' or 'EAST'):
        return Directions.EAST 
    elif move == ('West' or 'WEST'):
        return Directions.WEST
    elif move == ('North' or 'NORTH'):
        return Directions.NORTH
    elif move == ('South' or 'SOUTH'):
        return Directions.SOUTH
    else:
        print('returning STOP. move passed was {}'.format(move))
        return Directions.STOP



