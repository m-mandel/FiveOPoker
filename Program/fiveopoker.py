from game import *
from display import Display
from keyboardAgent import KeyboardAgent
from agents import *
from handEvaluator import evalHand
from util import Counter
import sys, os, csv, random, time


class GameState :
    """
    Holds a game state.
    all of the internal data is kept in GameStateData instance
    """
    def __init__(self, prevState = None) :
        if prevState != None : 
            #start = time.time()
            self.data = GameStateData(prevState.data)
            #print time.time() - start
        else:
            self.data = GameStateData()
    
    def getLegalActions(self, agentIndex) :
        if self.isGameOver() : return []
        return AgentRules.getLegalActions(self.getAgentState(agentIndex) )

    def getAgentState(self, agentIndex) :
        return self.data.agentStates[agentIndex]

    def generateSuccessor(self, agentIndex, action) :
        nextState = GameState(self) 
        nextCard = nextState.data.popCard()
        nextState.data.nextCard = nextCard
        AgentRules.applyAction(nextState.getAgentState(agentIndex), action, nextCard)
        if nextState.data.totPlyNum < 30 : #remove unseen card from opponent
            nextState.getAgentState((agentIndex+1)%2).configuration.revealCard(nextCard)
        nextState.data.totPlyNum += 1
        nextState.getAgentState(agentIndex).plyNumber += 1
        return nextState
    
    def doAction(self,agentIndex, action):
        self.data.totPlyNum +=1
        self.getAgentState(agentIndex).plyNumber += 1
        nextCard = self.data.popCard()
        AgentRules.applyAction(self.getAgentState(agentIndex), action, nextCard)
        if self.data.totPlyNum < 30 : #remove unseen card from opponent
            if nextCard in self.getAgentState((agentIndex+1)%2).configuration.unseenCards:
                self.getAgentState((agentIndex+1)%2).configuration.revealCard(nextCard)
        return self
    
    def removeAction(self,agentIndex, action):
        # Take back the last card from the hand
        popedCard = self.data.agentStates[agentIndex].configuration.hands[action].pop()
        # Add the card to the deck
        self.data.deck.add(popedCard)
        # Update the players state
        self.data.totPlyNum -=1
        self.getAgentState(agentIndex).plyNumber -= 1
        # Update the unseen cards
        if self.data.totPlyNum < 30 : #remove unseen card from opponent
            self.getAgentState((agentIndex+1)%2).configuration.unRevealCard(popedCard)
            
        return self
    
    def getDeck(self) :
        return self.data.deck
    
    def setDeck(self, deck) :
        self.data.deck = deck
    
    def getHands(self, agentIndex) :
        return self.data.agentStates[agentIndex].configuration.hands
    
    def getOppHands(self, agentIndex) :
        oppHands = self.getHands((agentIndex+1)%2)
        hiddenHands = dict()
        for i in range(5):
            hand = cardsDict._HANDS[i]
            hiddenHands[hand] = oppHands[hand][:4]
        return hiddenHands

    def getAsHidden(self, agentIndex) :
        return self.data.getAsHidden(agentIndex)

    def winEval(self, agentIndex):
        op = (agentIndex + 1)%2
        diff = []
        for i in range(5) :
            key = cardsDict._HANDS[i]
            myVal = evalHand(self.getAgentState(agentIndex).configuration.hands[key])
            opponentVal = evalHand(self.getAgentState(op).configuration.hands[key])
            diff.append((myVal - opponentVal)/7463.0)
        return sum(exp(tanh(9*x)) for x in diff)
    
    def isGameOver(self) :
        return (self.data.totPlyNum >= 40)
    
    def countWins(self, agentIndex) :
        count = 0
        for i in range(5) :
            key = cardsDict._HANDS[i]
            myVal = evalHand(self.getAgentState(agentIndex).configuration.hands[key])
            opponentVal = evalHand(self.getAgentState((agentIndex + 1)%2).configuration.hands[key])
            if myVal - opponentVal > 0 :
                count += 1
        return count

    def isWinner(self, agentIndex):
        count = self.countWins(agentIndex)
        return count > 2

    def __eq__(self, other) :
        #TODO:
        return

    def __hash__(self) :
        #TODO:
        return 

    def __str__(self) :
        return str(self.data)

    def deepcopy(self) :
        state = GameState()
        state.data = self.data.deepcopy()
        return state

    def initialize(self, deck, agents) :
        self.data.initialize(deck, agents)

