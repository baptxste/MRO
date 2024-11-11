#!/bin/bash

# Chemin vers le script Python
PYTHON_CMD="/home/baptiste/micromamba/envs/cours/bin/python3.10 /home/baptiste/Documents/cours/MRO/COP.py"

# Nombre total d'exécutions (18 fichiers * 3 objectifs)
total=$((3 * 18))
current=1

# Fonction pour afficher l'état actuel
display_status() {
    echo "Exécution: Fichier $1, Objectif $2 sur $total (Progression: $current sur $total)"
}

# Boucle sur chaque numéro de fichier de 0 à 18
for num_file in {0..18}; do
    # Boucle sur chaque objectif (1, 2, et 3)
    for objectif in {1..3}; do
        # Afficher l'état actuel
        display_status "$num_file" "$objectif"

        # Exécuter la commande avec le numéro de fichier et l'objectif actuels
        $PYTHON_CMD --num_file=$num_file --objectif=$objectif
        
        # Mise à jour de la progression
        current=$((current + 1))

        # Pause de 2 secondes
        sleep 2
    done
done

# Afficher un message final
echo -e "Terminé."
