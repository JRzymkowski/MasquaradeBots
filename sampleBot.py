# sample bot
# not so simple bot

import superposition.py
import random
import numpy as np

class adHoc():
  pass

class sampleBot:
  board = None
  events = []
  fullySupportedCardSet = ['Judge', 'King', 'Queen', 'Cheat', 'Bishop', 'Spy', 'Thief']
  supportedCardSet = ['Judge', 'King', 'Queen', 'Cheat', 'Bishop', 'Spy', 'Thief', 'Peasant', 'Witch', 'Widow', 'Inquisitor']
  lastWake = -1
  myNumber = -1
  lastWakeFor = ''
  
  belief = superposition()
  
  def RecieveLookUp(self, player, card):
    self.belief.reveal(player, card)
    
  def UpdateBeliefsOnGameStart(self, gameMoment):
    pass
    
  def UpdateBeliefs(self, gameMoment):
    if(gameMoment == 'BeforeChallenging'):
      # making predictions after a player announced and possibly some players claimed to have the announced card
      # this simple bot ignores such information
      pass
    elif(gameMoment == 'AfterChallenging'):
      # possibly some cards were revealed here
      # also, making prediction based on whether further players challenged the announcer
      # this simple bot only does the former
      for card in self.board.thisEvent.cardsRevealed:
        self.belief.reveal(card[0], card[1])
    elif(gameMoment == 'EndOfAction'):
      # wrapping it all up
      if(self.board.thisEvent.eventAction.actionType == 'announce'):
        if(self.board.thisEvent.eventAction.announcement == 'Inquisitor'):
          for card in self.board.thisEvent.cardsRevealed:
            self.belief.reveal(card[0], card[1])
        elif(self.board.thisEvent.eventAction.announcement == 'Fool' and self.board.thisEvent.performingPlayer != myNumber):
          self.belief.swap(self.board.thisEvent.response.cardA, self.board.thisEvent.response.cardB, 0.6)
        elif(self.board.thisEvent.eventAction.announcement == 'Spy' and self.board.thisEvent.performingPlayer != myNumber):
          self.belief.swap(self.board.thisEvent.performingPlayer, self.board.thisEvent.response.target, 0.5)
      elif(self.board.thisEvent.eventAction.actionType == 'swap' and self.board.thisEvent.performingPlayer != myNumber):
        self.belief.swap(self.board.thisEvent.actingPlayer, self.board.thisEvent.eventAction.cardToSwap, 0.7)
        
    
  def Action(self):
    if(random.random() < 0.1):
      action = adHoc()
      action.actionType = 'lookUp'
      return action
    elif(random.random() < 0.5):
      action = adHoc()
      action.actionType = 'swap'
      action.cardToSwap =  (self.myNumber + random.randint(1, self.board.numberOfPlayers-1)) % self.board.numberOfPlayers
      decision = (random.random() < 0.7)
      action.swapTrue = 1 if decision else 0
      if(decision):
        self.belief.swap(self.myNumber, action.cardToSwap, 1)
      return action
    else:
      beliefMatrix = belief.belief()
      myMostProbableCards = [i for i in beliefMatrix[:,3] if beliefMatrix[:,3][i] == max(beliefMatrix[:,3])]
      announceCard = myMostProbableCards[random.randint(0, len(myMostProbableCards)-1)] # works also if only one most probable
      action = adHoc()
      action.actionType = 'announce'
      action.announcement = self.board.startingPermutationCards.index(announceCard)

