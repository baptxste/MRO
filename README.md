Date de rendu du projet : dernière séance de MRO.

https://datascientest.com/nlp-word-embedding-word2vec


Le code COP.py fonctionne, le script run.sh permet de le faire tourner sur tous les fichiers d'entraînement
( on ne peut pas le faire directement dans le script python ca pause un problème avec les variables déjà enregistrées en mémoire, il faut relancer python à chaque fois). 
Le dossier result_cop contient tous les résultats pour chaque jeu de données, ainsi que les infos sur le pc qui les a résolu
( ca peut être utile pour faire une comparaisont valable), solver_file contient les fichiers des instances pour chacun des jeu de données. 
Dans COP.py ya un timeout dans le solveur, il faut vérifier si le code n'a pas un problème car pour certain fichier avec certaine contrainte ca n'aboutie jamais. 

Les fichiers dans results_cop sont structurés pour être chargé et faire un script d'analyse.