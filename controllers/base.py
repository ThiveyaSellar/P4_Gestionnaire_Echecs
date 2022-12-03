import db
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

    def show_players2(self):
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

    def show_players(self):
        players_table = self.db.table('players')
        serialized_players = players_table.all() # À ordonner selon classement
        for sp in serialized_players:
            print(f"{sp.doc_id}     {sp['last_name']} {sp['first_name']} ({sp['rank']})")

    def update_player_rank(self):
        # Récupérer le nom et prénom du joueur
        i = self.view.get_player_index()
        # Vérifier que le i est bien dans la bd sinon redemander
        # Demander le nouveau classement
        rank = self.view.get_new_rank()
        players_table = self.db.table('players')
        # À résoudre
        players_table.update({'rank': rank}, doc_ids=[i])
        # Update automatique des classements des autres joueurs ?
        # Si deux joueurs ont le même classement

    def create_tournament(self):
        infos = self.view.get_tournament_infos()
        tournament = Tournament(
            infos["name"],
            infos["location"],
            infos["date"],
            infos["time_control"],
            infos["description"]
        )
        return tournament

    def add_players(self, tournament):
        # Récupérer tous les id dans la table joueur
        players = self.db.table('players').all()
        players_id = []
        for p in players:
            players_id.append(str(p.doc_id))
        for p in range(tournament.NB_PLAYER):
            # Demander l'id du joueur
            p_id = self.view.add_player(players_id)
            # Créer le joueur et l'ajouter au tournoi grâce à l'id
            p_id = int(p_id)
            tournament.add_player(
                Player(
                    players[p_id]['last_name'],
                    players[p_id]['first_name'],
                    players[p_id]['birth_date'],
                    players[p_id]['gender'],
                    int(players[p_id]['rank']),
                )
            )
            # Retirer de la liste des joueurs
            players_id.remove(str(p_id))
        tournament.sort_players()
        tournament.show_players()

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
                    # Modifier un joueur (son classement)
                    self.update_player_rank()
                    # Afficher après la modification
                    self.show_players()
                elif option == 3:
                    # Afficher les joueurs selon le classement
                    self.show_players()
            elif choice == 2:
                # Nouveau tournoi
                # Demander les infos sur le tournoi
                tournament = self.create_tournament()
                # Afficher la liste des joueurs
                self.show_players()
                # Ajouter 8 joueurs
                self.add_players(tournament)

            elif choice == 3:
                # Rapports'''
                print("Rapports")
            elif choice == 4:
                # Quitter
                running = False