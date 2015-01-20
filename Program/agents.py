import time, csv, os, sys
from game import Agent
from game import Deck
from fiveopoker import GameState
from util import *
from numpy import prod, zeros, count_nonzero
from itertools import *
from greedyEval1 import greedyEval1
from greedyEval2 import greedyEval2, greedyEval3, fastGreedyEval2, eval, fastEval
from probTable import ProbTable
import monteCarloEvaluator
import cardsDict

gcounter = 0

class SearchAgent(Agent):
    """
    This is an abstract class.
    """
    def __init__(self, name, evalFn, depth = 10) :
        Agent.__init__(self, name)
        self.evaluationFunction = lookup(evalFn, globals() )
        self.maxDepth = int(depth)

class MinimaxAgent(Agent) :
    
    def getAction(self, state):
        """
        return an ACTION
        """
        start = time.time()
        self.tracks = 0
        actions = Counter()
        legal = state.getLegalActions(self.index)
        if len(legal) == 1 : return legal[0]

        for action in legal :
            actions[action] = self.maxValue(0, state )

        print "Time:\t",time.time() - start
        print "Tracks Checked:\t",self.tracks
        
        return actions.argMax()
    
    def maxValue(self, depth, state):
        """
        returns a UTILITY VALUE
        """
        if state.isGameOver() :
            self.tracks +=1
            if self.tracks%100 ==0:
                print self.tracks
            return state.isWinner(self.index) and 1 or 0
        
        maxVal = -99999
        for action in state.getLegalActions(self.index):
            tmpVal = self.minValue(depth+1, state.doAction(self.index, action) )
            state.removeAction(self.index, action) 
            maxVal = maxVal > tmpVal and maxVal or tmpVal
        return maxVal

    def minValue (self, depth, state):
        """
        returns a UTILITY VALUE
        """
        if state.isGameOver() :
            self.tracks +=1
            if self.tracks%100 ==0:
                print self.tracks
            return state.isWinner(self.index) and 1 or 0
        minVal = 999999
        op = (self.index+1)%2
        for action in state.getLegalActions( op):
            tmpVal = self.maxValue(depth+1, state.doAction(op, action) )
            state.removeAction(op, action)
            minVal = minVal < tmpVal and minVal or tmpVal
        return minVal

class ApproxMinimaxAgent(MinimaxAgent):

    def __init__(self, name, maxTime = 30, n = 10000) :
        MinimaxAgent.__init__(self, name)
        self.maxTime = maxTime*1000
        self.n  = n

    def getAction(self, state):
        actions = Counter()
        legal = state.getLegalActions(self.index)
        if len(legal) == 1 : return legal[0]
        for action in legal :
            actions[action] = self.monteCarloApprox(state, action, self.maxTime/len(state.getLegalActions(self.index) ) )
        return actions.argMax()


    def monteCarloApprox(self, state, action, maxTime) :
        """
        returns a UTILITY VALUE
        """
        val = 0
        counter = 0
        currMillis = int(round(time.time() * 1000))
        nextCard =state.getDeck().pop()
        newDeck = state.getAgentState(self.index).getUnseenCards().deepcopy()
        while counter < self.n and int(round(time.time() * 1000)) - currMillis <= maxTime :
            counter += 1
            newState = state.deepcopy()
            newDeck.shuffle()
            newDeck.insert(0, nextCard)
            newState.setDeck(newDeck)
            val+= self.maxValue(0, newState)
        print 'tracks: ', counter
        state.getDeck().insert(0,nextCard)
        return val/counter
                         
class HMinimaxAgent(SearchAgent) :
    
    def getAction(self, state):
        start = time.time()
        action = self.minimax(state)
        print time.time() - start
        return action
    
    def minimax(self, state):
        """
        return an ACTION
        """
        legal = state.getLegalActions(self.index)
        if len(legal) == 1 : return legal[0]

        actions = Counter()
        alpha = -float("inf")
        beta = float("inf")
        for action in legal :
            state.doAction(self.index, action)
            actions[action] = self.maxValue(0, state, alpha, beta )
            alpha = max(actions.values() ) - 0.001
            state.removeAction(self.index, action)
            
        return actions.argMax()


    def maxValue(self, depth, state,alpha,beta):
        """
        returns a UTILITY VALUE
        """
        if state.isGameOver():
            return state.winEval(self.index)
        if depth == self.maxDepth:
            return self.evaluationFunction(self.index,state)
        
        for action in state.getLegalActions(self.index):
            state.doAction(self.index, action)
            alpha = max(alpha,self.minValue(depth+1, state,alpha,beta ) )
            state.removeAction(self.index, action) 
            if alpha >= beta: 
                break
        return alpha

    def minValue (self, depth, state,alpha,beta):
        """
        returns a UTILITY VALUE
        """
        if state.isGameOver():
            return state.winEval(self.index)
        if depth == self.maxDepth:
            return self.evaluationFunction(self.index,state)
        
        op = (self.index+1)%2
        for action in state.getLegalActions( op):
            state.doAction(op, action)
            beta = min(beta,self.maxValue(depth+1, state,alpha,beta ) )
            state.removeAction(op, action)
            if alpha >= beta: 
                break
        return beta
    
