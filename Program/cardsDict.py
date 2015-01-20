
_2C = '2 clubs'
_2D = '2 diamonds'
_2H = '2 hearts'
_2S = '2 spades'
_3C = '3 clubs'
_3D = '3 diamonds'
_3H = '3 hearts'
_3S = '3 spades'
_4C = '4 clubs'
_4D = '4 diamonds'
_4H = '4 hearts'
_4S = '4 spades'
_5C = '5 clubs'
_5D = '5 diamonds'
_5H = '5 hearts'
_5S = '5 spades'
_6C = '6 clubs'
_6D = '6 diamonds'
_6H = '6 hearts'
_6S = '6 spades'
_7C = '7 clubs'
_7D = '7 diamonds'
_7H = '7 hearts'
_7S = '7 spades'
_8C = '8 clubs'
_8D = '8 diamonds'
_8H = '8 hearts'
_8S = '8 spades'
_9C = '9 clubs'
_9D = '9 diamonds'
_9H = '9 hearts'
_9S = '9 spades'
_10C = '10 clubs'
_10D = '10 diamonds'
_10H = '10 hearts'
_10S = '10 spades'
_JACK_C = 'Jack clubs'
_JACK_D = 'Jack diamonds'
_JACK_H = 'Jack hearts'
_JACK_S = 'Jack spades'
_QUEEN_C = 'Queen clubs'
_QUEEN_D = 'Queen diamonds'
_QUEEN_H = 'Queen hearts'
_QUEEN_S = 'Queen spades'
_KING_C = 'King clubs'
_KING_D = 'King diamonds'
_KING_H = 'King hearts'
_KING_S = 'King spades'
_ACE_C = 'Ace clubs'
_ACE_D = 'Ace diamonds'
_ACE_H = 'Ace hearts'
_ACE_S = 'Ace spades'
_JOKER = 'Joker'

#ranks
_R_TWO = 0
_R_THREE = 1
_R_FOUR = 2
_R_FIVE = 3
_R_SIX = 4
_R_SEVEN = 5
_R_EIGHT = 6
_R_NINE = 7
_R_TEN = 8
_R_JACK = 9
_R_QUEEN = 10
_R_KING = 11
_R_ACE = 12
_R_JOKER = -1

#suits
_S_JOKER = -1
_S_CLUBS = 0
_S_DIAMONDS = 1
_S_HEART = 2
_S_SPADE = 3

INTVAL = {  _JOKER : -1,
            _2C : 1,
            _2D : 2, 
            _2H : 3,
            _2S : 4,
            _3C : 5,
            _3D : 6,
            _3H : 7,
            _3S : 8,
            _4C : 9,
            _4D : 10,
            _4H : 11,
            _4S : 12,
            _5C : 13,
            _5D : 14,
            _5H : 15,
            _5S : 16,
            _6C : 17,
            _6D : 18,
            _6H : 19,
            _6S : 20,
            _7C : 21,
            _7D : 22,
            _7H : 23,
            _7S : 24,
            _8C : 25,
            _8D : 26,
            _8H : 27,
            _8S : 28,
            _9C : 29,
            _9D : 30,
            _9H : 31,
            _9S : 32,
            _10C : 33,
            _10D : 34,
            _10H : 35,
            _10S : 36,
            _JACK_C : 37,
            _JACK_D : 38,
            _JACK_H : 39,
            _JACK_S : 40,
            _QUEEN_C : 41,
            _QUEEN_D : 42,
            _QUEEN_H : 43,
            _QUEEN_S : 44,
            _KING_C : 45,
            _KING_D : 46,
            _KING_H : 47,
            _KING_S : 48,
            _ACE_C : 49,
            _ACE_D : 50,
            _ACE_H : 51,
            _ACE_S : 52,
        }

#lookup for card id by int value.
#(<int val>, <card str>) as (key,value) pairs
INVERTED_INTVAL = dict([[v,k] for k,v in INTVAL.items()])

