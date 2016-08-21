class action:
        actionType = None # 'lookUp', 'swap', 'announce'
        cardToSwap = None # card number
        swapTrue = -2 # 0: false, 1: true, -2: undefined, unknown
        announcement = None # card announced if actionType is 'announce'
        
    
class event:
    eventNumber = None
    actingPlayer = None
    eventAction = action()
    challengers = []
    cardsRevealed = [] # list of tuples (player number, card number)
    performingPlayer = None
    cardPerformance = adHoc() # how has the card owner used the card
    response = adHoc() # used for special cards as Spy and Inquisitor
