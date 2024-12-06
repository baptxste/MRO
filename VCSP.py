from pytoulbar2 import CFN
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

with open(os.path.join(path,'TP/donnees_cop', file_name)) as file: 
    data = json.load(file)
print(f"Fichier en cours : {file_name}, contrainte : {objectif}")

stations = data["stations"]
n_stations = len(stations)

Problem = CFN()

for i in range(n_stations):
    emetteur_domain = stations[i]["emetteur"]
    recepteur_domain = stations[i]["recepteur"]

    Problem.AddVariable(f"fe_{i}", list(emetteur_domain))
    Problem.AddVariable(f"fr_{i}", list(recepteur_domain))

for i, station in enumerate(stations):
    delta_i = station["delta"]

    ListConstraints = []

    for a in stations[i]["emetteur"]:
        for b in stations[i]["recepteur"]:
            d = abs(a - b)
            if d == delta_i:
                ListConstraints.append(0)
            else:
                ListConstraints.append(delta_i - d)

    Problem.AddFunction([f"fe_{i}", f"fr_{i}"], ListConstraints)

res = Problem.Solve()
print(res)
