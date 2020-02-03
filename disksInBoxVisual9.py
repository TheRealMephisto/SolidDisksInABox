import disksInBox as util

import matplotlib.pyplot as plt
import numpy as np

import pandas as pd

L = 100
N = 1000
r = 0.5
a = 1 * r # for noP2 it was = 1

#plt.ion()
fig = plt.figure()
ax = fig.gca()
plt.xlim(0, L)
plt.ylim(0, L)

[state, d] = util.initDisksInBox(L, N, r)

dataToSave = []
firstTime = True
e = util.calculateEnergies(d, 2*r)

for k in range(0, 1000000):
    #print("k: ", k)
    x = []
    y = []

    for i in range(0, len(state)):
        x.append(state[i][0])
        y.append(state[i][1])

    if k % 10 == 0:
        fig.clf()
        ax = fig.gca()
        ax.set_aspect('equal', adjustable='box')
        circles = []
        for i in range(0, len(x)):
            circles.append(plt.Circle((x[i], y[i]), r, color='r'))
            ax.add_artist(circles[i])
        plt.xlim(0, L)
        plt.ylim(0, L)
        
        plt.title('Iteration: ' + str(k))
        plt.xlabel('x')
        plt.ylabel('y')
        #fig.show()
        filename = 'images/e9/' + str(k)+'.png'
        fig.savefig(filename)
    #plt.pause(0.0001)
    meanDistance = 0
    amountD = 0
    for m in range(0, len(d)):
        for n in range(0, len(d[m])):
            meanDistance += d[m][n]
            amountD += 1
    meanDistance /= amountD
    #meanDistances.append(meanDistance)
    MSD = 0
    for m in range(0, len(d)):
        for n in range(0, len(d[m])):
            MSD += (d[m][n] - meanDistance)**2
    MSD /= amountD
    #MSDs.append(MSD)
    dataToSave.append([meanDistance, MSD, sum(e)])
    if k % 10 == 0:
        print("k: ", k)
        df = pd.DataFrame(dataToSave, columns=["E[d]", "Var[d]", "Energy"])
        if firstTime:
            df.to_csv('e9.csv', index=False)
            firstTime = False
        else:
            df.to_csv('e9.csv', mode='a', index=False, header=False)
        dataToSave = []

    [state, d, e] = util.updateDisksInBox(state, d, e, L, N, r, a, 3)

input("Press Enter to finish ...")