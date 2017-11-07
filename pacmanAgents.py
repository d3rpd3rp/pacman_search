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

class chromActionSequence:
    def __init__ (self, sequence):
        self.seq = sequence
        self.score = 0
        self.rank = 0
        self.selected = False     

class mctsNode:
    def __init__ (self, parent = None, score = 0, visited = False, prevAction = None, fullExpansion = False, visitCount = 0, terminal = False):
        self.parent = parent
        self.score = score
        self.prevAction = prevAction
        self.visited = visited
        self.fullExpansion = fullExpansion
        self.children = [ ]
        self.visitCount = visitCount
        self.terminal = terminal  

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
    """
    NOTES
    1. To initialize a sequence, pick five random actions from the ones returned by a getAllPossibleActions call.

    2. "Always return the first action from the sequence with the highest scoreEvaluation." 

    We are sorry if this sentence sounded ambiguous as some reported. It doesn't mean you have to generate multiple 
    sequences for the hill climber algorithm.  You have only one sequence with 5 actions. You return the one which 
    points you to the highest scoreEvaluation(state). Then, each action in the sequence has 50% chance to be changed 
    by random action.
    """

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
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        population = []
        popSize = 8
        for i in range(0, popSize):
            nextChrom = chromActionSequence(buildRandomSequence(state))
            nextChrom.score, nextChrom.seq = scoreAndTruncateActionSeq(state, nextChrom.seq)
            population.append(nextChrom)
        print('after population creation it\'s is sized {}'.format(len(population))) 
        #sorts from low to high
        population.sort(key = lambda x: x.score)
        for j in range(0, len(population)):
            population[j].rank = j + 1
        #need to cycle through whole population
        printPopRanks(population)
        while (countUnselectedPopMembers(population) > 1):
            mom, dad = rankSelect(population)
            #print('mom has rank {} and score {}, dad has rank {} and score {}'.format(mom.rank, mom.score, dad.rank, dad.score))
            if random.random() <= 0.70 and ((mom or dad) is not None):
                firstChild = crossover(mom, dad)
                secondChild = crossover(mom, dad)
                #print ('mom\'s sequence is {}'.format(mom.seq))
                #print ('dad\'s sequence is {}'.format(dad.seq))
                print('firstChild seq is {}'.format(firstChild.seq))
                print('secondChild seq is {}'.format(secondChild.seq))
                #find and remove mom, dad from chroms (population)
                #return filter(lambda s: s[1] == value or s[2] == value, students)
                #print('before filter population is sized {}'.format(len(population)))
                #are there chances the same sequence exists elsewhere? 
                population = filter(lambda x: ((x.seq is not mom.seq) and (x.seq is not dad.seq)), population)
                #print('after filter population is {}'.format(population))
                population.append(firstChild)
                population.append(secondChild)
                #print('after adding children population is sized {}'.format(len(population)))
                #printPopRanks(population)
                #print('after rankSelect call inside the crossover test. mom and dad are {} and {}, number of unselected chroms is {}'.format(mom, dad, countUnselectedPopMembers(population))) 
            else:
                #don't remove mom and dad, but find them in population and mark them selected
                for chromosome in population:
                    if mom.seq == chromosome.seq and mom.rank == chromosome.rank and mom.score == chromosome.score:
                        #print('marking mom visited.')
                        chromosome.selected = True
                    elif dad.seq == chromosome.seq and dad.rank == chromosome.rank and dad.score == chromosome.score:
                        chromosome.selected = True
                        #print('marking dad visited.')
                    else:
                        continue
                #print('ranks after marking parents as selected.')
                #printPopRanks(population)
        for k in range(0, len(population)):
            if random.random() <= 0.10:
                population[k] = mutateAction(population[k], state)
        print('before return of direction...recomputing rank for population.')
        for l in range(0, len(population)):
            population[l].score, population[l].seq = scoreAndTruncateActionSeq(state, population[l].seq) 
        population.sort(key = lambda x: x.score)
        for m in range(0, len(population)):
            population[m].rank = m + 1
        print('ranks after recompute.')
        printPopRanks(population)
        return (returnDirections(population[len(population) - 1].seq[0]))

class MCTSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        global UTCSearchTree
        UTCSearchTree = [ ]
        bestChildAction = UTCSearch(state)
        print('UTCSearch returned {}'.format(bestChildAction))
        return returnDirections(bestChildAction)

def UTCSearch(rootState):
    global UTCSearchTree
    rootNode = mctsNode(visitCount = 1)
    currentState = rootState
    UTCSearchTree.append(rootNode)
    while rootState.generatePacmanSuccessor(random.choice(rootState.getLegalPacmanActions())) is not None:
        lastNode, lastState = treePolicy(rootNode, currentState)
        print('inside for loop of UTCSearch, current state is type {}'.format(type(currentState)))
        terminalStateReward = defaultPolicy(lastState)
        #backup
        backup(lastNode, lastState, rootState)
    #here we return the action which resulted in the "best child"
    #constant down to 0 for this one to remove second term
    constant = 0
    bChild, bsChild = bestChild(rootNode, rootState, 0)    
    return bChild.prevAction

def treePolicy(node, state):
    currentState = state
    while not (currentState.isLose() or currentState.isWin()):
        if not node.fullExpansion:
            return expand(node, state)
        else:
            #constant of 1 as given by assignment document
            constant = 1
            node, state = bestChild(node, currentState, constant)
    return (node, state)

def expand(node, currentState):
    global UTCSearchTree
    legalActions = currentState.getLegalPacmanActions()
    for action in legalActions:
        childNode = mctsNode(parent = node, prevAction = action, visitCount = 1)
        node.children.append(childNode)
        UTCSearchTree.append(childNode)
    #returning a node that has all of its children added
    node.fullExpansion = True
    UTCSearchTree.append(node)
    return (node, currentState)


def bestChild(node, currentState, constant):
    #not sure what value to initialize here...
    max = float("-inf")
    for child in node.children:
        print('In best child, child has score of {}'.format(child.score))
        #constant of 1 as given in the instructions
        cScore, cState = childScore(child, node, currentState, 1)
        if cScore >= max:
            print('assigning bChild...')
            max = cScore
            bChild = child
            bcState = cState
    print('best child was sent {} node.'.format(node))
    if node is not None:
        print('With {} children.'.format(len(node.children)))
    return (bChild, bcState)

def childScore(child, node, currentState, constant):
    childState = currentState.generatePacmanSuccessor(node.prevAction)
    if childState is not None:
        currentBestChildScore = (scoreEvaluation(childState) / child.visitCount) + (constant * (math.sqrt((2 * math.lgamma(node.visitCount) / child.visitCount))))
        print('childState not none, score of {}',format(currentBestChildScore))
        return (currentBestChildScore, childState)
    else:
        return (float("-inf"), currentState)

def defaultPolicy(lastState):
    currentState = lastState
    print('inside default policy currentState is of type {}'.format(type(currentState)))
    if ((not currentState.isLose()) and (not currentState.isWin())):
       for i in range(0, 5):
            print('inside default policy for loop, legal actions are {}'.format(currentState.getLegalPacmanActions()))
            action = random.choice(currentState.getLegalPacmanActions())
            nextState = lastState.generatePacmanSuccessor(action)
            if nextState is not None: 
                if (not nextState.isLose()) and (not nextState.isLose()):
                    currentState = nextState
            else:
                break
    print('in default policy currentState is type {}\n and has actions {}'.format(type(currentState), currentState.getLegalPacmanActions()))
    return currentState    

def backup(lastNode, lastState, rootState):
    node = lastNode
    currentState = lastState.generatePacmanSuccessor(node.prevAction)
    while (node and currentState) is not None and not (currentState.isWin() or currentState.isLose()):
        node.visitCount += 1
        node.score = node.score + normalizedScoreEvaluation(rootState, currentState)
        currentState = currentState.generatePacmanSuccessor(node.prevAction)
        node = node.parent