class GameRules :

    def __init__(self) :
        return

    def newGame(self, agentsA, agentsB, display = None, quiet = False) :
        """
        agentsA: agents for playerA
        agentB: agents for playerB
        """
        #self.agentsA = agentsA
        #self.agentsB = agentsB
        self.agents = [agentsA, agentsB]
        random.shuffle(self.agents)

        for i in range(2) :
            self.agents[i][0].index = i
            self.agents[i][1].index = i
            self.agents[i][0].reset()
            self.agents[i][1].reset()
                    
        deck = list(range(1,53))
        random.shuffle(deck )
        game = Game(self.agents[0], self.agents[1], self)
        initState = GameState()
        initState.initialize(deck, [self.agents[0][0], self.agents[1][0] ])
        #add state to game instance
        game.state = initState
        return game

    def decideWinner(self, state):
        
        if state.isWinner(0) :
            winnerIndex = 0
        elif state.isWinner(1) :
            winnerIndex = 1
        else:
            print 'Tie!'
            winnerIndex = -1
 
        return winnerIndex, state.countWins(winnerIndex)

class AgentRules :

    def getLegalActions(agentState) :
        return Actions.getPossibleActions(agentState.configuration, agentState.plyNumber)

    getLegalActions = staticmethod(getLegalActions)

    def applyAction(agentState, action, nextCard) :
        
        legal = AgentRules.getLegalActions(agentState)
        #print legal
        if action not in legal:
            raise Exception("Illegal action " + str(action) + ' ' + str(legal) )

        agentState.configuration = agentState.configuration.generateSuccessor(action, nextCard)
        if nextCard in agentState.configuration.unseenCards:
            agentState.configuration.revealCard(nextCard)

    applyAction = staticmethod(applyAction)

def readCommand(argv) :
    from optparse import OptionParser
    import os
    usageStr = """
    USAGE: python fiveopoker.py <options>
    EXAMPLES: 
    (1) python fiveopoker.py -1 Moshe human -2 Shai human
    (2) python fiveopoker.py -1 Moshe hminimax -2 Shai human -g y
    (3) python fiveopoker.py -1 Moshe greedy prob -a greedyEval1 Shai greedy prob -b greedyEval2
    """
    parser = OptionParser(usageStr)
    parser.add_option("-1", "--playerA", dest = "playerA", help = "<PlayerA name> <AgentType>", nargs = 2, default = ['playerA', 'human'])
    parser.add_option("-a", "--function1", dest = "function1", help = "<evaluation function>", default = 'greedyEval2')
    parser.add_option("-2", "--playerB", dest = "playerB", help = "<PlayerB name> <AgentType>", nargs = 2, default = ['playerB', 'greedy'])
    parser.add_option("-b", "--function2", dest = "function2", help = "<evaluation function>", default = 'greedyEval2')
    parser.add_option("-n", "--numGames", dest = "numGames", help = "<int>", type = "int", default = 1)
    parser.add_option("-g", "--graphics", dest = "graphics", help = "y/n", default = 'y')
    parser.add_option("-v", "--verbose", dest = "verbose", help = "y/n", default = 'y')
    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
    args = dict()
    dirName = time.ctime()
    dirName = dirName.replace(':', ' ')
    dirName = os.path.join('games records', dirName)
    os.mkdir( os.path.join(os.getcwd() , dirName) )
    args['dirName'] = dirName
    agent1I, agent1II = parseAgentType(options.playerA, dirName, options.function1)
    agent2I, agent2II = parseAgentType(options.playerB, dirName, options.function2)
    args['agentsA'] = [agent1I, agent1II]
    args['agentsB'] = [agent2I, agent2II]
    args['numGames'] = options.numGames
    args['verbose'] = (options.verbose == 'y')
    if options.graphics == 'y' :
        args['display'] = Display()
    return args

def parseAgentType(playerList, dirName, function) :
    if playerList[1] == 'human' :
        agentA = KeyboardAgent(playerList[0])
        agentB = KeyboardAgent(playerList[0])
        return agentA, agentB
    if playerList[1] == 'random' :
        agentA = RandomAgent(playerList[0],function)
    if playerList[1] == 'minimax' :
        agentA = MinimaxAgent(playerList[0])
    #if playerList[1] == 'hminimax' :
    #    agentA = HMinimaxAgent(playerList[0],function)
    if playerList[1] == 'approxMinimax' :
        agentA = ApproxMinimaxAgent(playerList[0])
    if playerList[1] == 'hminimax' :
        agentA = ApproxHMinimaxAgent(playerList[0], function)
    if playerList[1] == 'greedy' :
        agentA = GreedyAgent(playerList[0], function)
    if playerList[1] == 'reflex1' :
        agentA = ReflexAgent1(playerList[0])
    if playerList[1] == 'reflex2' :
        agentA = ReflexAgent2(playerList[0])
    if playerList[1] == 'reflex3' :
        agentA = ReflexAgent3(playerList[0])
    if playerList[1] == 'reflex4' :
        agentA = ReflexAgent4(playerList[0])
    if playerList[1] == 'monte' :
        agentA = MonteCarloAgent(playerList[0], dirName)
    if playerList[1] == 'prob' :
        agentA = ProbAgent(playerList[0], dirName)
    agentB = ProbAgent(playerList[0], dirName)
    return agentA, agentB


