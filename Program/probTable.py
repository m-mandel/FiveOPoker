from itertools import *
from numpy import *
from tables import *
from handEvaluator import evalHand
import cardsDict
import os
import time
from operator import mul

class ProbTable :
    def __init__(self, myHand, oppHand, unseen, tableName, dirName) :
        self.dirName = dirName
        self.myHand = set(myHand)
        self.oppHand = set(oppHand)

        self.myComplementSize = 5 - len(myHand)
        self.oppComplementSize = 5 - len(oppHand)
        self.unseen = unseen[:]
        self.removed = set()
        
        #get all possible combinations of hand's outcomes
        if self.myComplementSize == self.oppComplementSize :
            self.myComplements = self.oppComplements = list(combinations(unseen, self.myComplementSize) )
        else:
            self.myComplements = list(combinations(unseen, self.myComplementSize) )
            self.oppComplements = list(combinations(unseen, self.oppComplementSize) )

        self.myComplementsLen = len(self.myComplements)
        self.oppComplementsLen = len(self.oppComplements)
        start = time.clock()
        #create dictionaries of cardKey, indicesSet pairs
        #e.g. myIndicesDict[cardKey] returns all indices of myComplements that contain cardKey
        self.myIndicesDict = dict()
        self.oppIndicesDict = dict()
        for card in range(1,53):
            self.myIndicesDict[card] = set()
            self.oppIndicesDict[card]= set()
        if self.myComplementSize == self.oppComplementSize:
            for index in range(self.myComplementsLen ) :
                for card in self.myComplements[index]:
                    self.myIndicesDict[card].add(index)
                for card in self.oppComplements[index]:
                    self.oppIndicesDict[card].add(index)
                
        else:
            for index in range(self.myComplementsLen ) :
                for card in self.myComplements[index]:
                    self.myIndicesDict[card].add(index)
            for index in range(self.oppComplementsLen ) :
                for card in self.oppComplements[index]:
                    self.oppIndicesDict[card].add(index)
        
        self.intersectingIndices = dict()
        #build table
        table = zeros( (self.myComplementsLen, self.oppComplementsLen ) )
        for i in range(self.myComplementsLen ):
            self.intersectingIndices[i] = set()
            tmpMyHand = self.myHand.union(set(self.myComplements[i])  )
            for j in range(self.oppComplementsLen ):
                if set(self.myComplements[i]) & set(self.oppComplements[j]): 
                    self.intersectingIndices[i].add(j)
                    continue
                tmpOppHand = self.oppHand.union(set(self.oppComplements[j]) )
                table[i][j] = 1 if ((evalHand(list(tmpMyHand)) - evalHand(list(tmpOppHand) ) ) >= 0) else 0
        if (self.myComplementsLen * self.oppComplementsLen > 6000000 ) :
            self.completeTableName = tableName + '.hdf'
            self.completePathName = os.path.join(os.getcwd(), dirName, self.completeTableName)
            self.stored = open_file(self.completePathName, 'w')
            ds = self.stored.create_carray(self.stored.root, 'table', obj = table)
            self.stored.flush()
            print self.completeTableName + ' done.'
            self.table = None
        else:
            self.table = table
    
    def update(self, unseenCards, nextCard):
        self.unseen = unseenCards[:]
        self.removed = set(range(1,53)) - set(unseenCards) - set([nextCard])

    def getWaitProb(self, currMyHand, currOppHand, nextCard):
        myHandIndices = set()
        oppHandIndices = set()
        totIntersectingIdxs = 0

        for card in currMyHand :
            myHandIndices.update(self.myIndicesDict[card])
        if myHandIndices == set([]) :
            for card in self.unseen :
                myHandIndices.update(self.myIndicesDict[card])
        
        for card in currOppHand :
            oppHandIndices.update(self.oppIndicesDict[card])
        if oppHandIndices == set([]) :
            for card in self.unseen :
                oppHandIndices.update(self.oppIndicesDict[card])
        tmpOppIndices = set()
        tmpMyIndices = set()
        for card in self.unseen :
            tmpOppIndices.update(self.oppIndicesDict[card])
            tmpMyIndices.update(self.myIndicesDict[card])
        for card in currMyHand :
            tmpMyIndices.update(self.myIndicesDict[card])
        for card in currOppHand:
            tmpOppIndices.update(self.oppIndicesDict[card])
        for removed in self.removed :
            if removed not in currOppHand : 
                oppHandIndices.difference_update(self.oppIndicesDict[removed])
            if removed not in currMyHand : 
                myHandIndices.difference_update(self.myIndicesDict[removed])
        oppHandIndices.difference_update(self.oppIndicesDict[nextCard])
        oppHandIndices.intersection_update(tmpOppIndices)
        myHandIndices.intersection_update(tmpMyIndices)

        waitMyHandIndices = myHandIndices.copy()
        toRemove = set()
        for idx in waitMyHandIndices :
            if nextCard in self.myComplements[idx] :
                toRemove.add(idx)
        
        waitMyHandIndices.difference_update(toRemove)    
        
        for i in waitMyHandIndices:
            for j in oppHandIndices:
                if j in self.intersectingIndices[i] :
                    totIntersectingIdxs += 1
        
        ixgrid = ix_(list(waitMyHandIndices), list(oppHandIndices) )
        table = self.stored.root.table.read() if self.table == None else self.table
        
        subTable = table[ixgrid]
        height, width = subTable.shape
        bernoulliPositive = count_nonzero(subTable)
        waitProb = float(bernoulliPositive)/float(height*width - totIntersectingIdxs)
        
        return waitProb

    def getProb(self, currMyHand, currOppHand, nextCard):
        myHandIndices = set()
        oppHandIndices = set()
        totIntersectingIdxs = 0
        cardsAdded = set(currMyHand) - self.myHand

        for card in currMyHand :
            myHandIndices.update(self.myIndicesDict[card])
        if myHandIndices == set([]) :
            for card in self.unseen :
                myHandIndices.update(self.myIndicesDict[card])
        
        
        for card in currOppHand :
            oppHandIndices.update(self.oppIndicesDict[card])
        if oppHandIndices == set([]) :
            for card in self.unseen :
                oppHandIndices.update(self.oppIndicesDict[card])
        tmpOppIndices = set()
        tmpMyIndices = set()

        for card in self.unseen :
            tmpOppIndices.update(self.oppIndicesDict[card])

            tmpMyIndices.update(self.myIndicesDict[card])

        for card in currMyHand :
            tmpMyIndices.update(self.myIndicesDict[card])
        for card in currOppHand:
            tmpOppIndices.update(self.oppIndicesDict[card])

        for removed in self.removed :
            if removed not in currOppHand : 
                oppHandIndices.difference_update(self.oppIndicesDict[removed])
            if removed not in currMyHand : 
                myHandIndices.difference_update(self.myIndicesDict[removed])
        oppHandIndices.difference_update(self.oppIndicesDict[nextCard])
        oppHandIndices.intersection_update(tmpOppIndices)
        myHandIndices.intersection_update(tmpMyIndices)

        waitMyHandIndices = myHandIndices.copy()
        toRemove = set()
        for idx in waitMyHandIndices :
            if nextCard in self.myComplements[idx] :
                toRemove.add(idx)
        
        waitMyHandIndices.difference_update(toRemove)    
        
        for i in waitMyHandIndices:
            for j in oppHandIndices:
                if j in self.intersectingIndices[i] :
                    totIntersectingIdxs += 1
        
        ixgrid = ix_(list(waitMyHandIndices), list(oppHandIndices) )
        table = self.stored.root.table.read() if self.table == None else self.table

        subTable = table[ixgrid]

        height, width = subTable.shape
        bernoulliPositive = count_nonzero(subTable)
        waitProb = float(bernoulliPositive)/float(height*width - totIntersectingIdxs)
        postMyHandIndices = myHandIndices.copy()
        postMyHandIndices.update(self.myIndicesDict[nextCard])
        for removed in self.removed :
            if removed not in currMyHand : 
                postMyHandIndices.difference_update(self.myIndicesDict[removed])
       
        toRemove = set()
        for idx in postMyHandIndices :
            for card in cardsAdded :        
                if card not in self.myComplements[idx] :
                    toRemove.add(idx)
            if nextCard not in self.myComplements[idx] :
                toRemove.add(idx)
       
        postMyHandIndices.difference_update(toRemove)
            
        
        postTotIntersectingIdxs = 0
        for i in postMyHandIndices:
            for j in oppHandIndices:
                if j in self.intersectingIndices[i]:                 
                    postTotIntersectingIdxs += 1
        ixgrid2 = ix_(list(postMyHandIndices), list(oppHandIndices))
        subTable2 = table[ixgrid2]
        
        height2, width2 = subTable2.shape
        bernoulliPositive2 = count_nonzero(subTable2)
        putProb = float(bernoulliPositive2)/float(height2*width2 - postTotIntersectingIdxs)
        return putProb, waitProb

    def terminate(self):
        if self.table == None :
            if self.stored.isopen :
                self.stored.close()
            os.remove(self.completePathName)

                
                
            
