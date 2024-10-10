from pycsp3 import *
import json

with open('TP/test.json') as f:
    data = json.load(f)

n = len(data['stations'])

# x[i][j] fréquence de la station i à la station j, il faut que tout xij soit égale à l'intersection des fréquences émetrices possibles de la station i et réceptrices de j

x = VarArray(size=[n, n], x = VarArray(size=[n, n], dom=lambda i, j: set(data['stations'][i]['emetteur']).intersection(data['stations'][j]['recepteur'])))
satisfy(

[abs(x[i][j] - x[k][i]) = data['stations'][i]['delta']
     for i in range(n)
     for j in range(n)
     for k in range(n) if j != k] #il faut que l'écart entre les fréquences émettrices xij et réceptrice xki de la station i soit égal à deltai


# at least 2 corners of different colors for any rectangle inside the board
NValues(x[i1][j1], x[i1][j2], x[i2][j1], x[i2][j2]) > 1
for i1, i2 in combinations(n, 2) for j1, j2 in combinations(m, 2) )
minimize(
# minimizing the greatest used color index (and so, the number of colors)
Maximum(x)
)