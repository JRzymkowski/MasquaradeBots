# Portions of code copied from: Michał Kaftanowicz, http://kaftanowicz.com
# Based on code by: Michał Kaftanowicz, http://kaftanowicz.com
# Inspiration from: Przemysław Kowalczyk, http://pkowalczyk.pl/
# Disclaimer:
# Mascarade board game was created by Bruno Faidutti (http://faidutti.com/blog/)
# Rules encoded and quoted in this program are referenced
# for educational purposes only.

import numpy as np
import random
import copy

# Simple hack for creating ad hoc objects instead of dictionaries
class adHoc:
    pass

# Auxiliary functions

def update(destination, source):
    for att in source.__dict__:
        destination.__dict__[att] = copy.deepcopy(source.__dict__[att])
    diri = copy.deepcopy(destination.__dict__)
    for att in diri:
        if att not in source.__dict__:
            destination.__dict__.pop(att, None)
    

def SwapCards(permutation, cardA, cardB):
    temp = permutation[cardA]
    permutation[cardA] = permutation[cardB]
    permutation[cardB] = temp
    
def RandomSwap(currentPlayer, playersNumber)
    A = action()
    A.actionType = 'swap'
    A.cardToSwap = (currentPlayer + random.randint(1, playersNumber-1)) % playersNumber
    A.actionTrue = (random.random() > 0.5)
    return A

# actionModes = ('Regular', 'Swap only', 'Challenge the announcer')
# actionTypes = ('Swap my card', 'Look at my card', 'Announce my character')

playersNames = ['Alice', 'Bob', 'Carol', 'David', 'Elise', 'Felix', ]
players = []
#players = [botA, botB, botC, botD, botE]
cardSet = ['Judge', 'King', 'Queen', 'Cheat', 'Bishop', 'Spy', 'Thief']

