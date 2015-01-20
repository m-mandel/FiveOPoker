import os, operator
import pygame
from pygame.locals import *
import cardsDict
from keyboardAgent import KeyboardAgent
from handEvaluator import evalHand

CARDS_IM = {cardsDict._2C : 'c2',
            cardsDict._2D : 'd2',
            cardsDict._2H : 'h2',
            cardsDict._2S : 's2',
            cardsDict._3C : 'c3',
            cardsDict._3D : 'd3',
            cardsDict._3H : 'h3',
            cardsDict._3S : 's3',
            cardsDict._4C : 'c4',
            cardsDict._4D : 'd4',
            cardsDict._4H : 'h4',
            cardsDict._4S : 's4',
            cardsDict._5C : 'c5',
            cardsDict._5D : 'd5',
            cardsDict._5H : 'h5',
            cardsDict._5S : 's5',
            cardsDict._6C : 'c6',
            cardsDict._6D : 'd6',
            cardsDict._6H : 'h6',
            cardsDict._6S : 's6',
            cardsDict._7C : 'c7',
            cardsDict._7D : 'd7',
            cardsDict._7H : 'h7',
            cardsDict._7S : 's7',
            cardsDict._8C : 'c8',
            cardsDict._8D : 'd8',
            cardsDict._8H : 'h8',
            cardsDict._8S : 's8',
            cardsDict._9C : 'c9',
            cardsDict._9D : 'd9',
            cardsDict._9H : 'h9',
            cardsDict._9S : 's9',
            cardsDict._10C : 'c10',
            cardsDict._10D : 'd10',
            cardsDict._10H : 'h10',
            cardsDict._10S : 's10',
            cardsDict._JACK_C : 'cj',
            cardsDict._JACK_D : 'dj',
            cardsDict._JACK_H : 'hj',
            cardsDict._JACK_S : 'sj',
            cardsDict._QUEEN_C : 'cq',
            cardsDict._QUEEN_D : 'dq',
            cardsDict._QUEEN_H : 'hq',
            cardsDict._QUEEN_S : 'sq',
            cardsDict._KING_C : 'ck',
            cardsDict._KING_D : 'dk',
            cardsDict._KING_H : 'hk',
            cardsDict._KING_S : 'sk',
            cardsDict._ACE_C : 'ca',
            cardsDict._ACE_D : 'da',
            cardsDict._ACE_H : 'ha',
            cardsDict._ACE_S : 'sa',
            'back' : 'back',
            }
_HAND1 = 'hand 1'
_HAND2 = 'hand 2'
_HAND3 = 'hand 3'
_HAND4 = 'hand 4'
_HAND5 = 'hand 5'
_HANDS = {      0 : _HAND1,
                1 : _HAND2,
                2 : _HAND3,
                3 : _HAND4,
                4 : _HAND5,
              }

def load_image(name, card, colorkey = None) :
    if card == True:
        fullname = os.path.join('images/cards/', name)
    else:
        fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannont load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


class Card(pygame.sprite.Sprite):
    """

    """
    def __init__(self, cardName, position, movable = False):
        pygame.sprite.Sprite.__init__(self)
        self.cardName = cardName
        imageName = CARDS_IM[cardName]
        self.cardImage = imageName + '.png'
        self.image, self.rect = load_image(self.cardImage, True)
        self.movable = movable
        self.position = position
        self.rect.center = position
        self.revealed = False
        self.moving = False

    def __str__(self):
        return self.cardName

    def hide(self) :
        self. image, self.rect = load_image('back.png', True)
        self.rect.center = self.position

    def reveal(self) :
        self.revealed = True
        self. image, self.rect = load_image(self.cardImage, True)
        self.rect.center = self.position
    
    def update(self):
        if self.movable and pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos() ):
            self.rect.center = pygame.mouse.get_pos()
            self.moving = True
        elif not pygame.mouse.get_pressed()[0]:
            self.rect.center = self.position
            self.moving = False

    def draw(self, screen) :
        screen.blit(self.image, self.rect)
    
    def getPosition(self) :
        return self.position

    def setPosition(self, position) :
        self.position = position
    
    def updatePos(self) :
        self.rect.center = pygame.mouse.get_pos()

    def resetPos(self):
        self.rect.center = self.position
    
    def isMovable(self) :
        return self.movable

    def move(self, targetPos):
        """
        move card to targetPos
        """
        if self.movable:
            relativePos = tuple(map(operator.sub, targetPos, self.position))
            self.rect = self.move(relativePos[0], relativePos[1])
            self.position = targetPos


        

