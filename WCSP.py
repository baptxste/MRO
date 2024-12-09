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

n_cost_functions = 0

# Première contrainte
# Arité: 2
# Portée: i et i + n_stations
# Coût par défaut: 1000 (dure)

header = f"{instance} {n_variables} {dom_size}"
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
                costs_1[(j, k)] = penalty
            n_tuples += 1

    if n_zeros > len(costs_1.values()) - n_zeros:
        default_cost = 0
        costs_1 = {k: v for k, v in costs_1.items() if v == penalty}
    else:
        default_cost = penalty
        costs_1 = {k: v for k, v in costs_1.items() if v == 0}

    content += f"2 {i} {i+n_stations} {default_cost} {n_tuples}\n"
    for k, v in costs_1.items():
        content += f"{k[0]} {k[1]} {v}\n"

    n_cost_functions += 1


# Deuxième contrainte
#
# Il faut l'encoder en deux contraintes,
# l'une pour les emetteurs et l'autre pour les recepteurs
#
# Arité: 2
# Portée: x et y, après + n_interferences pour la 2eme
# Coût par défaut: 1000 (dure)
n_interferences = len(data["interferences"])
costs_2_e = {}
costs_2_r = {}
for interference in data["interferences"]:
    x, y, delta_xy = interference["x"], interference["y"], interference["Delta"]
    n_zeros_e = 0
    n_tuples_e = 0
    n_zeros_r = 0
    n_tuples_r = 0

    for i, a in enumerate(stations[x]["emetteur"]):
        for j, b in enumerate(stations[y]["emetteur"]):
            if abs(a - b) >= delta_xy:
                costs_2_e[(i, j)] = 0
                n_zeros_e += 1
            else:
                costs_2_e[(i, j)] = penalty
            n_tuples_e += 1

    if n_zeros_e > len(costs_2_e.values()) - n_zeros_e:
        default_cost = 0
        costs_2_e = {k: v for k, v in costs_2_e.items() if v == penalty}
    else:
        default_cost = penalty
        costs_2_e = {k: v for k, v in costs_2_e.items() if v == 0}

    content += f"2 {x} {y} {default_cost} {n_tuples_e}\n"
    for k, v in costs_2_e.items():
        content += f"{k[0]} {k[1]} {v}\n"

    n_cost_functions += 1

    for i, a in enumerate(stations[x]["recepteur"]):
        for j, b in enumerate(stations[y]["recepteur"]):
            if abs(a - b) >= delta_xy:
                costs_2_r[(i, j)] = 0
                n_zeros_r += 1
            else:
                costs_2_r[(i, j)] = penalty
            n_tuples_r += 1

    if n_zeros_r > len(costs_2_r.values()) - n_zeros_r:
        default_cost = 0
        costs_2_r = {k: v for k, v in costs_2_r.items() if v == penalty}
    else:
        default_cost = penalty
        costs_2_r = {k: v for k, v in costs_2_r.items() if v == 0}

    content += f"2 {x+n_interferences} {y+n_interferences} {default_cost} {n_tuples_r}\n"
    for k, v in costs_2_r.items():
        content += f"{k[0]} {k[1]} {v}\n"

    n_cost_functions += 1


# Troisième contrainte
#
# Il faut l'encoder en deux contraintes,
# l'une pour les emetteurs et l'autre pour les recepteurs
#
# Arité: 2
# Portée: x et y, après + n_liaisons pour la 2eme
# Coût par défaut: 1000 (dure)
n_liaisons = len(data["liaisons"])
costs_3_e = {}
costs_3_r = {}
for liaison in data["liaisons"]:
    x, y = liaison["x"], liaison["y"]

    n_zeros_e = 0
    n_tuples_e = 0
    n_zeros_r = 0
    n_tuples_r = 0

    for i, a in enumerate(stations[x]["emetteur"]):
        for j, b in enumerate(stations[y]["emetteur"]):
            if a == b:
                costs_3_e[(i, j)] = 0
                n_zeros_e += 1
            else:
                costs_3_e[(i, j)] = 100
            n_tuples_e += 1

    if n_zeros_e > len(costs_3_e.values()) - n_zeros_e:
        default_cost = 0
        costs_3_e = {k: v for k, v in costs_3_e.items() if v == penalty}
    else:
        default_cost = penalty
        costs_3_e = {k: v for k, v in costs_3_e.items() if v == 0}

    content += f"2 {x} {y} {default_cost} {n_tuples_e}\n"
    for k, v in costs_3_e.items():
        content += f"{k[0]} {k[1]} {v}\n"

    n_cost_functions += 1

    for i, a in enumerate(stations[x]["recepteur"]):
        for j, b in enumerate(stations[y]["recepteur"]):
            if a == b:
                costs_3_r[(i, j)] = 0
                n_zeros_r += 1
            else:
                costs_3_r[(i, j)] = 100
            n_tuples_r += 1

    if n_zeros_r > len(costs_3_r.values()) - n_zeros_r:
        default_cost = 0
        costs_3_r = {k: v for k, v in costs_3_r.items() if v == penalty}
    else:
        default_cost = penalty
        costs_3_r = {k: v for k, v in costs_3_r.items() if v == 0}

    content += f"2 {x+n_liaisons} {y+n_liaisons} {default_cost} {n_tuples_r}\n"
    for k, v in costs_3_r.items():
        content += f"{k[0]} {k[1]} {v}\n"

    n_cost_functions += 1

header += f" {n_cost_functions} 1000\n"

wcsp = header + content

print(wcsp)

try:
    output_filename = instance + ".wcsp"
    with open(output_filename, "w") as f:
        f.write(wcsp)

    print(f"WCSP written to {output_filename}")
except Exception as e:
    print(f"Error writing file: {e}")
