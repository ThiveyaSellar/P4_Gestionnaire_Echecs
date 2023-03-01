## P4 Gestionnaire de tournois échecs

Ce programme console hors ligne est un gestionnaire de tournois d'échecs.
Il permet la gestion des joueurs avec l'inscription d'un joueur dans la base de données et le changement de son classement.
Avec au moins 8 joueurs dans la base de données il est possible de créer un nouveau tournoi.
Les tournois peuvent être interrompus et repris plus tard. L'état du tournoi est sauvegardé dans la base de données.
Il est également possible d'afficher différents rapports sur les joueurs, les tournois, les tours et les matchs.

### Installation

La base de données TinyDB "chess_db.json" comporte actuellement au moins huit joueurs et il est possible d'en ajouter davantage.


```bash
# Cloner le dépôt distant
$ git clone https://github.com/ThiveyaSellar/P4_Gestionnaire_Echecs.git

# Créer un environnement virtuel
$ python -m venv env

# Activer l'environnement virtuel
$ source env/bin/activate

# Installer les paquets nécessaires à partir du fichier requirements.txt
$ pip install -r requirements.txt

# Lancer le gestionnaire de tournoi
$ python main.py

```

### Génération du rapport flake8-html

```bash
# Générer le rapport flake8 dans le répertoire "flake-report"
$ flake8 --format=html --htmldir=flake-report
```