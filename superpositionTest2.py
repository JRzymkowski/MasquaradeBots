import superposition.py

dummy = superposition(playersNumber)
rozklady = {}
liczba = {}

swapHappensProbability = 0.5

def swap(permutation, cardA, cardB, probability):
    if(random.random() < probability):
        temp = permutation[cardA]
        permutation[cardA] = permutation[cardB]
        permutation[cardB] = temp
        
sekwencja = [(0,5), (3,4), (2,4), (2,6), (0,6), (0,2), 0, (3,4), (1,0), (2,3), (0,6), (5,1), (2,1), 3]
    

for i in range(100000):
    permutation = list(range(playersNumber))
    rev = []
    
    for s in sekwencja:
        if(type(s) is tuple):
            swap(permutation, s[0], s[1], swapHappensProbability)
        else:
            rev.append(permutation[s])
    
    if(tuple(rev) not in rozklady):
        rozklady[tuple(rev)] = dummy.permutationToMatrix(permutation)
        liczba[tuple(rev)] = 1
    else:
        rozklady[tuple(rev)] += dummy.permutationToMatrix(permutation)
        liczba[tuple(rev)] += 1

    
for r in rozklady:
    rozklady[r] = rozklady[r]/liczba[r]
        

przyklad = list(rozklady.keys())[random.randint(0, len(rozklady.keys())-1)]
print(przyklad)
print(liczba[przyklad])

nty = 0
        
for s in sekwencja:
    if(type(s) is tuple):
        dummy.swap(s, swapHappensProbability)
    else:
        dummy.reveal(s, przyklad[nty])
        nty += 1

np.set_printoptions(formatter={'float': '{: 0.3f}'.format})

print(rozklady[przyklad])
print()
print(dummy.belief())
