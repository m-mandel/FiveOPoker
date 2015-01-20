from collections import Counter
from itertools import combinations_with_replacement, permutations
from handEvaluator import evalHand
from numpy import *

def addMinKicker(ranks) :
    minVal = min(ranks)
    maxVal = max(ranks)
    for rank in range(13) :
        if rank not in ranks :
            if Counter(ranks).most_common(1)[0][1] != 1 or maxVal - minVal > 4 \
                or (maxVal - minVal == 4 and (rank < minVal or rank > maxVal) ) \
                or (maxVal - minVal == 3 and (rank < minVal -1 or rank > maxVal + 1) ):
                    return list(ranks + (rank,) )
 
def isSubset(tuple1, tuple2) :
    tmp = list(tuple2)
    for item in tuple1 :
        if item not in tmp : return False
        tmp.remove(item)
    return True          

class ValueDict:
    
    def __init__(self):
        self.dict4 = {}
        self.dict3 = {}
        self.dict2 = {}
        self.dict1 = {}
        self._fill4Dict()
        self._fill3Dict()
        self._fill2Dict()
        self._fill1Dict()
        self.dicts = [self.dict1, self.dict2, self.dict3, self.dict4]


    def _fill4Dict(self) :
        cards = array(range(1,53) )
        cards.shape = (13,4)
        for combo in combinations_with_replacement(range(13), 4) :
            min5Combo = addMinKicker(combo)
            tmpHand = []
            for i in range(4) :
                tmpHand.append(cards[min5Combo[i] ][0])
            tmpHand.append(cards[min5Combo[4] ][1])
            self.dict4[combo] = evalHand(tmpHand)
            for p in permutations(combo) :
                self.dict4[p] = self.dict4[combo]

    def _fill3Dict(self) :
        for combo in combinations_with_replacement(range(13), 3) :
            superSets = [(set, self.dict4[set]) for set in combinations_with_replacement(range(13), 4) if isSubset(combo, set) ]
            minVal = min(superSets, key = lambda x : x[1])[1]
            #maxVal = max(superSets, key = lambda x : x[1])[1]
            self.dict3[combo] = minVal
            for p in permutations(combo) :
                self.dict3[p] = self.dict3[combo]
    
    def _fill2Dict(self) :
        for combo in combinations_with_replacement(range(13), 2) :
            superSets = [(set, self.dict3[set]) for set in combinations_with_replacement(range(13), 3) if isSubset(combo, set) ]
            minVal = min(superSets, key = lambda x : x[1])[1]
            #maxVal = max(superSets, key = lambda x : x[1])[1]
            self.dict2[combo] = minVal
            for p in permutations(combo) :
                self.dict2[p] = self.dict2[combo]

    def _fill1Dict(self) :
        for combo in range(13) :
            superSets = [(set, self.dict2[set]) for set in combinations_with_replacement(range(13), 2) if isSubset((combo,), set) ]
            minVal = min(superSets, key = lambda x : x[1])[1]
            #maxVal = max(superSets, key = lambda x : x[1])[1]
            self.dict1[(combo,)] = minVal


