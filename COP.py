from pycsp3 import *
import json

with open('TP/test.json') as f:
    data = json.load(f)

n = len(data['stations'])

D = 0
for e in data['stations']:
    if max(e['emetteur']) or (e['recepteur']) > D :
        D = max([max(e['emetteur']), max(e['recepteur'])])

# x[i][j] fréquence de la station i à la station j 

x = VarArray(size=[n, n], dom=range(D))
satisfy(

for i, j in range(D):

# at least 2 corners of different colors for any rectangle inside the board
NValues(x[i1][j1], x[i1][j2], x[i2][j1], x[i2][j2]) > 1
for i1, i2 in combinations(n, 2) for j1, j2 in combinations(m, 2) )
minimize(
# minimizing the greatest used color index (and so, the number of colors)
Maximum(x)
)