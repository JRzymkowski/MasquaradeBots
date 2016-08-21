import sampleBot from sampleBot.py
import MascardeGame from game.py
import numpy as np

players = [sampleBot() for _ in list(range(8))]
cardSet = ['Judge', 'King', 'Queen', 'Cheat', 'Bishop', 'Widow', 'Spy', 'Fool']

np.set_printoptions(formatter={'float': '{: 0.3f}'.format})

endMode, winners, gameLog, errorLog = MascaradeGame(players, cardSet, 100)

print(endMode, winners)
print(errorLog)

def verySimpleGameLogFormatter(gameLog):
  print("Coins by player; Coins in Courthouse; Acting player; Type of Action; (Announcement, Challengers, Player performing card action)")
  print("Last three only applicable if action is announcement, \'/\' in place of challengers, if none")
  print([6]*gameLog[0].board.numberOfPlayers, end = ' ')
  print("0 0 swap")
  
  for index in range(1,len(gameLog)):
    print(gameLog[index-1].board.playerCoins, gameLog[index-1].board.coinsInCourthouse,
    gameLog[index].event.actingPlayer, gameLog[index].event.eventAction.actionType, end = ' ')
    if(gameLog[index].event.eventAction.actionType == 'announce'):
       print(gameLog[index].event.eventAction.announcement,
       (gameLog[index].event.challengers if len(gameLog[index].event.challengers) > 1 else '/'),
       gameLog[index].event.performingPlayer, end = '')
    print()
    
  print(gameLog[-1].board.playerCoins)
    
verySimpleGameLogFormatter(gameLog)
