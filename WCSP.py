import json
import os
from time import time
import re
import platform
import psutil
import shutil
import argparse

parser = argparse.ArgumentParser(description="Script pour résoudre un problème WCSP.")
parser.add_argument("--num_file", type=int, nargs='?', default=0 , help="Index du fichier JSON à utiliser dans files_sorted")
parser.add_argument("--objectif", type=int, nargs='?', default=-1 , choices=[-1, 1, 2, 3], help="Objectif à minimiser (1, 2 ou 3)")
args = parser.parse_args()

def get_system_info():
    system_info = {
        "machine": platform.machine(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "processor": platform.processor(),
        "architecture": platform.architecture(),
        "ram": round(psutil.virtual_memory().total / (1024 ** 2)),  # En Mo
        "cpu_cores": psutil.cpu_count(logical=True),
        }
    return system_info

path = os.path.dirname(os.path.abspath(__file__))

# len(files_sorted)= 19
files_sorted = [
    "celar_50_7_10_5_0.800000_0.json",
    "celar_50_7_10_5_0.800000_1.json",
    "celar_50_7_10_5_0.800000_6.json",
    "celar_50_7_10_5_0.800000_7.json",
    "celar_50_7_10_5_0.800000_8.json",
    "celar_150_13_15_5_0.800000_2.json",
    "celar_150_13_15_5_0.800000_26.json",
    "celar_150_13_15_5_0.800000_28.json",
    "celar_150_13_15_5_0.800000_29.json",
    "celar_150_13_15_5_0.800000_8.json",
    "celar_250_25_15_5_0.820000_20.json",
    "celar_250_25_15_5_0.820000_22.json",
    "celar_250_25_15_5_0.820000_5.json",
    "celar_250_25_15_5_0.820000_7.json",
    "celar_250_25_15_5_0.820000_9.json",
    "celar_500_30_20_5_0.870000_24.json",
    "celar_500_30_20_5_0.870000_29.json",
    "celar_500_30_20_5_0.870000_45.json",
    "celar_500_30_20_5_0.870000_48.json"
]

num_file = args.num_file
objectif = args.objectif
# solvers = ["ACE","Choco" ]
file_name = files_sorted[num_file]

with open(os.path.join(path,'TP/donnees_wcsp', file_name)) as file: 
    data = json.load(file)
print(f"Fichier en cours : {file_name}, contrainte : {objectif}")

stations = data["stations"]
n_stations = len(stations)

instance = "StationsProblem"
n_variables = 2*n_stations
dom_size = 0
penalty = 1000

max_e = 0
max_r = 0
for s in stations:
    if len(s["emetteur"]) > max_e:
        max_e = len(s["emetteur"])
    if len(s["recepteur"]) > max_r:
        max_r = len(s["recepteur"])

dom_size = max(max_e, max_r)

domain_sizes_fe = [len(station["emetteur"]) for station in stations]
domain_sizes_fr = [len(station["recepteur"]) for station in stations]

# Première contrainte
# Arité: 2
# Portée: i et i + n_stations
# Coût par défaut: 1000 (dure)

content = ""
costs_1 = {}
for i, station in enumerate(stations):
    delta_i = station["delta"]

    n_zeros = 0
    n_tuples = 0
    for j, a in enumerate(stations[i]["emetteur"]):
        for k, b in enumerate(stations[i]["recepteur"]):
            d = abs(a - b)
            if d == delta_i:
                costs_1[(j, k)] = 0
                n_zeros += 1
            else:
                costs_1[(j, k)] = abs(delta_i - d)
            n_tuples += 1

    if n_zeros > len(costs_1.values()) - n_zeros:
        default_cost = 0
        costs_1 = {k: v for k, v in costs_1.items() if v == penalty}
    else:
        default_cost = penalty
        costs_1 = {k: v for k, v in costs_1.items() if v == 0}

    content += f"1 {i} {i+n_stations} {default_cost} {n_tuples}\n"
    for k, v in costs_1.items():
        content += f"{k[0]} {k[1]} {v}\n"

print(content)
assert 0

for interference in data["interferences"]:
    x, y, delta_xy = interference["x"], interference["y"], interference["Delta"]

    ListConstraintsFe = []
    for a in stations[x]["emetteur"]:
        for b in stations[y]["emetteur"]:
            if abs(a - b) >= delta_xy:
                ListConstraintsFe.append(0)
            else:
                ListConstraintsFe.append(penalty)

    # Problem.AddFunction([f"fe_{x}", f"fe_{y}"], ListConstraintsFe)

    ListConstraintsFr = []
    for a in stations[x]["recepteur"]:
        for b in stations[y]["recepteur"]:
            if abs(a - b) >= delta_xy:
                ListConstraintsFr.append(0)
            else:
                ListConstraintsFr.append(penalty)

    # Problem.AddFunction([f"fr_{x}", f"fr_{y}"], ListConstraintsFr)

# Contrainte 4 (souple)
for liaison in data["liaisons"]:
    x, y = liaison["x"], liaison["y"]

    # fe[x] == fe[y]
    fe_costs = []
    fe_domain_x = stations[x]["emetteur"]
    fe_domain_y = stations[y]["emetteur"]

    for val_x in fe_domain_x:
        for val_y in fe_domain_y:
            if val_x == val_y:
                fe_costs.append(0)
            else:
                fe_costs.append(penalty)

    # Problem.AddFunction([f"fe_{x}", f"fe_{y}"], fe_costs)

    # fr[x] == fr[y]
    fr_costs = []
    fr_domain_x = stations[x]["recepteur"]
    fr_domain_y = stations[y]["recepteur"]

    for val_x in fr_domain_x:
        for val_y in fr_domain_y:
            if val_x == val_y:
                fr_costs.append(0)
            else:
                fr_costs.append(penalty)

    # Problem.AddFunction([f"fr_{x}", f"fr_{y}"], fr_costs)
