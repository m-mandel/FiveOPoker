from valueDict import ValueDict
from handEvaluator import evalHand
from decimal import *
import cardsDict
from math import exp, tanh, log10, log, pow, sqrt, fabs, copysign
from util import hypGeoProb, multiHypGeoProb
from operator import mul
from numpy import  zeros, count_nonzero, prod
from scipy import special
from collections import Counter
import time

_ACE_FLUSH = 7463 - (815+323)/2
_KING_FLUSH = 7463 - (1144+816)/2
_QUEEN_FLUSH = 7463 - (1353+1145)/2
_JACK_FLUSH = 7463 - (1477+1354)/2
_10_FLUSH = 7463 - (1546+1478)/2
_9_FLUSH = 7463 - (1581+1547)/2
_8_FLUSH = 7463 - (1595+1582)/2
_7_FLUSH = 7463 - (1599+1596)/2
_FLUSH_VALUES = {0 : _7_FLUSH,
                 1 : _7_FLUSH,
                 2 : _7_FLUSH,
                 3 : _7_FLUSH,
                 4 : _7_FLUSH,
                 5 : _7_FLUSH,
                 6 : _8_FLUSH, 7 : _9_FLUSH, 8 : _10_FLUSH, 9 : _JACK_FLUSH, 10 : _QUEEN_FLUSH, 11 : _KING_FLUSH, 12 : _ACE_FLUSH}
_ACE_STRAIGHT = 7463 - 1600
_KING_STRAIGHT = 7463 - 1601
_QUEEN_STRAIGHT = 7463 - 1602
_JACK_STRAIGHT = 7463 - 1603
_10_STRAIGHT = 7463 - 1604
_9_STRAIGHT = 7463 - 1605
_8_STRAIGHT = 7463 - 1606
_7_STRAIGHT = 7463 - 1607
_6_STRAIGHT = 7463 - 1608
_5_STRAIGHT = 7463 - 1609
_STRAIGHT_VALUES = { 0 : _5_STRAIGHT,
                     1 : _5_STRAIGHT,
                     2 : _5_STRAIGHT,
                     3 : _5_STRAIGHT,
                     4 : _6_STRAIGHT,
                     5 : _7_STRAIGHT,
                     6 : _8_STRAIGHT, 7 : _9_STRAIGHT, 8 : _10_STRAIGHT, 9 : _JACK_STRAIGHT, 10 : _QUEEN_STRAIGHT, 11 : _KING_STRAIGHT, 12 : _ACE_STRAIGHT}
valDict = ValueDict()

def greedyEval2(agentIndex, state):
    agentHands = state.getHands(agentIndex)
    opponentHands = state.getHands((agentIndex+1)%2)
    
    
    diff = []
    
    for i in range(5):
        hand = cardsDict._HANDS[i]
        myHand = eval(agentHands[hand], agentIndex, state)
        oppHand = eval(opponentHands[hand], (agentIndex + 1)%2, state)
        diff.append(log(float(myHand)/float(oppHand)) )
    retVal = sum(x for x in diff)
    return retVal

def greedyEval3(agentIndex, state):
    agentHands = state.getHands(agentIndex)
    opponentHands = state.getHands((agentIndex+1)%2)
    
    
    diff = []
    
    for i in range(5):
        hand = cardsDict._HANDS[i]
        myHand = eval(agentHands[hand], agentIndex, state)
        oppHand = eval(opponentHands[hand], (agentIndex + 1)%2, state)
        diff.append(log(float(myHand)/float(oppHand)) )
    retVal = sum(x for x in diff)
    return retVal

def fastGreedyEval2(agentIndex, state):
    agentHands = state.getHands(agentIndex)
    opponentHands = state.getHands((agentIndex+1)%2)
    
    unseenCards = state.getAgentState(agentIndex).getUnseenCards().asList()
    unseenArr = zeros(52, dtype = 'int')
    for i in unseenCards:
        unseenArr[i-1] = 1
    unseenArr.shape = (13,4)
    unseenSize = len(unseenCards)
    diff = []
    
    for i in range(5):
        hand = cardsDict._HANDS[i]        
        myHand = fastEval(agentHands[hand], agentIndex, state, unseenArr, unseenSize)
        oppHand = fastEval(opponentHands[hand], (agentIndex + 1)%2, state, unseenArr, unseenSize)
        diff.append(log(float(myHand)/float(oppHand) ) )
    retVal = sum(x for x in diff)
    return retVal

