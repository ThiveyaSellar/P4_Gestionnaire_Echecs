from models.tournament import Tournament
from models.match import Match
from models.round import Round
from models.player import Player


class Controller:

    def __init__(self, db, manager, view):
        # database
        self.db = db
        # models
        self.manager = manager
        # views
        self.view = view

    def get_player_data(self):
        # Récupérer les données du nouveau joueur
        # Les ajouter dans la base de données
        infos = self.view.prompt_for_player()
        if not infos:
            return
        # Ajouter le joueur dans la base de données
        # sérialiser le joueur
        serialized_player = {
            "last_name": infos["last_name"],
            "first_name": infos["first_name"],
            "birth_date": infos["birth_date"],
            "gender": infos["gender"],
            "rank": infos["rank"]
        }
        players_table = self.db.table('players')
        players_table.insert(serialized_player)

    def show_players(self):
        players_table = self.db.table('players')
        serialized_players = players_table.all() # À ordonner selon classement
        players = []
        for sp in serialized_players:
            player = Player(
                sp["last_name"],
                sp["first_name"],
                sp["birth_date"],
                sp["gender"],
                sp["rank"]
            )
            players.append(player)
        self.view.display_all_players(players)

    def update_player_rank(self, i, new_rank):
        players_table = self.db.table('players')
        players_table.update({'rank': new_rank}, doc_ids=[i])
        # Update automatique des classements des autres joueurs ?
        # Si deux joueurs ont le même classement

    def run(self):
        running = True
        while running:
            choice = int(self.view.display_main_menu())

            if choice == 1:
                # Gestion des joueurs
                option = int(self.view.display_player_management_options())
                if option == 1:
                    # Ajouter un nouveau joueur
                    new_player = True
                    while new_player:
                        self.get_player_data()
                        # Un autre joueur à insérer ?
                        new_player = self.view.ask_new_player()
                elif option == 2:
                    # Afficher tous les joueurs
                    self.show_players()
                    # Récupérer l'indice du joueur
                    i = self.view.get_player_index()
                    # Demander le nouveau classement
                    rank = self.view.get_new_rank()
                    # Modifier un joueur (son classement)
                    self.update_player_rank(i, rank) # Ici
                    # Afficher après la modification
                    self.show_players()
                elif option == 3:
                    # Afficher les joueurs selon le classement
                    self.show_players()
            elif choice == 2:
                # Quitter
                running = False
            '''elif choice == 2:
                # Nouveau tournoi
            elif choice == 3:
                # Rapports'''
            print("Hello")