class ApproxHMinimaxAgent(HMinimaxAgent):
    def __init__(self, name, evalFn, depth = 3, maxTime = 60, n = 10000) :
        HMinimaxAgent.__init__(self, name, evalFn, depth)
        self.n  = n
        self.maxTime = maxTime

    def getAction(self, state):
        sTime = time.time()
        legal = state.getLegalActions(self.index)
        state.data.totPlyNum -= 1

        if len(legal) == 1 : return legal[0]
        print 'minimax is thinking...'
        action = self.monteCarloApprox(state, self.maxTime )
        
        print time.time() - sTime
        return action


    def monteCarloApprox(self, state, maxTime) :
        """
        returns an ACTION
        """
        monTrack = 0
        currMillis = int(round(time.time()))
        nextCard = state.getDeck().pop()
        sampleSize = min(len(state.getDeck()),self.maxDepth)
        actions = Counter()
#         (monTrack < self.n) and 
        while ((int(round(time.time())) - currMillis < maxTime)) :
            monTrack += 1
            newDeck = Deck(random.sample(state.getAgentState(self.index).getUnseenCards() , sampleSize))
            newDeck.add( nextCard)
            newState = state.deepcopy()
            newState.setDeck(newDeck)
            bestAction = self.minimax(newState)
            actions[bestAction] +=1

        print 'Decks Checked:\t ', monTrack

        return actions.argMax()

class GreedyAgent(SearchAgent) :
    
    def getAction(self, state):
        # Goes over the legal moves
        bestMove = ""
        bestScore = -999
        legalMove = state.getLegalActions(self.index)
        if len(legalMove) == 1: return legalMove[0]
        actions = Counter()
        for action in legalMove:
            tmpState = state.generateSuccessor(self.index, action)
            tmpScore = self.evaluationFunction(self.index, tmpState)
            actions[action] = tmpScore  
        return actions.argMax()

class ReflexAgent1(Agent) :

    def getAction(self, state) :
        legal = state.getLegalActions(self.index)
        if len(legal) == 1 : return legal[0]
        actionVals = Counter()
        for action in legal :
            tmpState = state.generateSuccessor(self.index, action)
            myHand = eval(tmpState.getHands(self.index)[action], self.index, tmpState)
            oppHand = eval(tmpState.getHands((self.index + 1)%2)[action], (self.index + 1)%2, tmpState)
            diff = myHand - oppHand
            actionVals[action] = diff
        return actionVals.argMax()

class ReflexAgent2(Agent) :

    def getAction(self, state) :
        legal = state.getLegalActions(self.index)
        if len(legal) == 1 : return legal[0]
        actionVals = Counter()
        for action in legal :
            tmpState = state.generateSuccessor(self.index, action)
            actionVals[action] = eval(tmpState.getHands(self.index)[action], self.index, tmpState)
        return actionVals.argMax()

class ReflexAgent3(Agent) :

    def getAction(self, state) :
        legal = state.getLegalActions(self.index)
        if len(legal) == 1 : return legal[0]
        actionVals = Counter()
        for action in legal :
            preAction = eval(state.getHands(self.index)[action], self.index, state)
            tmpState = state.generateSuccessor(self.index, action)
            postAction = eval(tmpState.getHands(self.index)[action], self.index, tmpState)
            #start = time.clock()
            actionVals[action] = postAction - preAction
            #print 2, time.clock() - start
        return actionVals.argMax()

class ReflexAgent4(Agent) :
    
    def getAction(self, state) :
        legal = state.getLegalActions(self.index)
        if len(legal) == 1 : return legal[0]
              
        unseenCards = state.getAgentState(self.index).getUnseenCards().asList()
        unseenArr = zeros(52, dtype = 'int')
        
        for i in unseenCards:
            unseenArr[i-1] = 1
        unseenArr.shape = (13,4)
        unseenSize = count_nonzero(unseenArr)   
         
        actionVals = Counter()
        for action in legal :
            start = time.clock()
            tmpState = state.doAction(self.index, action)
            print time.clock() - start
            actionVals[action] = fastEval(tmpState.getHands(self.index)[action], self.index, tmpState, unseenArr, unseenSize)
        
        return actionVals.argMax()