class Display():
    _DX = 100
    _DY = 25
    _PLAYER = 0
    _OPPONENT = 1
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 600))
        pygame.display.set_caption('Five O Poker')
        self.myfont = pygame.font.SysFont("Arial Black", 32)
        pygame.mouse.set_visible(1)
        self.nextCardDisplay = Card('back', tuple(map(operator.add, self.screen.get_rect().center, (-300, 0) ) ) )
        self.deckCard = Card('back', tuple(map(operator.add, self.screen.get_rect().center, (-325, 0) ) ) )
        self.hands0 = dict()
        self.hands1 = dict()
        self.background = pygame.Surface(self.screen.get_size() )
        self.background = self.background.convert()
        self.background.fill((0,100,0))

        self.screen.blit(self.background, (0,0) )
        pygame.display.flip()
        self.humanAgentIndex = -1
        self.clock = pygame.time.Clock()
        self.mX, self.mY = 0, 0

    def update(self):
        self.clock.tick(40)
        self.screen.blit(self.background, (0,0) )
        self.screen.blit(self.aLabel, map(operator.add, self.screen.get_rect().center, (-400, 200) ) )
        self.screen.blit(self.bLabel, map(operator.add, self.screen.get_rect().center, (-400, -200) ) )
        if self.nextCardDisplay.moving :
            self.nextCardDisplay.updatePos()

        #if self.nextCardDisplay.rect.collidepoint(pygame.mouse.get_pos() ) and pygame.mouse.get_pressed()[0] and self.nextCardDisplay.isMovable():
        #    self.nextCardDisplay.updatePos()
        #elif not pygame.mouse.get_pressed()[0]:
        #    self.nextCardDisplay.resetPos()
        self.nextCardDisplay.update()
        for j in range(2) :
            for i in range(5) :
                hand = _HANDS[i]
                if len(self.agents[self._OPPONENT][hand]) == 5 and not self.agents[self._OPPONENT][hand][4].revealed :
                    self.agents[self._OPPONENT][hand][4].hide()
                    self.agents[self._OPPONENT][hand][4].draw(self.screen)

                for card in self.agents[j][hand] :         
                    card.update()
                    card.draw(self.screen)

        self.deckCard.draw(self.screen)
        self.nextCardDisplay.draw(self.screen)
        self.nextCardDisplay.update()
        pygame.display.update()
    
    def initialize(self, gameState) :
        self.gameState = gameState
        self.agentsIndices = dict()
        position0 = tuple(map(operator.add, self.screen.get_rect().center, (-200, 50) ) )
        
        
        position1 = tuple(map(operator.add, self.screen.get_rect().center, (-200, -175) ) )
        for i in range(2) :
            agent = self.agentsType[i]
            
            if isinstance(agent, KeyboardAgent) :
                self.humanAgentIndex = i
                self.playerAName = agent.name
                self.playerBName = self.agentsType[(i+1)%2].name                
                self.agentsIndices[i] = self._PLAYER
                self.agentsIndices[(i+1)%2] = self._OPPONENT
                agentState0 = gameState.getAgentState(i)
                agentState1 = gameState.getAgentState((i+1)%2)
                break
            else:
                self.agentsIndices[0] = self._PLAYER
                self.agentsIndices[1] = self._OPPONENT
                agentState0 = gameState.getAgentState(self._PLAYER)
                agentState1 = gameState.getAgentState(self._OPPONENT)
                self.playerAName = gameState.getAgentState(self._PLAYER).name
                self.playerBName = gameState.getAgentState(self._OPPONENT).name
        self.aLabel = self.myfont.render(self.playerAName, 1, (255,255,255))
        self.bLabel = self.myfont.render(self.playerBName, 1, (255,255,255))
        self.agents = dict()
        self.agents[self._PLAYER] = self.hands0
        self.agents[self._OPPONENT] = self.hands1
        for i in range(5) :
            tmpCard0 = Card(cardsDict.INVERTED_INTVAL[agentState0.configuration.hands[_HANDS[i] ][0] ], tuple(map(operator.add, position0, (100 + self._DX * i,self._DY) ) ) )
            self.agents[self._PLAYER][_HANDS[i]] = list([tmpCard0]) 
            tmpCard1 = Card(cardsDict.INVERTED_INTVAL[agentState1.configuration.hands[_HANDS[i] ][0] ], tuple(map(operator.add, position1, (100 + self._DX * i,self._DY) ) ) )
            self.agents[self._OPPONENT][_HANDS[i]] = list([tmpCard1]) 

        
    
    def run(self, game, dirName, log = None, verbose = True):
        self.agentsType = game.zipped[0]
        self.initialize(game.state)
        self.update()
        while not game.state.isGameOver():
            self.getEvent()
            for i  in range(2):
                self.nextCardDisplay = Card(cardsDict.INVERTED_INTVAL[game.state.data.deck[0]], tuple(map(operator.add, self.screen.get_rect().center, (-300, 0) ) ) )
                self.update()
                if game.state.data.totPlyNum >= 30:
                    self.agentsType = game.zipped[1]
                agent = self.agentsType[i]
                observation = game.state.deepcopy()
                if isinstance(agent, KeyboardAgent) :
                    action = agent.getAction(observation, self)
                else:
                    action = agent.getAction(observation)
                self.applyAction(self.agentsIndices[i], action)

                game.state = game.state.generateSuccessor(i, action)                
                self.gameState = game.state
    
            if log != None:
                log.write(str(game.state) + '\n')

        self.nextCardDisplay = Card('back', tuple(map(operator.add, self.screen.get_rect().center, (-300, 0) ) ) )
        
        
        
        index, numWins = game.rules.decideWinner(game.state)
        verdictStr = '{!s} Wins!: {:n}/5'.format(self.agentsType[index].name, numWins)
        if log != None:
            log.write('\n'.join(str(item) for item in game.getScore().items() ) )
            log.write('\n' + verdictStr)
        scores = game.getScore()
        score1 = game.state.getAgentState(0).name + ':\n' +  '\n'.join(str(k) + ': ' + str(v) for k,v in scores[game.state.getAgentState(0).name])
        score2 = game.state.getAgentState(1).name + ':\n' + '\n'.join(str(k) + ': ' + str(v) for k,v in scores[game.state.getAgentState(1).name])
        if verbose :
            print game.state
            print '\n'.join([score1, score2])
            print verdictStr
        if self.humanAgentIndex != -1 :
            for i in range(5) :
                hand = _HANDS[i]
                self.agents[self._OPPONENT][hand][4].reveal()
                self.agents[self._OPPONENT][hand][4].draw(self.screen)
        self.update()
        self.printVerdict()
        verdictLabel = self.myfont.render(verdictStr, 1, (255,255,255))
        self.screen.blit(verdictLabel, (400,20))
        pygame.display.update()
        while self.getEvent() != -1:
            continue
        return self.agentsType[index].name
    
    
    def getEvent(self):
       for event in pygame.event.get():
           if event.type == QUIT:
               return 
           elif event.type == KEYDOWN and event.key == K_ESCAPE:
               return -1
           elif event.type == MOUSEBUTTONDOWN:
               self.mX, self.mY  = pygame.mouse.get_pos()
           elif event.type == MOUSEBUTTONUP:
               self.mX, self.mY = 0, 0

    
    def getMove(self, agentIndex):
        """
        get a move for keyboard agent
        """
        self.nextCardDisplay.movable = True
        while 1:
            self.getEvent()
            self.update()
            for i in range(5):
                if pygame.sprite.collide_rect(self.nextCardDisplay, self.agents[self.agentsIndices[agentIndex]][_HANDS[i]][-1]) and pygame.mouse.get_pressed()[0]:
                    self.getEvent()
                    if not pygame.mouse.get_pressed()[0]:
                        return _HANDS[i]
                elif self.agents[self.agentsIndices[agentIndex]][_HANDS[i]][-1].rect.collidepoint(pygame.mouse.get_pos() ) and not pygame.mouse.get_pressed()[0]:
                    self.getEvent()
                    if pygame.mouse.get_pressed()[0]:
                        pygame.time.delay(100)
                        return _HANDS[i]

    def applyAction(self, agentIndex, action):
        """
        apply action for computer agent
        """
        #dy = self._DY if agentIndex == 0 else -self._DY
        position = tuple(map(operator.add, self.agents[agentIndex][action][-1].position, (0, self._DY) ) )
        tmp = Card(self.nextCardDisplay.cardName, position)
        self.agents[agentIndex][action].append(tmp)

    def printVerdict(self) :
        myfont = pygame.font.SysFont("Arial Black", 32)      
        label = winLabel = myfont.render("Win", 1, (102,146,27))
        loseLabel = myfont.render("Lose", 1, (255,0,0))
        for i in range(5) :
            hand = _HANDS[i]
            playerVal = evalHand([cardsDict.INTVAL[x.cardName] for x in  self.agents[self._PLAYER][hand]])
            opponentVal = evalHand([cardsDict.INTVAL[x.cardName] for x in  self.agents[self._OPPONENT][hand]])
            if playerVal > opponentVal :
                position = self.agents[self._PLAYER][hand][-1].position
            elif opponentVal > playerVal :
                position = self.agents[self._OPPONENT][hand][-1].position
            else:
                label = myfont.render("Tie", 1, (0,255,0))
                position = (self.screen.get_rect().center[0], self.agents[self._PLAYER][hand][-1].position[1])
            self.screen.blit(label, tuple(map(operator.add,position, (-34,-20) ) ) )

        pygame.display.update()