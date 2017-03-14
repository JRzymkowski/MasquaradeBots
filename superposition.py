# introduces class superposition, which represents beliefs about card placement in form of superposition of possible card positions
# class superpositionOld is old version of superposition, I left it as it's code is clearer. 
# however it's not optimized and might pose problem for large players numbers
# use of superposition is strongly suggested

# on initialization, superposition takes one argument - players number
# methods of superposition:
#   setPlacement(permutation) - permutation is list representing cards of players; sets cards placement
#   reset(); resets the superposition, same as setPlacement([0,1,2,3,...])
#   swap(cards, probability) - cards is a tuple of player numbers, whose cards are being swapped, 
#   probability is subjetive probability of swap; 


import itertools as it
import numpy as np

playersNumber = 7
class superpositionOld:
    def __init__(self, playersNumber):
        self.playersNumber = playersNumber
        self.possiblePermutations = list(it.permutations(range(playersNumber))) #[0,2,3,1] means player 0 has card 0, player 1 has card 2, etc.
        
        #dictionary with tuples as keys
        #because lists can't be keys in Python, because why would Python lists behave in any way reasonable ever
        #and yes, if you want to modify a tuple, you need to convert it into list, modify the list and then convert it back into tuple
        #and bear in mind that almost everything can be dictionary key in Python
        #heck, I could put numpy as a dictionary key and Python would be okey with that
        #but not lists, nope
        self.cardPlacementSuperposition = {}
        for p in possiblePermutations:
            self.cardPlacementSuperposition[tuple(p)] = 0
            
        self.cardPlacementSuperposition[tuple(range(playersNumber))] = 1 #initialy card placement is [0,1,2,3...]
    
    def setPlacement(self, placement):
        self.cardPlacementSuperposition = {}
        self.cardPlacementSuperposition[tuple(placement)] 
    
    def permutationToMatrix(self, permutation):
        #columns are players, rows are cards
        #matrix represents card placement, not probability
        matrix = np.zeros((self.playersNumber, self.playersNumber))
        for i, p in enumerate(permutation):
            matrix[i][p] = 1
        return matrix
    
    def belief(self):
        #columns are players, rows are cards
        #matrix represents probability of owning card
        belief = np.zeros((self.playersNumber, self.playersNumber))
        for permutation, probability in self.cardPlacementSuperposition.items():
            belief += probability*permutationToMatrix(permutation)
        return belief
        
    def swap(self, cards, subjectiveProbability):
        newSuperposition = {}
        for p in self.possiblePermutations:
            newSuperposition[tuple(p)] = 0
        for permutation, probability in self.cardPlacementSuperposition.items():
            if(probability != 0):
                tempPermutation = list(permutation)
                tempValue = tempPermutation[cards[0]]
                tempPermutation[cards[0]] = tempPermutation[cards[1]]
                tempPermutation[cards[1]] = tempValue
                newPermutation = tuple(tempPermutation)
                
                newSuperposition[newPermutation] += probability*subjectiveProbability
                newSuperposition[permutation] += probability*(1-subjectiveProbability)
        self.cardPlacementSuperposition = dict(newSuperposition)
    
    def reveal(self, player, card):
        newSuperposition = {}
        for p in self.possiblePermutations:
            newSuperposition[tuple(p)] = 0
        probabilitySum = 0
        for permutation, probability in self.cardPlacementSuperposition.items():
            if(permutation[player] == card):
                newSuperposition[permutation] = probability
                probabilitySum += probability
        if probabilitySum == 0:
            print("Error, impossible situation")
            self.cardPlacementSuperposition = {}
        else:
            for p in self.possiblePermutations:
                newSuperposition[tuple(p)] /= probabilitySum
            self.cardPlacementSuperposition = dict(newSuperposition)

### end of class definition

