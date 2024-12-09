#!/bin/bash

# Chemin vers le script Python
PYTHON_CMD="python3 WCSP.py"

# Nombre total d'exécutions (18 fichiers * 3 objectifs)
total=$((20))
current=1

# Fonction pour afficher l'état actuel
display_status() {
    echo "Exécution: Fichier $1 sur $total (Progression: $current sur $total)"
}

for num_file in $(seq 0 19); do
    display_status "$num_file"

    $PYTHON_CMD --num_file=$num_file
    
    current=$((current + 1))

    # Pause de 2 secondes
    sleep 2
done

# Afficher un message final
echo -e "Terminé."