class MonteCarloAgent(Agent):

    def __init__(self, name, dirName) :
        Agent.__init__(self, name)
        self.probAgent = None
        self.dirName = dirName
    
    def reset(self) :
        self.probAgent = None

    def getAction(self, state) :
        #if state.data.totPlyNum >= 10 :
        #    if self.probAgent == None :
        #        self.probAgent = ProbAgent(self.name, self.dirName)
        #        self.probAgent.index = self.index
        #        self.probAgent.initialize(state)
        #    return self.probAgent.getAction(state)
        
        utilValues = Counter()
        legal = state.getLegalActions(self.index)
        if len(legal) == 1: return legal[0]
        monte = monteCarloEvaluator.MonteCarloEvaluator(state,self.index)
        for action in legal:
            utilValues[action] = monte.eval(action)
        return utilValues.argMax()

    def terminate(self) :
        if self.probAgent is not None: 
            self.probAgent.terminate()

class ProbAgent(Agent):
    
    def __init__(self, name, dirName) :
        Agent.__init__(self, name)
        self.handTables = None
        self.dirName = dirName
        

    def initialize(self, initState) :
        self.handTables = dict()
        for i in range(5):
            handName = cardsDict._HANDS[i]
            tableName = self.name  + handName
            self.handTables[handName] = ProbTable(initState.getHands(self.index)[handName], initState.getOppHands(self.index)[handName], initState.getAgentState(self.index).getUnseenCards(), tableName, self.dirName)

    def getAction(self, state):
        
        legal = state.getLegalActions(self.index)
        if len(legal) == 1 : return legal[0]
        actions = Counter()

        if state.data.totPlyNum <= 10 :
            monte = monteCarloEvaluator.MonteCarloEvaluator(state, self.index)
            for action in legal:
                actions[action] = monte.eval(action)
            return actions.argMax()

        if self.handTables == None: self.initialize(state)
        actionsProbs = dict()

        nextCard = state.getDeck().pop()
        state.getAgentState(self.index).configuration.revealCard(nextCard)
        unseenCards = state.getAgentState(self.index).getUnseenCards()[:]
        for i in range(5):
            action = cardsDict._HANDS[i]

            self.handTables[action].update(unseenCards, nextCard)
            if action in legal:
                putProb, waitProb = self.handTables[action].getProb(state.getHands(self.index)[action], state.getOppHands(self.index)[action], nextCard)
                actionsProbs[action] = putProb, waitProb

            else :
                waitProb = self.handTables[action].getWaitProb(state.getHands(self.index)[action], state.getOppHands(self.index)[action], nextCard)
                actionsProbs[action] = 0, waitProb
                putProb = 0
        
        for action in legal:
            winProb = self.getWinProb(actionsProbs, action)
            actions[action] = winProb 

        return actions.argMax()

    def getWinProb(self, actionsProbs, selectedAction):
        """
        actionProbs is a (Action, (putProb, winProb) ) pair
        """
        probsDict = dict()
        for action, probs in actionsProbs.items():
            if action == selectedAction : 
                probsDict[action] = probs[0]
            else:
                probsDict[action] = probs[1]
        combos3 = combinations(probsDict.keys(), 3)
        combos4 = combinations(probsDict.keys(), 4)
        combos5 = combinations(probsDict.keys(), 5)
        totalProb = 0
        for combo in combos3:
            tmpProbs = []
            for action, prob in probsDict.items():
                if action in combo : tmpProbs.append(prob)
                else : tmpProbs.append(1-prob)
            totalProb += prod(tmpProbs)
        for combo in combos4:
            tmpProbs = []
            for action, prob in probsDict.items():
                if action in combo : tmpProbs.append(prob)
                else : tmpProbs.append(1-prob)
            totalProb += prod(tmpProbs)
        for combo in combos5:
            tmpProbs = []
            for action, prob in probsDict.items():
                if action in combo : tmpProbs.append(prob)
                else : tmpProbs.append(1-prob)
            totalProb += prod(tmpProbs)
        return totalProb

    def terminate(self) :
        if self.handTables != None :
            for i in range(5):
                action = cardsDict._HANDS[i]
                self.handTables[action].terminate()
        self.handTables = None
            
               
class RandomAgent(SearchAgent) :
    
    def getAction(self, state):
        legalMove = state.getLegalActions(self.index)
        return random.choice(legalMove)
    