def fastEval(hand, agentIndex, state, unseenArr = None, unseenSize = None):
    global valDict
    size = len(hand)
    if size == 5 :
        return evalHand(hand)
    ranks = tuple(cardsDict.RANK[cardsDict.INVERTED_INTVAL[card] ] for card in hand)
    suits = set(cardsDict.SUIT[cardsDict.INVERTED_INTVAL[card] ] for card in hand )
    suitSize = len(suits)
    minVal = min(ranks)
    maxRank = maxVal = max(ranks)
    if maxVal == 12 and minVal < 4:
        tmpRanks = sorted(ranks)
        maxVal = max(tmpRanks[:-1])
        minVal = -1 
    if suitSize == 1:
        suit = suits.pop()
        suitsLeft = count_nonzero(unseenArr[:, suit])
        flushProb = float(suitsLeft)/float(unseenSize)
    else :
        flushProb = 0
    if maxVal - minVal < 5 :
        straightProb = getFastStraightProb(ranks, unseenArr, unseenSize, minVal, maxVal)
    else:
        straightProb = 0
    return ((1-flushProb - straightProb)*valDict.dicts[size-1][ranks] + (flushProb * _FLUSH_VALUES[maxRank] + straightProb * _STRAIGHT_VALUES[maxRank])*size/5.0) 
    
  

def eval(hand, agentIndex, state) :
    global valDict
    size = len(hand)
    if size == 5 :
        return evalHand(hand)
    ranks = tuple(cardsDict.RANK[cardsDict.INVERTED_INTVAL[card] ] for card in hand )
    suits = set(cardsDict.SUIT[cardsDict.INVERTED_INTVAL[card] ] for card in hand )
    suitSize = len(suits)
    minVal = min(ranks)
    maxRank = maxVal = max(ranks)
    if maxVal == 12 and minVal < 4:
        tmpRanks = sorted(ranks)
        maxVal = max(tmpRanks[:-1])
        minVal = -1 
    flushProb = 0
    straightProb = 0
    
    if suitSize == 1 or maxVal - minVal < 5 :
        ranksSet = []
        unseenCards = state.getAgentState(agentIndex).getUnseenCards().asList()
        unseenArr = zeros(52, dtype = 'int')
        for i in unseenCards:
            unseenArr[i-1] = 1
        unseenArr.shape = (13,4)
        
        flushProb = getFlushProb(list(suits)[0], unseenArr, state, len(unseenCards), size) if suitSize == 1 else 0

        for rank in ranks:
            if rank not in ranksSet:
                ranksSet.append(rank)
        
        straightProb = getStraightProb(ranks, unseenArr, state, len(unseenCards), size, minVal, maxVal) if (maxVal - minVal < 5 and len(ranksSet) == size) else 0
    return ((1-flushProb - straightProb)*valDict.dicts[size-1][ranks] + (flushProb * _FLUSH_VALUES[maxRank] + straightProb * _STRAIGHT_VALUES[maxRank])*size/5.0)


def getFlushProb(suit, unseenArr, state, unseenSize, handSize) :
    """
    unseenCards - a 13X4 numpy matrix
    """
    #N - population, K - successful cards, t - total moves in game until next time this hand is available
    # s - number of draws that will be available for this hand ,k - successful draws needed
    #start = time.clock()
    N = unseenSize
    K = count_nonzero(unseenArr[:, suit])
    t = -state.data.totPlyNum%10
    n = (40 - (state.data.totPlyNum + t))/2
    k = 5 - handSize
    return hypGeoProb(N,K,n,k)

def getStraightProb(ranks, unseenArr, state, unseenSize, handSize, minRank, maxRank) :
    """
    ranks - tuple of ranks in hand
    unseenCards - a 13X4 numpy matrix
    """
    #N - population, t - total moves in game until next time this hand is available
    # s - number of draws that will be available for this hand
    # l - number of cards needed to complete hand ( 0<=l<=4 )
    N = unseenSize
    t = -state.data.totPlyNum%10
    s = (40 - (state.data.totPlyNum + t))/2
    l = 5 - handSize

    leftCardsLists = []    
    for lowRank in range(max(-1, maxRank - 4) , minRank + 1):
        highRank = min(12, lowRank + 4)
        if highRank < maxRank or lowRank > highRank - 4 : continue
        tmpLeftCardsList = []
        for rank in range(lowRank, highRank + 1 ):
            tmpRank = rank if rank != -1 else 12
            if tmpRank not in ranks:
                tmpLeftCardsList.append(count_nonzero(unseenArr[rank, :]) )
        leftCardsLists.append(tmpLeftCardsList)

    tmpSum = 0.0
    for leftCardsList in leftCardsLists :
        tmpSum += multiHypGeoProb(N, leftCardsList, s, l) 
    return tmpSum

def getFastStraightProb(ranks, unseenArr, unseenSize, minRank, maxRank) :
    tmpSum = 0.0  
    for lowRank in range(max(-1, maxRank - 4) , minRank + 1):
        highRank = min(12, lowRank + 4)
        if highRank < maxRank or lowRank > highRank - 4 : continue
        tmpLeftCardsList = []
        for rank in range(lowRank, highRank + 1 ):
            tmpRank = rank if rank != -1 else 12
            if tmpRank not in ranks:
                tmpLeftCardsList.append(count_nonzero(unseenArr[rank, :])/float(unseenSize) )
        tmpSum += reduce(mul, tmpLeftCardsList)
    return tmpSum