def runGames(agentsA, agentsB,  dirName, display = None, numGames = 2, record = True, verbose = True):
    rules = GameRules()
    totalCount = Counter()
    rows = []
    sortedRows = []
    print 'Running games...'
    for i in range (numGames) :
        
        game = rules.newGame(agentsA, agentsB)
        if record :
            completeName = os.path.join(os.getcwd(), dirName, str(i) + '.txt')
            log = open(completeName, 'w')
        else :
            log = None
        if display == None:        
            winner = game.run(dirName, log, verbose)
        else:
            winner = display.run(game, dirName, log, verbose)
        for k in range(2) :
            agentsA[k].terminate()
            agentsB[k].terminate()
        totalCount[winner] += 1
        if record:
            gameDict = dict()
            gameDict[agentsA[0].name] = [0]
            gameDict[agentsB[0].name] = [0]
            gameDict[winner][0] = 1
            row = dict()
            sortedRow = dict()
            for name, scores in game.getScore().items():
                gameDict[name].append([score[1] for score in scores])
            sortedA = sorted(gameDict[agentsA[0].name][1], reverse = True)
            sortedB = sorted(gameDict[agentsB[0].name][1], reverse = True)
            for j in  range(5) :
                keyA  = 'score A' + str(j+1)
                keyB = 'score B' + str(j+1)
                row[keyA] = gameDict[agentsA[0].name][1][j]
                row[keyB] = gameDict[agentsB[0].name][1][j]
                sortedRow[keyA] = sortedA[j]
                sortedRow[keyB] = sortedB[j]
            row['Game No.'] = i + 1
            row['agent A'] = gameDict[agentsA[0].name][0]
            row['agent B'] = gameDict[agentsB[0].name][0]
            sortedRow['Game No.'] = i + 1
            sortedRow[agentsA[0].name] = gameDict[agentsA[0].name][0]
            sortedRow[agentsB[0].name] = gameDict[agentsB[0].name][0]
            rows.append(row)
            sortedRows.append(sortedRow)
    total = agentsA[0].name + '\t' + str(agentsA[0].__class__.__name__ ) + '\t' + str(agentsA[1].__class__.__name__ ) +  '\t' + str(totalCount[agentsA[0].name]) +'\n' \
                        + agentsB[0].name + '\t' + str(agentsB[0].__class__.__name__) + '\t' + str(agentsB [1].__class__.__name__ ) + '\t' + str(totalCount[agentsB[0].name]) + '\nTotal:\t' + str(numGames)
    if record:
        tablePath = os.path.join(os.getcwd(), dirName, 'table.csv')
        table = open(tablePath, 'w')
        fieldNames = ('Game No.', 'agent A', 'agent B', 'score A1', 'score B1', 'score A2', 'score B2', 'score A3', 'score B3', 'score A4', 'score B4', 'score A5', 'score B5')
        dw =  csv.DictWriter(table, fieldNames)
        dw.writeheader()
        dw.writerows(rows)
        tablePath = os.path.join(os.getcwd(), dirName, 'table2.csv')
        table2 = open(tablePath, 'w')
        fieldNames2 = ('Game No.', agentsA[0].name, agentsB[0].name, 'score A1', 'score A2',  'score A3', 'score A4', 'score A5', 'score B1', 'score B2', 'score B3', 'score B4', 'score B5')
        dw =  csv.DictWriter(table2, fieldNames2)
        dw.writeheader()
        dw.writerows(sortedRows)
        summary = open(os.path.join(os.getcwd(), dirName, 'summary.txt'), 'w')
        summary.write(total)
        summary.write('\n' + '*'*40 + '\n')
    print 'Summary:'
    print total
    

if __name__ == '__main__':
    args = readCommand( sys.argv[1:] ) # Get game components based on input
    runGames(**args)

    pass
