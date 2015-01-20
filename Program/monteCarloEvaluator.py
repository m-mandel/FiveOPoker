from numpy import *
import random
from util import *
from itertools import *
from handEvaluator import evalHand
import cardsDict

def evalHandPair(handA, handB, unseenCards, size):
    complementSizeA = 5 - len(handA)
    complementSizeB = 5 - len(handB)
    sample = list(unseenCards)
    sampleSize = len(sample)
    wins = 0
    count = 0
    maxA = special.binom(sampleSize, complementSizeA)
    maxB = special.binom(sampleSize -complementSizeA, complementSizeB)
    maxSampleSize = mul(maxA, maxB)
    if maxSampleSize <= size and maxSampleSize > 0:
        for combA in combinations(sample, complementSizeA ) :
            
            tmpHandA = handA[:]
            tmpHandA.extend(combA)
            tmpSample = unseenCards - set(combA)
            for combB in combinations(tmpSample, complementSizeB) :
                count+=1
                tmpHandB = handB[:]
                tmpHandB.extend(combB)
                
                diff = evalHand(tmpHandA) - evalHand(tmpHandB)
                win = diff >=0 and 1 or 0
                wins += win

        return float(wins)/float(maxSampleSize)
    else:
        while count < size:
            count += 1
            complementA = set(random.sample(unseenCards, complementSizeA) )
            tmpUnseenCards = unseenCards - complementA
            complementB = random.sample(tmpUnseenCards, complementSizeB)
            tmpHandA = handA[:]
            tmpHandA.extend(complementA)
            tmpHandB = handB[:]
            tmpHandB.extend(complementB)
            diff = evalHand(tmpHandA) - evalHand(tmpHandB)
            win = diff >=0 and 1 or 0
            wins += win

        return float(wins)/float(count)

class MonteCarloEvaluator:
    def __init__(self, state, agentIndex, size = 1000):
        self.size = size
        self.state = state.deepcopy()
        self.agentIndex = agentIndex
        self.nextCard = state.getDeck().pop()
        self.state.getAgentState(self.agentIndex).configuration.revealCard(self.nextCard)
        self.unseenCards = set(self.state.getAgentState(agentIndex).getUnseenCards() )
        
        self.handsA = state.getHands(agentIndex)
        self.handsB = state.getOppHands(agentIndex)
        self.preActionProbs = dict()
        for i in range(5):
            handName = cardsDict._HANDS[i]
            self.preActionProbs[handName] = evalHandPair(self.handsA[handName], self.handsB[handName], self.unseenCards, self.size)

    def eval(self, action):
        tmpHandA = self.handsA[action][:]
        tmpHandA.append(self.nextCard)
        postActionProb = evalHandPair(tmpHandA, self.handsB[action], self.unseenCards, self.size)
        postActionProbs = deepish_copy(self.preActionProbs)
        postActionProbs[action] = postActionProb
       
        winProb = self.getWinProb(postActionProbs)
        return winProb

    def getWinProb(self, actionProbsDict):
        """
        probs : a list of 4 wait probabilities and 1 put probalbility
        """

        combos3 = combinations(actionProbsDict.keys(), 3)
        combos4 = combinations(actionProbsDict.keys(), 4)
        combos5 = combinations(actionProbsDict.keys(), 5)
        totalProb = 0
        for combo in combos3:
            tmpProbs = []
            for action, prob in actionProbsDict.items():
                if action in combo : tmpProbs.append(prob)
                else : tmpProbs.append(1-prob)
            totalProb += prod(tmpProbs)
        for combo in combos4:
            tmpProbs = []
            for action, prob in actionProbsDict.items():
                if action in combo : tmpProbs.append(prob)
                else : tmpProbs.append(1-prob)
            totalProb += prod(tmpProbs)
        for combo in combos5:
            tmpProbs = []
            for action, prob in actionProbsDict.items():
                if action in combo : tmpProbs.append(prob)
                else : tmpProbs.append(1-prob)
            totalProb += prod(tmpProbs)
        return totalProb

        
        