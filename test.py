from pycsp3 import *
import json
import os 

path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(path,'TP/donnees_cop/celar_50_7_10_5_0.800000_0.json')) as f:
    data = json.load(f)


# Variables
stations = data["stations"]
n_stations = len(stations)

# Variables pour les fréquences d'émission et de réception pour chaque station
fe = VarArray(size=n_stations, dom=lambda i: stations[i]["emetteur"])
fr = VarArray(size=n_stations, dom=lambda i: stations[i]["recepteur"])

# Contraintes
# 1. Contrainte sur l'écart delta entre émetteur et récepteur pour chaque station
for i, station in enumerate(stations):
    delta_i = station["delta"]
    satisfy(abs(fe[i] - fr[i]) == delta_i)

# 2. Contraintes de non-interférence pour les paires de stations proches
for interference in data["interferences"]:
    x, y, delta_xy = interference["x"], interference["y"], interference["Delta"]
    satisfy(abs(fe[x] - fe[y]) >= delta_xy)
    satisfy(abs(fr[x] - fr[y]) >= delta_xy)

# 3. Contraintes de nombre de fréquences différentes par région
for r, max_freqs in enumerate(data["regions"]):
    region_stations = [i for i, s in enumerate(stations) if s["region"] == r]
    if region_stations:
        satisfy(NValues([fe[i] for i in region_stations] + [fr[i] for i in region_stations]) <= max_freqs)

# Objectifs (Choisissez un seul objectif pour chaque exécution)
        
# Objectif 1 : Minimiser le nombre de fréquences différentes utilisées
# minimize(NValues(fe + fr))

# Objectif 2 : Minimiser les fréquences totales (utilisation des fréquences les plus basses)
# minimize(Sum(fe) + Sum(fr))

# Objectif 3 : Minimiser la largeur de la bande de fréquences
# minimize(Maximum(fe + fr) - Minimum(fe + fr))

# Résolution
if solve():
    print("Solutions trouvées :")
    for i in range(n_stations):
        print(f"Station {i}: émetteur = {fe[i].value}, récepteur = {fr[i].value}")
else:
    print("Pas de solution trouvée.")