def isTerminal(state):
    if state.isWin():
        return True
    elif state.isLose():
        return True
    else:
        return False

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
    nextState = None
    for index in range(0, len(sequence) - 1):
        nextState = state.generatePacmanSuccessor(sequence[index])
        if nextState.isLose():
            sequence = [sequence[i] for i in range(0, index)]
            score = scoreEvaluation(nextState)
            print('Lost in scoring computation, sequence returned is {}, length is {}'.format(sequence, len(sequence)))
            if len(sequence) == 0:
                while nextState.isLose():
                    randSeq = buildRandomSequence(state)
                    randIndex = random.randint(0, (len(randSeq) - 1))
                    nextState = state.generatePacmanSuccessor(randSeq[randIndex])
                sequence.append(randSeq[randIndex])
            return (score, sequence)
        elif nextState.isWin():
            score = scoreEvaluation(nextState)
            return (score, sequence)
        else:
           continue
    if nextState is not None:
        score = scoreEvaluation(nextState)
    else:
        print('nextState not created, sequence returned is {}'.format(sequence))
        score = scoreEvaluation(state)
    return (score, sequence)

def rankSelect(population):
    print('inside rankSelect, number of unselected members is {}'.format(countUnselectedPopMembers(population)))
    selectionPop = []
    if countUnselectedPopMembers(population) == 0:
        return (None, None)
    #there should not be a countUnselectedPopMembers(population) == 1 case as every set of parents is 2 and initial population is 8
    elif countUnselectedPopMembers(population) == 2:
        print('only two left ')
        indices = [0, 1]
        randomIndex = random.choice(indices)
        mom = chromActionSequence(population[randomIndex].seq)
        dad = chromActionSequence(population[abs(randomIndex - 1)].seq)
        print('rand index is {} and abs of that minus one is {}'.format(randomIndex, abs(randomIndex - 1)))
        mom.selected = True
        dad.selected = True
        print('inside only two left...mom is {} and dad is {}'.format(mom, dad))
        return (mom, dad)
    else:
        for i in range(0, len(population)):
            if population[i].selected is False:
                rankFactor = population[i].rank - 1
                if rankFactor > 0:
                    for j in range(0, rankFactor):
                        selectionPop.append(population[i])
            else:
                continue
        print('selectionPop is sized {}'.format(len(selectionPop)))
        #print('and is composed of {}'.format(selectionPop))
        if len(selectionPop) > 0:
            mom = random.choice(selectionPop)
            dad = random.choice(selectionPop)
            while dad.rank == mom.rank:
                #print('inside while loop for dad selection.')
                dad = random.choice(selectionPop)
            mom.selected = True
            dad.selected = True
        else:
            mom = None
            dad = None
    return(mom, dad)

def crossover(mom, dad):
    child = chromActionSequence(mom.seq)
    child.selected = True
    lengthDiff = len(child.seq) - len(dad.seq)
    if lengthDiff < 0:
        for i in range(0, len(child.seq)):
            inheritanceTestValue = random.random()
            if inheritanceTestValue > 0.50:
                child.seq[i] = dad.seq[i]
        for k in range(lengthDiff, len(dad.seq)):
            child.seq.append(dad.seq[k])
        print('crossover if statement, child.seq is {}'.format(child.seq))
    else:    
        for j in range(0, len(dad.seq)):
            inheritanceTestValue = random.random()
            if inheritanceTestValue > 0.50:
                child.seq[j] = dad.seq[j]
        print('crossover else statement, child seq is {}'.format(child.seq))
    return(child)

def mutateAction(chrom, state):
    randIndex = random.randint(0, min((len(chrom.seq) - 1), 4))
    randActionList = buildRandomSequence(state)
    print('length of the given chrom is {} length of random seq is {} and randIndex is {}'.format(len(chrom.seq), len(randActionList), randIndex))
    chrom.seq[randIndex] = randActionList[randIndex]
    return (chrom)

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

def countUnselectedPopMembers(population):
    count = 0
    print('chromosomes in population are of type:')
    for chromosome in population:
        print('{}'.format(type(chromosome)))
        if chromosome.selected == False:
            count += 1
        else:
            continue
    return (count)

def printPopRanks(population):
    for index in range(0, len(population)):
        print('Index {} in population is rank {} and score {}'.format(index, population[index].rank, population[index].score))
        print('population sequence is {}'.format(population[index].seq))