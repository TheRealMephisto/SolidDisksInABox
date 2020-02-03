
import numpy as np
import random
import math

'''
    A configuration x in |R^2N is represented by a list of N elements,
    where each element itself is a list containing the two coordinates of one particle,
    and where N is the total number of particles in the box.
    d describes a |R^(N x N) matrix containing the distance between particle i and j.
    It is sufficient to calculate the upper triangle,
    as the matrix is symmetric and the diagonal entries are zero.
    Therefore d is a |R^N vector containing the entries [(1, 0)], [(2, 0), (2, 1)], ...
    Therefore d is a |R^(N^2/2) vector containing the entries (1, 0), (2, 0), (2, 1), (3, 0)...
    Returns [-1] if x is not a valid configuration,
    i.e. that one distance is less than the disks radius.
'''
def getDistancesToXi(x, xi, r, L):
    d = []
    for j in range(0, len(x)):
        xshift = [-L, 0, L, -L, 0, L, -L, 0, L]
        yshift = [L, L, L, 0, 0, 0, -L, -L, -L]
        distance = math.sqrt(2)*L
        for k in range(0, 9):
            candidate = math.sqrt( ( xi[0] - ( x[j][0] + xshift[k] ) )**2 + ( xi[1] - ( x[j][1] + yshift[k] ) )**2 )
            distance = candidate if candidate < distance  else distance
        if distance >= 200:
            print("SOMETHINGSWRONG!!!")
        if distance <= 2*r:
            #print("distance too small: ", distance)
            return [-1]
        d.append(distance)
    return d

def calculateEnergy(d, i, rmin):
    energy = 0
    #boundary = len(d)
    #if i < len(d):
    #    boundary = len(d[i])
    for j in range(0, i): # go through d[i]
        energy += 5*((rmin/d[i-1][j])**12 - 2*(rmin/d[i-1][j])**6)
    for j in range(i, len(d)): # g through [d[j][i]]
        #print(j)
        #print("row j: ", j)
        energy += 5*((rmin/d[j][i])**12 - 2*(rmin/d[j][i])**6)
    return energy/2



'''
    Calculate the energy of a given state with distances d.
    Using simplified form of Lennard-Jones-Potential.
    rmin is the distance where V reaches minimal value -5.
'''
def calculateEnergies(d, rmin):
    e = []
    for i in range(0, len(d)+1):
        e.append(calculateEnergy(d, i, rmin))
        #for j in range(0, len(d[i])):
        #    energy += 5*((rmin/d[i][j])**12 - 2*(rmin/d[i][j])**6)
    return e

'''
    Initialise first starting position with given sidelength L of the 2D-Box and the total Number N
    of disks inside the box.
    Watch out not to put too much disks inside a too small box!
    Return state x
'''
def initDisksInBox(L, N, r):
    x = []
    distances = []
    for i in range(0, N):
        while len(x) == i:
            xi = [random.uniform(0, L), random.uniform(0, L)]
            DistancesToXi = getDistancesToXi(x, xi, r, L)
            if DistancesToXi != [-1]:
                x.append(xi)
                if DistancesToXi != []:
                    distances.append(DistancesToXi)

    return [x, distances]

'''
    Randomly choose a disk of the given state and move it randomly inside a box with sidelength a,
    e energy of current state
'''
def updateDisksInBox(x, d, e, L, N, r, a, T=1):

    origX = x[0:len(x)]
    origD = d[0:len(d)]

    i = random.randint(0, len(x)-1)
    origXi = x.pop(i)
    if i > 0:
        origDistancesToXi = d.pop(i-1)

    deltaXi = [random.uniform(-a, a), random.uniform(-a, a)]
    newXi = [ (origXi[0]+deltaXi[0]) % L, (origXi[1]+deltaXi[1]) % L ]

    DistancesToNewXi = getDistancesToXi(x, newXi, r, L)
    if DistancesToNewXi != [-1]:
        x.insert(i, newXi)
        for j in range(i, len(d)):
            d[j][i-1] = DistancesToNewXi[j]

        if i > 0:
            d.insert(i-1, DistancesToNewXi[0:i])

        origEofXi = e[i]
        newEofXi = calculateEnergy(d, i, 2*r)
        deltaE = newEofXi - origEofXi
        if deltaE < 0:
            e[i] = newEofXi
            #print("accepted because of improvement")
        else:
            u = random.uniform(0, 1)
            accProb = math.exp(-deltaE/T)
            #print("acceptance Probability: ", accProb)
            if u < accProb:
                e[i] = newEofXi
                #print("accepted")
            else:
                #print("Not accepted")
                x = origX
                d = origD
    else:
        #print("Not possible")
        x = origX
        d = origD

    return [x, d, e]
    

'''
    Check if any of the entries in d has radius less or equal the disks radius epsilon.
    Return true if that is not the case and false if it is.
'''
def isValid(d, epsilon):
    for i in range(0, len(d)):
        if d[i] <= epsilon:
            return False
    return True


if __name__ == "__main__":
    pass