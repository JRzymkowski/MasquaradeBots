import superposition.py

#turning superposition into predictor classes

class predictorExpectSwap(superposition):
    def swap(self, cards):
        super().swap(cards, 0.8)

class predictorBaseline(superposition):
    def swap(self, cards):
        super().swap(cards, 0.5)
        
class predictorConstantSwapProbability(superposition):
    def __init__(self, playersNumber, swapProbability):
        super().__init__(playersNumber)
        self.swapProbability = swapProbability
        
    def swap(self, cards):
        super().swap(cards, self.swapProbability)
   
#test
cards = predictorConstantSwapProbability(playersNumber,0.7)

cards.swap([0,1])
cards.swap([0,3])
cards.swap([4,6])
cards.reveal(0, 0)
cards.swap([5,6])

#enviornament for testing prediction accuracy

predictors = [baseline(playersNumber), justReveal(playersNumber), predictorConstantSwapProbability(playersNumber, 0.3),
              predictorConstantSwapProbability(playersNumber, 0.5), predictorConstantSwapProbability(playersNumber, 0.8)]
names = ["baseline", "justReveal", "swap 0.3", "swap 0.5", "swap 0.8"]

predictorNames = {}

#mostProbable = []
brierScore = {}
#logLossScore = []

for index, pred in enumerate(predictors):
    predictorNames[pred] = names[index]
    brierScore[pred] = 0

numberOfGames = 5
gameLength = 5
swapOccurence = 0.75 #else reveal random card
swapHappensProbability = 0.5


for i in range(numberOfGames):
    
    
    for pred in predictors:
        pred.reset()
    
    permutation = list(range(playersNumber))
    swaps = []
    for j in range(gameLength):
        #choose action
        if(random.random() < swapOccurence):
            cardA = random.randint(0, playersNumber-1)
            nextCard = random.randint(1, playersNumber-1)
            cardB = (cardA + nextCard) % playersNumber #so card is not swapped with itself
            action = {"type" : "swap", "cards" : [cardA, cardB]}
            if(random.random() < swapHappensProbability):
                temp = permutation[cardA]
                permutation[cardA] = permutation[cardB]
                permutation[cardB] = temp
                swaps.append((cardA, cardB))
        else:
            player = random.randint(0, playersNumber-1)
            action = {"type" : "reveal", "player" : player}
            
        #update predictors
        if(action["type"] == "swap"):
            for pred in predictors:
                pred.swap(action["cards"])
        elif(action["type"] == "reveal"):
            for pred in predictors:
                if(pred.reveal(action["player"], permutation[action["player"]]) == "error"):
                    print(permutation, action["player"], permutation[action["player"]])
                    print(swaps)
                    permutation2 = list(range(playersNumber))
                    for s in swaps:
                        temp = permutation2[s[0]]
                        permutation2[s[0]] = permutation2[s[1]]
                        permutation2[s[1]] = temp
                    print(permutation2)
        
        #gather scores
        #Brier score
        for pred in predictors:
            stepScore = 0
            belief = pred.belief()
            for k in range(playersNumber):
                for l in range(playersNumber):
                    if(permutation[k] == l):
                        stepScore += (1-belief[k][l])**2
                    else:
                        stepScore += belief[k][l]**2
            brierScore[pred] += stepScore
        
for pred in predictors:
    print(predictorNames[pred], brierScore[pred]/numberOfGames/gameLength)
