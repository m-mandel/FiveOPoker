from ctypes import *
import os, sys
LIB_FILE = ".\\library\\libPoker.dll"
global pokerLib

pokerLib = CDLL(LIB_FILE)



def evalHand(hand):
    global pokerLib
    cHand = (c_int * 5)(hand[0], hand[1], hand[2], hand[3], hand[4])
    return pokerLib.getHandRank(cHand)