class superposition:
    #class superposition optimized for sparse probablity vector, i.e. most of permutation has probablity 0
    def __init__(self, playersNumber):
        self.playersNumber = playersNumber
        
        #dictionary with tuples as keys
        #because lists can't be keys in Python, because why would Python lists behave in any way reasonable ever
        #and yes, if you want to modify a tuple, you need to convert it into list, modify the list and then convert it back into tuple
        self.cardPlacementSuperposition = {}          
        self.cardPlacementSuperposition[tuple(range(playersNumber))] = 1 #initialy card placement is [0,1,2,3...]
    
    def setPlacement(self, placement):
        self.cardPlacementSuperposition = {}
        self.cardPlacementSuperposition[tuple(placement)] = 1
        
    def reset(self):
        self.setPlacement(range(self.playersNumber))
    
    def permutationToMatrix(self, permutation):
        #columns are players, rows are cards
        #matrix represents card placement, not probability
        matrix = np.zeros((self.playersNumber, self.playersNumber))
        for i, p in enumerate(permutation):
            matrix[i][p] = 1
        return matrix
    
    def belief(self):
        #columns are players, rows are cards
        #matrix represents probability of owning card
        belief = np.zeros((self.playersNumber, self.playersNumber))
        for permutation, probability in self.cardPlacementSuperposition.items():
            belief += probability*self.permutationToMatrix(permutation)
        return belief
        
    def swap(self, cards, subjectiveProbability):
        newSuperposition = {}
        for permutation, probability in self.cardPlacementSuperposition.items():
            if(probability != 0):
                tempPermutation = list(permutation)
                tempValue = tempPermutation[cards[0]]
                tempPermutation[cards[0]] = tempPermutation[cards[1]]
                tempPermutation[cards[1]] = tempValue
                newPermutation = tuple(tempPermutation)
                
                if(newPermutation in newSuperposition):
                    newSuperposition[newPermutation] += probability*subjectiveProbability
                else:
                    newSuperposition[newPermutation] = probability*subjectiveProbability
                if(permutation in newSuperposition):
                    newSuperposition[permutation] += probability*(1-subjectiveProbability)
                else:
                    newSuperposition[permutation] = probability*(1-subjectiveProbability)
        self.cardPlacementSuperposition = dict(newSuperposition)
    
    def reveal(self, player, card):
        newSuperposition = {}
        probabilitySum = 0
        for permutation, probability in self.cardPlacementSuperposition.items():
            if(permutation[player] == card):
                newSuperposition[permutation] = probability
                probabilitySum += probability
        if probabilitySum == 0:
            print("Error, impossible situation")
            print(player, card)
            print(self.belief())
            self.cardPlacementSuperposition = {}
            return "error"
        else:
            for p in newSuperposition:
                newSuperposition[p] /= probabilitySum
            self.cardPlacementSuperposition = dict(newSuperposition)
            
    def __rmul__(self, coefficient):
        newSuperposition = {}
        for permutation, probability in self.cardPlacementSuperposition.items():
            newSuperposition[permutation] = probability*coefficient
        selfCopy = superpositionOpt(self.playersNumber)
        selfCopy.cardPlacementSuperposition = newSuperposition
        return selfCopy
    
    def __add__(self, element):
        newSuperposition = {}
        allPermutation = set().union(*[self.cardPlacementSuperposition,element.cardPlacementSuperposition])
        for p in allPermutation:
            probability = 0
            if(p in self.cardPlacementSuperposition):
                probability += self.cardPlacementSuperposition[p]
            if(p in element.cardPlacementSuperposition):
                probability += element.cardPlacementSuperposition[p]
            newSuperposition[p] = probability
        selfCopy = superpositionOpt(self.playersNumber)
        selfCopy.cardPlacementSuperposition = newSuperposition
        return selfCopy
    
    def probabilisticReveal(self, player, card, subjectiveProbability):
        afterReveal = superpositionOpt(self.playersNumber)
        afterReveal.cardPlacementSuperposition = self.cardPlacementSuperposition
        afterReveal.reveal(player, card)
        self.cardPlacementSuperposition = (subjectiveProbability*afterReveal+(1-subjectiveProbability)*self).cardPlacementSuperposition
        
    def probabilisticRevealC(self, player, card, subjectiveProbability):
        afterReveal = superpositionOpt(self.playersNumber)
        afterReveal.cardPlacementSuperposition = self.cardPlacementSuperposition
        afterReveal.reveal(player, card)
        self.cardPlacementSuperposition = ( \
        sqrt(2)/(1+subjectiveProbability)*subjectiveProbability*afterReveal+ \
        (1-(subjectiveProbability*sqrt(2)/(1+subjectiveProbability)))*self).cardPlacementSuperposition
        
    def revealNot(self, player, card):
        newSuperposition = {}
        probabilitySum = 0
        for permutation, probability in self.cardPlacementSuperposition.items():
            if(permutation[player] != card):
                newSuperposition[permutation] = probability
                probabilitySum += probability
        if probabilitySum == 0:
            print("Error, impossible situation")
            print(player, card)
            print(self.belief())
            self.cardPlacementSuperposition = {}
            return "error"
        else:
            for p in newSuperposition:
                newSuperposition[p] /= probabilitySum
            self.cardPlacementSuperposition = dict(newSuperposition)
            
    def probabilisticRevealB(self, player, card, subjectiveProbability):
        afterReveal = superpositionOpt(self.playersNumber)
        afterReveal.cardPlacementSuperposition = self.cardPlacementSuperposition
        afterReveal.reveal(player, card)
        
        priorProbability = self.belief()[player, card]
        effectiveProbability = subjectiveProbability*0.5/(1-priorProbability)
        
        self.cardPlacementSuperposition = (effectiveProbability*afterReveal+(1-effectiveProbability)*self).cardPlacementSuperposition
    

### end of class superpositionOpt definition