def MascaradeGame(playersSet, cardSet, gameLength):
    
    # returns endMode ('win', 'tie', 'timeout') and list winner (one element if win, multipe if tie, none if timeout)
    
    errorLog = []
    gameLog = []
    
    # Initilize game
    # board collects all the information to be aviable to bots
    # bots operate on boardCopy, lest they modify board
    # boardCopy is a *DeepCopy* of board
    # boardCopy should be updated every time a bot is called
    board = adHoc()
    boardCopy = adHoc()
    for player in playersSet:
        player.board = boardCopy
    
    numberOfPlayers = len(playersSet)
    board.numberOfPlayers = numberOfPlayers
    players = random.sample(list(playersSet), numberOfPlayers)
    
    
    # General case, games of less than 6 players not fully supported
    
    activePlayers = players[:]
    board.numberOfActivePlayers = len(activePlayers)
    
    ## If there are 4 or 5 players, 2 or 1 cards are placed on the table;
    ## in this case, the table plays a role of a dummy player
    ## who takes no actions and has no coins
       
    if (numberOfPlayers < 6):
      players.append(players, 'dummy')
      board.numberOfPlayers = 6
        
    # End of: general case, games of less than 6 players not fully supported
    
    board.playerCoins = [6] * board.numberOfActivePlayers
    board.coinsInCourthouse = 0
    
    # Permutation will every time mean permutation of cards i.e. cards possesed by every player
    board.cardsInPlay = cardSet
    # shuffle card names and assume this permutation as starting sequence [0, 1, 2, 3...]
    board.startingPermutationCards = random.sample(list(cardSet), numberOfPlayers)
    permutation = list(range(numberOfPlayers) 
    
    numberOfTurnsForSwapOnly = 4 # according to the rules
    eventNumber = 0 
    # Event is all what happens between the start of one player's action till start of the next player's action
    # Action is player's call on the beggining of his turn
    
    # For the sake of structure clarity class attributes are declared explicitly and therefore have to have values assigned
    
    class action:
        actionType = None # 'lookUp', 'swap', 'announce'
        cardToSwap = None # card number
        swapTrue = -2 # 0: false, 1: true, -2: undefined, unknown
        announcement = None # card announced if actionType is 'announce'
        
    
    class event:
        eventNumber = None
        playerActing = None
        eventAction = action()
        challengers = []
        cardsRevealed = [] # list of tuples (player number, card number)
        playerPerforming = None
        cardPerformance = adHoc() # how has the card owner used the card
        response = adHoc() # used for special cards as Spy and Inquisitor
        
    board.gameHistory = [] # list of events
    eventNumber = -1 # global event number  
    currentPlayer = -1
    board.playersRevealedLastTurn = [] #numbers of players
    gameWinner = None
    
    # game starts here
    while all(board.playerCoins > 0) and \
        all(board.playerCoins > 13) and \
        eventNumber < gameLength and \
        gameWinner == None:
        
        eventNumber += 1
        currentPlayer = (currentPlayer + 1) % numberOfPlayers
        if(players(currentPlayer) == 'dummy'):
            currentPlayer = 0
        # because we always put dummy players at the end
        
        actionMode = 'Regular'
        if turnNumber <= numberOfTurnsForSwapOnly:
            actionMode = 'Swap only'
        if currentPlayer in board.playersRevealedLastTurn:
            actionMode = 'Announcing banned'
        
        player = players[currentPlayer] # just making alias
        update(boardCopy, board)
        currentAction = player.Action(actionMode)

        
        # Checking action type
        if(actionMode == 'Swap only' and currentAction.actionType != 'swap'):
            errorLog.append("Player " + currentPlayer + " wants to perform " + currentAction.actionType + ", despite Swap only")
            currentAction = RandomSwap(currentPlayer, numberOfPlayers)
        if(actionMode == 'Announcing banned' and currentAction.actionType == 'announce'):
            errorLog.append("Player " + currentPlayer + " wants to announce, despite Announcing banned")
            currentAction = action()
            currentAction.actionType = 'lookUp'
            
                
        thisEvent = event()
        thisEvent.eventNumber = eventNumber
        thisEvent.actingPlayer = currentPlayer
        alteredAction = copy.deepcopy(currentAction)
        alteredAction.swapTrue = -2
        thisEvent.eventAction = alteredAction
            
        # additional check for correctness of announcing and swapping will go here
        # ...
        
        # Perform action
        if(currentAction.actionType == 'lookUp'):
            player.RecieveLookUp(currentPlayer, permutation[currentPlayer])
        if(currentAction.actionType == 'swap'):
            if(currentAction.swapTrue == True):
                SwapCards(permutation, currentPlayer, currentAction.cardToSwap)
        if(currentAction.actionType == 'announce'):
            # Here come the big guns
            board.challengers = [currentPlayer]
            cardIndex = board.startingPermutationCards.index(currentAction.announcement)
            
            # Ask all players
            # future improvement: maybe create function returning "range modulo"?
            
            for i in range(currentPlayer+1, numberOfPlayers):
                update(boardCopy, board)
                if(players[i] != 'dummy'):
                    if(players[i].Challenge()):
                        board.challengers.append(i)
            for i in range(0, currentPlayer):
                update(boardCopy, board)
                if(players[i] != 'dummy'):
                    if(players[i].Challenge()):
                        board.challengers.append(i)
        
            thisEvent.challengers = board.challengers[:]
            
            # check who performs the card's action... 
            # warning: nonsensical handling for paesant!
            
            if(board.challengers == [currentPlayer]):
                performingPlayer = currentPlayer
                board.performingPlayer = performingPlayer
            else:
                cardsRevealed = []
                # all cards get revealed
                for player in challengers:
                    cardsRevealed.append((player, permutation[player]))
                thisEvent.cardsRevealed = cardsRevealed[:]
                board.cardsRevealed = cardsRevealed[:]
                
                performingPlayer = None
                if(cardIndex in [permutation[x] for x in challengers]):
                    performingPlayer = permutation.index(cardIndex)
                thisEvent.performingPlayer = performingPlayer
                board.performingPlayer = performingPlayer
                    
                    
            # future improvement: turn card actions into function to allow for easy implementation of new cards
            
            # CARD ACTIONS
            
            board.thisEvent = thisEvent
            update(boardCopy, board)
            if(performingPlayer != None):
                if(currentAction.announcement == 'King'):
                    board.playerCoins[performingPlayer] += 3
                elif(currentAction.announcement == 'Queen'):
                    board.playerCoins[performingPlayer] += 2
                elif(currentAction.announcement  == 'Judge'):
                    board.playerCoins[performingPlayer] += board.coinsInCourthouse
                elif(currentAction.announcement  == 'Bishop'):
                    richest = [i for i in list(range(numberOfPlayers)) if board.playerCoins[i] == max(board.playerCoins)]
                    if(len(richest) == 1):
                        board.playerCoins[performingPlayer] += 2 # let's assume richest player has at least 2 coins
                        board.playerCoins[richest[0]] -= 2
                    else:
                        response = player[performingPlayer].Respond('Bishop', richest)
                        thisEvent.response = response
                        # now comes a check
                        if response.target in richest:
                            board.playerCoins[performingPlayer] += 2
                            board.playerCoins[response.target] -= 2
                        else:
                            errorLog.append("Player " + performingPlayer + " chose wrong target on Bishop")
                            board.playerCoins[performingPlayer] += 2
                            board.playerCoins[richest[0]] -= 2
                elif(currentAction.announcement  == 'Fool'):
                    response = player[performingPlayer].Respond('Fool')
                    if(response.cardA != performingPlayer and response.cardB != performingPlayer):
                        if(response.swapTrue == 1):
                            SwapCards(permutation, response.cardA, response.cardB)
                        response.swapTrue = -2
                        board.playerCoins[performingPlayer] += 1
                    else:
                        errorLog.append("Player " + performingPlayer + " chose wrong targets on Fool")
                        
                    thisEvent.response = response
                elif(currentAction.announcement  == 'Thief'):
                    board.playerCoins[performingPlayer] += 2
                    board.playerCoins[(performingPlayer-1) % numberOfPlayers] -= 1
                    board.playerCoins[(performingPlayer+1) % numberOfPlayers] -= 1
                elif(currentAction.announcement  == 'Cheat'):
                    if(board.playerCoins[performingPlayer] >= 10):
                        gameWinner = performingPlayer
                elif(currentAction.announcement  == 'Witch'):
                    response = player[performingPlayer].Respond('Witch')
                    thisEvent.response = response
                    if(response.swapWith != None):
                        temp = board.playerCoins[performingPlayer]
                        board.playerCoins[performingPlayer] = board.playerCoins[response.swapWith]
                        board.playerCoins[response.swapWith] = temp
                elif(currentAction.announcement  == 'Spy'):
                    response = player[performingPlayer].Respond('Spy')
                    player[performingPlayer].RecieveLookUp(performingPlayer, permutation[performingPlayer])
                    player[performingPlayer].RecieveLookUp(response.target, permutation[response.target])
                    thisEvent.response = response
                    update(boardCopy, board)
                    swapTrue = player[performingPlayer].Respond('SpySwap')
                    # mind you: player has acces to boardCopy, which is copy of board, which has acces to thisEvent
                    if(swapTrue):
                        SwapCards(permutation, performingPlayer, response.target)
                    responseForEvent = response
                    responseForEvent.swapTrue = -2
                    thisEvent.response = responseForEvent
                elif(currentAction.announcement  == 'Peasant'):
                    arePeasants = [i for i in challengers if board.startingPermutationCards[permutation[i]] == 'Peasant']
                    if(len(challengers) == 1):
                        board.playerCoins[performingPlayer] += 1
                    elif(len(arePeasants) == 1):
                        board.playerCoins[arePeasants[0]] += 1
                    elif(len(arePeasants) == 2):
                        board.playerCoins[arePeasants[0]] += 2
                        board.playerCoins[arePeasants[1]] += 2
                elif(currentAction.announcement  == 'Inquisitor'):
                    response = player[performingPlayer].Respond('Inquisitor')
                    inqusition = player[response.target].Respond('Inquisition')
                    board.revealedCards.append((response.target, permutation[response.target]))
                    if(inqusition.answer != board.startingPermutationCards[permutation[response.target]]):
                        board.playerCoins[performingPlayer] += 4
                        board.playerCoins[response.target] -= 4
                    response.answer = inquisition.answer
                    thisEvent.response = response
                elif(currentAction.announcement  == 'Widow'):
                    board.playerCoins[performingPlayer] = max(10, board.playerCoins[performingPlayer])
                    
                update(boardCopy, board) # just to make sure
                
                # now come penalties for wrong announcement
                if(len(challengers) > 1):
                    wrongdoers = [i for i in challengers if board.startingPermutationCards[permutation[i]] != currentAction.announcement]
                    for wrongdoer in wrongdoers:
                        board.playerCoins[wrongdoer] -= 1
                        board.coinsInCourthouse += 1
                
    # check who won/tied
    
    if(eventNumber < gameLength):
        if(gameWinner == None):
            winners = [i for i in players if board.playerCoins[i] >= 13]
            if(winners == []):
                winners = [i for i in list(range(numberOfPlayers)) if board.playerCoins[i] == max(board.playerCoins)]
            if(len(winners) > 1):
                return 'tie', winners
            else:
                return 'win', winners
        else:
            return 'win', [gameWinner]
    else:
        return 'timeout', []
    
