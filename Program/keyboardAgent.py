from game import Agent
from game import Actions
import cardsDict
import time


class KeyboardAgent(Agent) :
    """
    an agent controlled by keyboard
    """
    def getAction(self, state, display = None) :
        legal = state.getLegalActions(self.index)
        move = ''
        while move not in legal:
            if display is not None:
                move = display.getMove(self.index)
            else:
                print state.getAsHidden(self.index)
                print '%s\'s turn.'%(self.name)
                print 'nextCard: ', cardsDict.INVERTED_INTVAL[state.data.nextCard]
                move = self.getMove(state)
        return move

    def getMove(self, state) :
        key = 'a'
        while (True):
            key = raw_input('Action:')
            if key in set("123456"):
                break
            else:
                print state.getAsHidden(self.index)
                print '%s\'s turn.'%(self.name)
                print 'NextCard: ', cardsDict.INVERTED_INTVAL[state.data.nextCard]
                 
                
        return Actions._actions[int(key)]
