import math
import random
import copy
import time
import util
from handEvaluator import evalHand
import cardsDict

class Agent:

    def __init__(self, name):
        self.name = name
        self.index = None

    def getAction(self, state):
        pass

    def reset(self):
        return

    def terminate(self):
        return

class Card:
    
    def __init__(self, intVal):
        self.intVal = intVal
        self.name = str(cardsDict.INVERTED_INTVAL[intVal] )
        self.rank = cardsDict.RANK[self.name]
        self.suit = cardsDict.SUIT[self.name]

    def __eq__(self, other) :
        return hash(self) == hash(other)

    def __str__(self) :
        return self.name

    def __int__(self) :
        return self.intVal

    def __hash__(self) : 
        return hash(self.intVal)

    def copy(self) :
        return Card(self.intVal)
          
class Hand :
    """
        a hand of up to 5 cards.
    """
    def __init__(self, cards):
        self.cards = cards[:]
        self.val = None
    
    def add(self, card) :
        self.cards.append(card)
        
    def __len__(self):
        return len(self.cards)

    def __getitem__(self, key) :
        """
        returns the card at index <key>.
        according to the order added to hand.
        """
        return self.cards[key]

    def __eq__(self, other) :
        if other == None or self.size != other.size : return False
        for i in range(self.size) :
            if self.cards[i] != other.cards[i] : return False
        return True

    def __str__(self) :
        handStr = ', '.join(str(card) for card in self.cards )
        return handStr

    def __hash__(self):
        """
            for hands to be hashable -> available in dict's (is this neccessary?)
        """
        #TODO: hash poker hand the same as HT lookup value.
        return hash
    
    def getVal(self):
        if self.val == None:
            assert len(self) == 2, "Can't evaluate incomplete hand, current hand size: %d. \ncards: %s" %(len(self), str(self) )
            self.val = getHandRank(self.cards)
        return self.val

class Deck:

    def __init__(self, cards = None):
        if cards != None:
            self.cards = cards[:]
    
    def __str__(self):
        self.grid = [[False for i in range(4)] for j in range(13)]
        for card in self.cards:
            cardVal = cardsDict.INVERTED_INTVAL[card]
            self.grid[cardsDict.RANK[cardVal]][cardsDict.SUIT[cardVal]] = True
            
        f = lambda x : x == True and '*' or ' '
        rankStr = ''.ljust(9, ' ') + '|'.join(str(i).center(3, ' ') for i in range(2,11) + ['J','Q','K','A'])
        diamondsStr = 'Diamonds'.ljust(8, ' ') + ':'+ '|'.join(f(x).center(3, ' ') for x in [self.grid[x][cardsDict._S_DIAMONDS] for x in range(13)])
        heartsStr = 'Hearts'.ljust(8, ' ') + ':'+ '|'.join(f(x).center(3, ' ') for x in [self.grid[x][cardsDict._S_HEART] for x in range(13)]) 
        spadesStr = 'Spades'.ljust(8, ' ') + ':'+ '|'.join(f(x).center(3, ' ') for x in [self.grid[x][cardsDict._S_SPADE] for x in range(13)])
        clubsStr = 'Clubs'.ljust(8, ' ') + ':'+ '|'.join(f(x).center(3, ' ') for x in [self.grid[x][cardsDict._S_CLUBS] for x in range(13)])
        return '\n'.join([rankStr, clubsStr, diamondsStr, heartsStr, spadesStr])


    def __hash__(self):
        cardList = [card for card in self.cards]
        return hash(tuple(cardList))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.cards == other.cards
        else:
            return False

    def __getitem__(self, key) :
        """
        Access operator.
        e.g. deck[0] returns first card
        """
        return self.cards[key]
    
    def __setitem__(self, key, value) :
        self.cards[key] = value

    def __len__(self) :
        return len(self.cards)
    
    def __contains__(self, key) :
        return key in self.cards
    
    def insert(self, index, value) :
        self.cards.insert(index, value)

    def asList(self) :
        return self.cards

    def copy(self) :
        newDeck = Deck()
        newDeck.cards = self.cards
        return newDeck

    def deepcopy(self) :
        cards = copy.deepcopy(self.cards)
        return Deck(cards)
        
    def add(self, card) :
        """
        inserts card to begining of deck
        """
        self.cards.insert(0, card)

    def remove(self, card) :
        """
        remove specific card from deck
        """
        try:
            self.cards.remove(card)
        except:
            print 'card', cardsDict.INVERTED_INTVAL[card], card
            print 'cards:', [x for x in self.cards]
            raise

    def pop(self) :
        """
        removes and returns first card in deck
        """
        return self.cards.pop(0)
    
    def shuffle(self) :
        random.shuffle(self.cards)

