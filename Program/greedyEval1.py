'''
Created on 02/02/2014
@author: Shai Aharon

This is the file that executes the first Stage.
'''
from time import clock
import cardsDict
from game import Card
from operator import sub as sub
from math import exp, tanh

# Hands value
ROYAL_SCORE = 4  
RANK_SCORE = 8  
SUIT_SCORE = 2  
RANGE_SCORE = 2  
HIGH_CARD = 1

SUM_SCORE = sum([ROYAL_SCORE,
                RANK_SCORE,
                SUIT_SCORE,  
                RANGE_SCORE])
MIN_SCORE = 1.839 * 5
MAX_SOCRE = 13.591
DIFF_SCORE = 11.0


global getRank
global getSuit
getRank = lambda x: cardsDict.RANK[cardsDict.INVERTED_INTVAL[ x ] ]
getSuit = lambda x: cardsDict.SUIT[cardsDict.INVERTED_INTVAL[ x ] ]

def greedyEval1(agentIndex,state):
    #start = clock()
    packsCOMP = state.getHands(agentIndex).values()
    packsOP = state.getHands((agentIndex+1)%2).values()

    diff = []
    for packA,packB in zip(packsCOMP,packsOP):
        diff.append((getPackExpect(packA, state) - getPackExpect(packB, state))
                    /SUM_SCORE )
    
    retVal = sum(exp(tanh(9*x)) for x in diff)
    
    #print clock() - start
#     print "diff:",diff
#     print "retVal:",retVal
    return retVal

def getPackExpect(pack,state):
    retSum = 0

    # Same suit
    retSum += sameSuit(pack) * SUIT_SCORE
    
    # Same rank
    hasDub = sameRank(pack) * RANK_SCORE
    retSum += hasDub 
    
    # Rank range & High Card
    retSum += inRangeAndHighCard(pack,hasDub)
    
    if len(pack) < 5: return retSum
    # Royal Flush
    retSum += getRoyalProb(pack,state) * ROYAL_SCORE
       
    return retSum

def inRangeAndHighCard(pack,hasDub):
    packLen = len(pack)
    highCard = -1
    minCard = 999
    if hasDub: return max([getRank(x) for x in pack])/12.0
    for x in pack:
        tmpNum = getRank(x)
        highCard = max(highCard,tmpNum)
        minCard = min(minCard,tmpNum)
    if highCard - minCard > 4 : return highCard/12.0
    
    return RANGE_SCORE * packLen/5.0 + highCard/12.0

def sameSuit(pack):
    pSuit = getSuit(pack[0])
    for tmpCard in pack[1:]:
        if not getSuit(tmpCard) == pSuit:
            return 0
    return len(pack)/5.0

def sameRank(pack):
    sLst = set(pack)
    orderdRanks = [pack.count(x) for x in sLst] 
    orderdRanks.append(1)
    orderdRanks.sort(cmp=None, key=None, reverse=True)
    sumNum = orderdRanks[0] * orderdRanks[1]**2
    if not sumNum%12: return 3.0 # 3 & 2
    if not sumNum%8: return 2.0  # 2 & 2 
    if not sumNum%4: return 1.0
    if not sumNum%3: return 0.75
    if not sumNum%2: return 0.5
    return 0
    
def getRoyalProb(pack,state):
    # Check if the pack has a card that dosen't belong to royalFlush
    pSuit = getSuit(pack[0])
    for tmpCard in pack:
        if not getSuit(tmpCard) == pSuit:
            return 0
    
    oPack = [getRank(c) for c in pack]
    oPack.sort(cmp=None, key=None, reverse=False)
    smallNum = oPack[0]
    bigestNum = oPack[4]
    if bigestNum is not 12: return 0
    if smallNum is not  8: return 0
    
    return 1.0
