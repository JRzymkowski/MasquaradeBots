# sample bot
# not so simple bot

import random
import numpy as np
import superposition from superposition.py

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
  
  
  def RecieveLookUp(self, player, card):
    self.belief.reveal(player, card)
    
  def UpdateBeliefsOnGameStart(self):
    self.belief = superposition(self.board.numberOfCards)
    
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
      if(self.board.thisEvent.eventAction.actionType == 'announce' and self.board.thisEvent.performingPlayer != None):
        if(self.board.thisEvent.eventAction.announcement == 'Inquisitor'):
          for card in self.board.thisEvent.cardsRevealed:
            self.belief.reveal(card[0], card[1])
        elif(self.board.thisEvent.eventAction.announcement == 'Fool' and self.board.thisEvent.performingPlayer != self.myNumber):
          self.belief.swap((self.board.thisEvent.response.cardA, self.board.thisEvent.response.cardB), 0.7)
        elif(self.board.thisEvent.eventAction.announcement == 'Spy' and self.board.thisEvent.performingPlayer != self.myNumber):
          self.belief.swap((self.board.thisEvent.performingPlayer, self.board.thisEvent.response.target), 0.7)
      elif(self.board.thisEvent.eventAction.actionType == 'swap' and self.board.thisEvent.actingPlayer != self.myNumber):
        self.belief.swap((self.board.thisEvent.actingPlayer, self.board.thisEvent.eventAction.cardToSwap), 0.7)
        
    
  def Action(self, actionMode):
    
    if(actionMode == 'Swap only' or actionMode == 'Announcing banned'):
      action = adHoc()
      action.actionType = 'swap'
      action.cardToSwap =  (self.myNumber + random.randint(1, self.board.numberOfCards-1)) % self.board.numberOfCards
      decision = (random.random() < 0.7)
      action.swapTrue = 1 if decision else 0
      if(decision):
        self.belief.swap((self.myNumber, action.cardToSwap), 1)
      return action
    
    if(random.random() < 0.15):
      action = adHoc()
      action.actionType = 'lookUp'
      return action
    elif(random.random() < 0.3):
      action = adHoc()
      action.actionType = 'swap'
      action.cardToSwap =  (self.myNumber + random.randint(1, self.board.numberOfCards-1)) % self.board.numberOfCards
      decision = (random.random() < 0.7)
      action.swapTrue = 1 if decision else 0
      if(decision):
        self.belief.swap((self.myNumber, action.cardToSwap), 1)
      return action
    else:
      beliefMatrix = self.belief.belief().transpose()
      myMostProbableCards = [i for i in list(range(self.board.numberOfCards)) if beliefMatrix[:,self.myNumber][i] == max(beliefMatrix[:,self.myNumber])]
      announceCard = random.choice(myMostProbableCards) # works also if only one most probable
      action = adHoc()
      action.actionType = 'announce'
      action.announcement = self.board.startingPermutationCards[announceCard]
        
      if(max(beliefMatrix[:][self.myNumber]) < 1 and self.board.playerCoins[self.myNumber] == 1):
        action = adHoc()
        action.actionType = 'lookUp'
        return action
        
      if(self.board.coinsInCourthouse > 2):
        if(beliefMatrix[self.board.startingPermutationCards.index('Judge')][self.myNumber] > (1.0/self.board.coinsInCourthouse)):
            action.announcement = 'Judge'
      
      return action
  
  def Respond(self, query):
    if(type(query) == tuple):
      if(query[0] == 'Bishop'):
        response = adHoc()
        response.target = random.choice(query[1])
        return response
    elif(query == 'Fool'):
      response = adHoc()
      response.cardA =  (self.myNumber + random.randint(1, self.board.numberOfCards-1)) % self.board.numberOfCards
      available = list(range(self.board.numberOfCards))
      available.remove(self.myNumber)
      available.remove(response.cardA)
      response.cardB = available[random.randint(0, len(available)-1)]
      decision = (random.random() < 0.5)
      response.swapTrue = 1 if decision else 0
      if(decision):
        self.belief.swap((response.cardA, response.cardB), 1)
      return  response
    elif(query == 'Witch'):
      response = adHoc()
      richest = [i for i in list(range(self.board.numberOfPlayers)) if self.board.playerCoins[i] == max(self.board.playerCoins)]
      if self.myNumber in richest:
        response.swapWith = None
        return response
      else:
        response.swapWith = random.choice(richest)
        return response
    elif(query == 'Spy'):
      beliefMatrix = self.belief.belief().transpose()
      maxims = [max(beliefMatrix[:,i]) for i in list(range(self.board.numberOfCards))]
      minimaxs = [index for index, maxim in enumerate(maxims) if maxim == min(maxims)]
    
      response = adHoc()
      response.target = random.choice(minimaxs)
      self.choosenTargetOnSpy = response.target
      return response
    elif(query == 'SpySwap'):
      response = adHoc()
      decision = (random.random() < 0.5)
      response.swapTrue = 1 if decision else 0
      if(decision):
        self.belief.swap((self.myNumber, self.choosenTargetOnSpy), 1)
      return response
    elif(query == 'Inquisitor'):
      beliefMatrix = self.belief.belief().transpose()
      maxims = [max(beliefMatrix[:,i]) for i in list(range(self.board.numberOfPlayers))]
      minimaxs = [index for index, maxim in enumerate(maxims) if maxim == min(maxims)]
    
      response = adHoc()
      response.target = random.choice(minimaxs)
      return response
    elif(query == 'Inquisition'):
      beliefMatrix = self.belief.belief().transpose()
      myMostProbableCards = [i for i in list(range(self.board.numberOfCards)) if beliefMatrix[:,self.myNumber][i] == max(beliefMatrix[:,self.myNumber])]
      announceCard = random.choice(myMostProbableCards)
      
      response = adHoc()
      response.answer = self.board.startingPermutationCards[announceCard]
      return response
    
  def Challenge(self):
    
        
    beliefMatrix = self.belief.belief().transpose()
    announcerChance = beliefMatrix[self.board.startingPermutationCards.index(self.board.thisEvent.eventAction.announcement), self.board.thisEvent.actingPlayer]
    myChance = beliefMatrix[self.board.startingPermutationCards.index(self.board.thisEvent.eventAction.announcement), self.myNumber]
    if(myChance < 1 and self.board.playerCoins[self.myNumber] == 1):
        return False
    if(myChance > announcerChance):
      return True
    elif(self.board.coinsInCourthouse > 2 and self.board.thisEvent.eventAction.announcement == 'Judge'):
        if(beliefMatrix[self.board.startingPermutationCards.index('Judge')][self.myNumber] > (1.0/self.board.coinsInCourthouse)):
            return True
    elif(random.random() > 0.9): # let's add 10% chance of randomly challenging
        return True
    else:
      return False
