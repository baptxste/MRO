from pycsp3 import *
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
solvers = ["ACE","Choco" ]
file_name = files_sorted[num_file]

with open(os.path.join(path,'TP/donnees_cop',file_name)) as file : 
    data = json.load(file)
print(f"Fichier en cours : {file_name}, contrainte : {objectif}")    

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


# choix de la contrainte
if objectif==1:
    minimize(NValues(fe + fr))
elif objectif==2:
    minimize(Sum(fe) + Sum(fr))
elif objectif==3:
    minimize(Maximum(fe + fr) - Minimum(fe + fr))



results = {
        "objectif": objectif,
        "system_info": get_system_info(),
        "solvers": {}
    }


for solver in solvers:
    t0 = time()
    # Résolution
    if solve(solver=solver, options="-t=60s"):  # solver="Choco", "ACE"
        t1 = time()
        results["solvers"][solver] = {
            "temps": t1 - t0,
            "nombre_stations": len(data["stations"]),
            "stations": []
        }
        for i in range(len(data["stations"])):
            station_info = {
                "station": i,
                "emetteur": fe[i].value,
                "recepteur": fr[i].value
            }
            results["solvers"][solver]["stations"].append(station_info)
    else:
        results["solvers"][solver] = {
            "message": "Pas de solution trouvée."
        }

    # Écriture dans un fichier JSON
    output_dir = "results_cop"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"result_{file_name.split('.json')[0]}_{objectif}.json")

    with open(output_file, 'w') as json_file:
        json.dump(results, json_file, indent=4)


    # déplacer l'instance xml
    os.makedirs("solver_file", exist_ok=True)
    source_xml = "test.xml"  # Nom du fichier XML généré par défaut
    output_file= f"solver_file/instance_{file_name.split('.json')[0]}_{objectif}
     .xml"
    shutil.move(source_xml, output_file)