class Configuration:
    """
    Contatins Configuration of an agent in a game.
    includes refernce to deck, instance of agent's unseen cards, his 5 hands, and a reference to next card in deck
    """

    def __init__(self, unseenCards, deck, hands  = None) :
        """
        unseenCards is a list of integers
        deck is a Deck instance
        """
        self.hands = hands
        self.unseenCards = Deck(unseenCards)
        self.deck = deck
        self.nextCard = self.deck[0]
              
    def __eq__(self, other) :
        return self.hands == other.hands 

    def __str__(self) :
        f = lambda x : cardsDict._HANDS[x]
        grid = [[' '.center(14,' ') for i in range(5)] for j in range(5)]
        for i in range(5):
            for j in range(len(self.hands[f(i)])):
                grid[j][i] = str(cardsDict.INVERTED_INTVAL[self.hands[f(i)][j]].center(14,' ') )
        
        line1 = '|'.join(grid[0][x] for x in range(5) )
        line2 = '|'.join(grid[1][x] for x in range(5) )
        line3 = '|'.join(grid[2][x] for x in range(5) )
        line4 = '|'.join(grid[3][x] for x in range(5) )
        line5 = '|'.join(grid[4][x] for x in range(5) )
        handsStr = '\n'.join([line1, line2, line3, line4, line5])
        unseenStr =  'unseen Cards:\n' +  str(self.unseenCards)
        configStr = unseenStr + '\nHands:\n' + handsStr
        return configStr
    
    def getHiddenStateStr(self) :
        f = lambda x : cardsDict._HANDS[x]
        grid = [[' '.center(14,' ') for i in range(5)] for j in range(5)]
        for i in range(5):
            for j in range(len(self.hands[f(i)])):
                if j == 4:
                    grid[j][i] = '*'.center(14, ' ') if (len(self.hands[f(i)]) == 5) else ' '.center(14, ' ')
                else:
                    grid[j][i] = str(cardsDict.INVERTED_INTVAL[self.hands[f(i)][j]].center(14,' ') )
        
        line1 = '|'.join(grid[0][x] for x in range(5) )
        line2 = '|'.join(grid[1][x] for x in range(5) )
        line3 = '|'.join(grid[2][x] for x in range(5) )
        line4 = '|'.join(grid[3][x] for x in range(5) )
        line5 = '|'.join(grid[4][x] for x in range(5) )
        handsStr = '\n'.join([line1, line2, line3, line4, line5])
        configStr = '\nHands:\n' + handsStr
        return configStr

    def __hash__(self) :
        #TODO:
        return
    
    def deepcopy(self) :
        newConfig = Configuration(self.unseenCards[:], self.deck )
        newConfig.hands = util.deepish_copy(self.hands)
        return newConfig

    def peek(self) :
        return int(self.nextCard)

    def removeCard(self, nextCard) :
        """
        Shouldn't really by used.
        """
        self.deck.remove(nextCard)

    def revealCard(self, nextCard) :
        self.unseenCards.remove(nextCard)
    
    def unRevealCard(self, preCard) :
        self.unseenCards.add(preCard)
          
    def generateSuccessor(self, action, nextCard) :       
        newConfig = self.deepcopy()
        newConfig.hands[action].append(nextCard)
        return newConfig

    def initialize(self, hands) :
        self.hands = {cardsDict._HAND1: hands[0],
                      cardsDict._HAND2: hands[1],
                      cardsDict._HAND3: hands[2],
                      cardsDict._HAND4: hands[3],
                      cardsDict._HAND5: hands[4],
                      }

class Actions :
    """
    allows to check the available actions for a given configuration
    """
    _actions = {1 : cardsDict._HAND1,
                2 : cardsDict._HAND2,
                3 : cardsDict._HAND3,
                4 : cardsDict._HAND4,
                5 : cardsDict._HAND5,
                }

    def getPossibleActions(config, plyNumber) :
        """
        returns action "names" as specified in cardsDict.py.
        can be converted to integers through "_actions"    
        """
        #plyNumber = 1...20
        maxSize = int(math.ceil(plyNumber/5) + 1)
        if maxSize > 5 : return []
        possibleActions = []
        
        for i in range(5) :
            hand = config.hands[cardsDict._HANDS[i]]
            if len(hand) <= maxSize:
                possibleActions.append(cardsDict._HANDS[i])
        return possibleActions
    getPossibleActions = staticmethod(getPossibleActions)

class AgentState :
    """
    Contains data about current state of agent.
    Contains current configuration, agent Name and the agent's current ply number (move no. ) in game
    """
    def __init__(self, startConfiguration, playerName, plyNumber):
        self.startConfiguration = startConfiguration
        self.configuration = startConfiguration
        self.name = playerName
        self.plyNumber = plyNumber
    
    def __str__(self) :
        return 'Player name: %s.\nPly Number: %i.\n%s' %(self.name, self.plyNumber, str(self.configuration))

    def getAsHidden(self):
        return 'Player name: %s.\nPly Number: %i.\n%s' %(self.name, self.plyNumber, self.configuration.getHiddenStateStr() )

    def __eq__(self, other) :
        #TODO
        return

    def deepcopy(self) :
        state = AgentState(self.startConfiguration , self.name, self.plyNumber)
        state.configuration = self.configuration.deepcopy()
        return state

    def getUnseenCards(self):
        return self.configuration.unseenCards