RANK = {    _2C : _R_TWO,
            _2D : _R_TWO, 
            _2H : _R_TWO,
            _2S : _R_TWO,
            _3C : _R_THREE,
            _3D : _R_THREE,
            _3H : _R_THREE,
            _3S : _R_THREE,
            _4C : _R_FOUR,
            _4D : _R_FOUR,
            _4H : _R_FOUR,
            _4S : _R_FOUR,
            _5C : _R_FIVE,
            _5D : _R_FIVE,
            _5H : _R_FIVE,
            _5S : _R_FIVE,
            _6C : _R_SIX,
            _6D : _R_SIX,
            _6H : _R_SIX,
            _6S : _R_SIX,
            _7C : _R_SEVEN,
            _7D : _R_SEVEN,
            _7H : _R_SEVEN,
            _7S : _R_SEVEN,
            _8C : _R_EIGHT,
            _8D : _R_EIGHT,
            _8H : _R_EIGHT,
            _8S : _R_EIGHT,
            _9C : _R_NINE,
            _9D : _R_NINE,
            _9H : _R_NINE,
            _9S : _R_NINE,
            _10C : _R_TEN,
            _10D : _R_TEN,
            _10H : _R_TEN,
            _10S : _R_TEN,
            _JACK_C : _R_JACK,
            _JACK_D : _R_JACK,
            _JACK_H : _R_JACK,
            _JACK_S : _R_JACK,
            _QUEEN_C : _R_QUEEN,
            _QUEEN_D : _R_QUEEN,
            _QUEEN_H : _R_QUEEN,
            _QUEEN_S : _R_QUEEN,
            _KING_C : _R_KING,
            _KING_D : _R_KING,
            _KING_H : _R_KING,
            _KING_S : _R_KING,
            _ACE_C : _R_ACE,
            _ACE_D : _R_ACE,
            _ACE_H : _R_ACE,
            _ACE_S : _R_ACE,
            _JOKER : _R_JOKER,
        }

SUIT = {    _2C: _S_CLUBS,
            _2D : _S_DIAMONDS, 
            _2H : _S_HEART,
            _2S : _S_SPADE,
            _3C : _S_CLUBS,
            _3D : _S_DIAMONDS,
            _3H : _S_HEART,
            _3S : _S_SPADE,
            _4C : _S_CLUBS,
            _4D : _S_DIAMONDS,
            _4H : _S_HEART,
            _4S : _S_SPADE,
            _5C : _S_CLUBS,
            _5D : _S_DIAMONDS,
            _5H : _S_HEART,
            _5S : _S_SPADE,
            _6C : _S_CLUBS,
            _6D : _S_DIAMONDS,
            _6H : _S_HEART,
            _6S : _S_SPADE,
            _7C : _S_CLUBS,
            _7D : _S_DIAMONDS,
            _7H : _S_HEART,
            _7S : _S_SPADE,
            _8C : _S_CLUBS,
            _8D : _S_DIAMONDS,
            _8H : _S_HEART,
            _8S : _S_SPADE,
            _9C : _S_CLUBS,
            _9D : _S_DIAMONDS,
            _9H : _S_HEART,
            _9S : _S_SPADE,
            _10C : _S_CLUBS,
            _10D : _S_DIAMONDS,
            _10H : _S_HEART,
            _10S : _S_SPADE,
            _JACK_C : _S_CLUBS,
            _JACK_D : _S_DIAMONDS,
            _JACK_H : _S_HEART,
            _JACK_S : _S_SPADE,
            _QUEEN_C : _S_CLUBS,
            _QUEEN_D : _S_DIAMONDS,
            _QUEEN_H : _S_HEART,
            _QUEEN_S : _S_SPADE,
            _KING_C : _S_CLUBS,
            _KING_D : _S_DIAMONDS,
            _KING_H : _S_HEART,
            _KING_S : _S_SPADE,
            _ACE_C : _S_CLUBS,
            _ACE_D : _S_DIAMONDS,
            _ACE_H : _S_HEART,
            _ACE_S : _S_SPADE,
            _JOKER : _S_JOKER,        
        }

_HAND1 = 'hand 1'
_HAND2 = 'hand 2'
_HAND3 = 'hand 3'
_HAND4 = 'hand 4'
_HAND5 = 'hand 5'
_HANDS = {  0 : _HAND1,
            1 : _HAND2,
            2 : _HAND3,
            3 : _HAND4,
            4 : _HAND5,
            }