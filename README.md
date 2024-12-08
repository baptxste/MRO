# Modélisation et résolution pour l'optimisation

Date de rendu du projet : dernière séance de MRO.

## Description

Le code `COP.py` fonctionne, le script `run.sh` permet de le faire tourner sur tous les fichiers d'entraînement
( on ne peut pas le faire directement dans le script python ca pause un problème avec les variables déjà enregistrées en mémoire, il faut relancer python à chaque fois). 

Le dossier `result_cop` contient tous les résultats pour chaque jeu de données, ainsi que les infos sur le pc qui les a résolu
( ca peut être utile pour faire une comparaisont valable), `solver_file` contient les fichiers des instances pour chacun des jeu de données. 
Dans `COP.py` ya un timeout dans le solveur, il faut vérifier si le code n'a pas un problème car pour certain fichier avec certaine contrainte ca n'aboutie jamais. 

Les fichiers dans `results_cop` sont structurés pour être chargé et faire un script d'analyse.

`VCSP.py` contient le code pour la deuxième partie, mais il faut encore changer quelques aspects:

1. Le traitement des dossiers est copié de la première partie, il faut peut-être changer quelques parties.
2. Les contraintes 2 et 3 ne sont peut-être pas encore correcte, il s'agit en ce moment que de l'idée générale.
3. On pourrait éventuellement changer `penalty` pour les contraintes dures, peut-être des valuers plus grandes (?)

## Rapport

Le rapport peut être généré par LaTeX dans le dossier `tex` en utilisant un script bash:

```bash
$ sh build.sh projet
```

Ce script construit un pdf à partir d'un fichier avec le nom du premier argument, en supprimant les fichiers auxilières.  