class GameStateData :
    """
    Contains all internal data of a game state.
    """
    
    def __init__(self, prevState = None) :
        """
        Generates a new data packet by copying information from its predecessor.
        """
        if prevState != None:
            self.agentStates = self.copyAgentStates(prevState.agentStates)
            self.deck = Deck(prevState.deck)
            self.totPlyNum = prevState.totPlyNum
            self.nextCard = self.deck[0]
        
    def copyAgentStates(self, agentStates) :
        copiedStates = []
        for agentState in agentStates:
            copiedStates.append(agentState.deepcopy() )
        return copiedStates

    def __str__(self) :
        stateDataStr = str('\n'+'='*50+'\n').join([str(self.agentStates[0]), str(self.agentStates[1] ) ])
        moveStr = 'Move #: %d' %(self.totPlyNum)
        return (stateDataStr + '\n' + moveStr + '\n' + '*'*72)

    def getAsHidden(self, agentIndex) :
        stateDataStr = str('\n'+'='*50+'\n').join([str(self.agentStates[agentIndex]), self.agentStates[(agentIndex+1)%2].getAsHidden() ])
        moveStr = 'Move #: %d' %(self.totPlyNum)
        return (stateDataStr + '\n' + moveStr + '\n' + '*'*72)

    def __hash__(self) :
        #TODO
        return

    def __eq__(self, other) :
        if not self.deck == other.deck : return False
        return self.agentStates == other.agentStates
    
    def popCard(self) :
        """
        removes next card from deck
        """
        return self.deck.pop()
    
    def deepcopy(self) :
        newStateData = GameStateData()
        newStateData.agentStates = self.copyAgentStates(self.agentStates)
        newStateData.deck = Deck(self.deck)
        newStateData.totPlyNum = self.totPlyNum
        newStateData.nextCard = newStateData.deck[0]
        return newStateData

    def initialize(self, deck, agents) :
        """
            Create new data packet from given permuatation of 52 cards (deck)
        """
        
        assert len(deck) == 52, "Size of initial deck is %r" %len(deck)
        handsA = []
        handsB = []
        for i in range(5) :
            handsA.append(Hand([deck.pop(0)] ) )
            handsB.append(Hand([deck.pop(0)] ) )
        self.deck = Deck(deck)
        self.nextCard = self.deck[0]
        configA = Configuration(deck, self.deck)
        configA.initialize(handsA)
        configB = Configuration(deck, self.deck)
        configB.initialize(handsB)
        agentA = AgentState(configA, agents[0].name, 0)
        agentB = AgentState(configB, agents[1].name, 0)
        
        self.agentStates = [agentA, agentB]
        self.totPlyNum = 0

class Game :
    """
    runs the game according to the game rules.
    deals with internal implications
    """
    def __init__(self, agentsA, agentsB, rules):
        self.agentsA = agentsA
        self.agentsB = agentsB
        #zipped[0]: agents for stage I
        #zipped[1]: agents for stage II
        self.zipped = zip(agentsA, agentsB)
        self.rules = rules
        return

    def run(self, dirName, log = None, verbose = True):
        agents = self.zipped[0]
        while not self.state.isGameOver() :
            #let the fun begin
            if self.state.data.totPlyNum >= 30:
                agents = self.zipped[1]
            for i  in range(2):
                agent = agents[i]
                observation = self.state.deepcopy()
                action = agent.getAction(observation)
                self.state = self.state.generateSuccessor(i, action)
            if log != None:
                log.write(str(self.state) + '\n')
        
        index, numWins = self.rules.decideWinner(self.state)
        verdictStr = '{!s} Wins!: {:n}/5'.format(agents[index].name, numWins)
        if log != None:
            log.write('\n'.join(str(item) for item in self.getScore().items() ) )
            log.write('\n' + verdictStr)
        scores = self.getScore()
        score1 = self.state.getAgentState(0).name + ':\n' +  '\n'.join(str(k) + ': ' + str(v) for k,v in scores[self.state.getAgentState(0).name])
        score2 = self.state.getAgentState(1).name + ':\n' + '\n'.join(str(k) + ': ' + str(v) for k,v in scores[self.state.getAgentState(1).name])
        if verbose :
            print self.state
            print '\n'.join([score1, score2])
            print verdictStr
        return agents[index].name
    
    def getScore(self):
        p1=[]
        p2=[]
        for i in range(5) :
            key = cardsDict._HANDS[i]
            p1.append((key,evalHand(self.state.getAgentState(0).configuration.hands[key])) )
            p2.append((key,evalHand(self.state.getAgentState(1).configuration.hands[key])) )
        scoreDict = dict()
        scoreDict[self.state.getAgentState(0).name] = p1
        scoreDict[self.state.getAgentState(1).name] = p2
        return scoreDict
    
    