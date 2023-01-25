# import db
# import pprint
from models.tournament import Tournament
# from models.match import Match
from models.round import Round
from models.player import Player


class Controller:

    def __init__(self, database, manager, view):
        # database
        self.db = database
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

    def show_players_by_rank(self):
        players_table = self.db.table('players')
        serialized_players = players_table.all()  # À ordonner selon classement
        players_list = []
        for sp in serialized_players:
            p = Player(
                sp['last_name'],
                sp['first_name'],
                sp['birth_date'],
                sp['gender'],
                sp['rank']
            )
            players_list.append(p)
        players_list.sort(key=lambda x: x.rank)
        print("\nListe des joueurs par rang : ")
        for n in range(len(players_list)):
            print(
                f"{players_list[n].get_rank()} -- {players_list[n].get_last_name()} -- {players_list[n].get_first_name()}\n",
                end=""
            )
        print("\n")

    def show_players_by_name(self):
        players_table = self.db.table('players')
        serialized_players = players_table.all()  # À ordonner selon classement
        players_list = []
        for sp in serialized_players:
            p = Player(
                sp['last_name'],
                sp['first_name'],
                sp['birth_date'],
                sp['gender'],
                sp['rank']
            )
            players_list.append(p)
        players_list = sorted(players_list, key=lambda x: (x.last_name, x.first_name))
        print("\nListe des joueurs par ordre alphabétique : ")
        for n in range(len(players_list)):
            print(
                f"{players_list[n].get_rank()} -- {players_list[n].get_last_name()} -- {players_list[n].get_first_name()}\n", end = ""
            )
        print("\n")

    def show_tournament_players_by_name(self, players_list):
        players_list = sorted(players_list, key=lambda x: (x.last_name, x.first_name))
        print("\nListe des joueurs par ordre alphabétique : ")
        for n in range(len(players_list)):
            print(
                f"{players_list[n].get_rank()} -- {players_list[n].get_last_name()} -- {players_list[n].get_first_name()}\n", end = ""
            )
        print("\n")

    def show_tournament_players_by_rank(self, players_list):
        players_list.sort(key=lambda x: x.rank)
        print("\nListe des joueurs par rang : ")
        for n in range(len(players_list)):
            print(
                f"{players_list[n].get_rank()} -- {players_list[n].get_last_name()} -- {players_list[n].get_first_name()}\n",
                end=""
            )
        print("\n")


    def show_players_to_add(self, id_list):
        for id in id_list:
            # Afficher le joueur dont l'id correspond
            players_table = self.db.table('players')
            p = players_table.get(doc_id=id)
            print(
                f"{p.doc_id}     "
                f"{p['last_name']} "
                f"{p['first_name']} "
                f"({p['rank']})"
            )
        print()

    def show_tournaments(self, id_list):
        i = 1
        for id in id_list:
            # Afficher le tournoi dont l'id correspond
            tournaments_table = self.db.table('tournaments')
            t = tournaments_table.get(doc_id=id)
            print(
                # f"{t.doc_id}    "
                f"{i}    "
                f"{t['name']} "
                f"{t['date']} "
                f"{t['location']} "
            )
            i = i + 1
        print()

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
        # Récupérer tous les joueurs dans la table joueur
        players = self.db.table('players').all()
        players_id = []
        # Récupérer tous les id
        for p in players:
            players_id.append(str(p.doc_id))
        for p in range(tournament.NB_PLAYERS):
            # Montrer les joueurs
            self.show_players_to_add(players_id)
            # Demander l'id du joueur
            p_id = self.view.add_player(players_id)
            # Créer le joueur et l'ajouter au tournoi grâce à l'id
            p_id = int(p_id)
            tournament.add_player(
                Player(
                    players[p_id-1]['last_name'],
                    players[p_id-1]['first_name'],
                    players[p_id-1]['birth_date'],
                    players[p_id-1]['gender'],
                    int(players[p_id-1]['rank']),
                )
            )
            # Retirer de la liste des joueurs
            players_id.remove(str(p_id))

    def update_players_scores(self, tournament, round):
        for match in round.matchs:
            scores = self.view.get_scores(
                match.player_a.get_name(),
                match.player_b.get_name()
            )
            match.add_score(scores[0], scores[1])
            match.player_a.update_score(scores[0])
            match.player_b.update_score(scores[1])

    def save_tournament(self, tournament, tournament_id=None):
        # Sérialiser le tournoi pour l'insertion dans TinyDB
        serialized_tournament = tournament.serialize()
        # Récupérer la table tournoi
        tournament_table = self.db.table('tournaments')
        # S'il n'y a pas de id associé au tournoi
        # Il n'existe pas et donc on l'insère
        # Sinon on update
        if tournament_id is None:
            tournament_table.insert(serialized_tournament)
        else:
            # item = tournament_table.update({str(tournament_id) : "serialized_tournament"}, doc_ids=[tournament_id])
            tournament_table.remove(doc_ids=[tournament_id])
            tournament_table.insert(serialized_tournament)

    def run_tournament(self, tournament):
        # Le tournoi est en cours
        play = True
        # Si aucun tour a été joué lancé le tour 1
        if tournament.remaining_rounds == tournament.NB_ROUNDS:
            # Demander le nom du premier tour
            round_name = self.view.ask_round_name()
            # Créer le premier tour et afficher les matchs
            round = tournament.prepare_round_one(round_name)
            round.show_status()
            # Terminer le tour
            self.view.ending_round()
            round.stop_round()
            round.show_status()
            # Saisir les scores
            self.update_players_scores(tournament, round)
            # Ajouter le tour au tournoi
            tournament.add_round(round)
            # Demander si on continue
            play = self.view.ask_continuing()

        while play and tournament.has_remaining_rounds():
            # Demander le nom du round
            round_name = self.view.ask_round_name()
            # Créer le tour et afficher les matchs
            round = tournament.prepare_next_round(round_name)
            round.show_status()
            # Terminer le tour
            self.view.ending_round()
            round.stop_round()
            round.show_status()
            # Saisir les scores
            self.update_players_scores(tournament, round)
            # Ajouter le tour au tournoi
            tournament.add_round(round)
            # S'il reste des tours demander si on continue
            if tournament.has_remaining_rounds():
                play = self.view.ask_continuing()

        # Afficher le statut
        if not play and tournament.has_remaining_rounds():
            print("Tournoi en pause")
        elif not tournament.has_remaining_rounds():
            final_ranking = self.view.end_tournament(tournament)
            tournament.update_ranking(final_ranking)



    def run(self):
        running = True
        while running:
            # Menu principal
            choice = int(self.view.display_main_menu())
            if choice == 1:
                # Sous-menu : Gestion des joueurs
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
                # Créer le tournoi
                tournament = self.create_tournament()
                '''if not tournament.has_remaining_rounds():
                    tournament.clear_all()'''
                tournament.clear_all()
                # Ajouter 8 joueurs au tournoi créé
                self.add_players(tournament)
                # Demander si on commence le tournoi
                start = self.view.ask_starting()
                # Si oui commence sinon retour au menu principal
                if start:
                    self.run_tournament(tournament)
                    # Enregistrer l'état du tournoi
                    self.save_tournament(tournament)
                else:
                    print("Tournoi en pause")
                    # Sauvegarder l'état du tournoi
                    self.save_tournament(tournament)
                    # Retour au menu principal
            elif choice == 3:
                # Reprendre le tournoi
                print("Reprendre le tournoi")
                # Récupérer les tournois dans la base de données
                # Afficher les tournois avec leurs ids
                tournaments = self.db.table('tournaments').all()
                if len(tournaments) != 0:
                    tournaments_id = []
                    # Récupérer tous les id
                    for t in tournaments:
                        tournaments_id.append(str(t.doc_id))
                    # Montrer les tournois
                    self.show_tournaments(tournaments_id)
                    # Demander l'id du tournoi
                    t_id = self.view.choose_tournament(tournaments_id)
                    t_id = int(t_id)
                    rounds = []
                    for round in tournaments[t_id - 1]['rounds']:
                        rounds.append(Round.deserialize_round(round))
                    players = []
                    for player in tournaments[t_id - 1]['players']:
                        players.append(Player.deserialize_player(player))
                    tournament = Tournament(
                            tournaments[t_id - 1]['name'],
                            tournaments[t_id - 1]['location'],
                            tournaments[t_id - 1]['date'],
                            tournaments[t_id - 1]['time_control'],
                            tournaments[t_id - 1]['description'],
                            int(tournaments[t_id - 1]['nb_rounds']),
                            int(tournaments[t_id - 1]['remaining_rounds']),
                            rounds,
                            players,
                            tournaments[t_id - 1]['ranking']
                        )
                    print(tournament)
                    # Continuer
                    self.run_tournament(tournament)
                    self.save_tournament(tournament, t_id)
                else:
                    print("Aucun tournoi en cours ...")
            elif choice == 4:
                # Liste de rapports
                print("Liste des rapports")
                """
                Rapports :

                • Liste de tous les acteurs:
                    ◦ par ordre alphabétique
                    ◦ par classement.
                • Liste de tous les joueurs d'un tournoi:
                    ◦ par ordre alphabétique
                    ◦ par classement.
                • Liste de tous les tournois.
                • Liste de tous les tours d'un tournoi.
                • Liste de tous les matchs d'un tournoi.

                """
                selection = self.view.select_report()
                if selection == 1:
                    self.show_players_by_name()
                elif selection == 2:
                    self.show_players_by_rank()
                elif selection == 3:
                    # Afficher les tournois
                    # Récupérer le tournoi
                    tournaments = self.db.table('tournaments').all()
                    if len(tournaments) != 0:
                        tournaments_id = []
                        # Récupérer tous les id
                        for t in tournaments:
                            tournaments_id.append(str(t.doc_id))
                        # Montrer les tournois
                        self.show_tournaments(tournaments_id)
                        # Demander l'id du tournoi
                        t_id = self.view.choose_tournament(tournaments_id)
                        t_id = int(t_id)
                        players_list = []
                        for player in tournaments[t_id - 1]['players']:
                            players_list.append(Player.deserialize_player(player))
                        self.show_tournament_players_by_name(players_list)
                    else:
                        print("Aucun tournoi disponible ...")
                elif selection == 4:
                    # Afficher les tournois
                    # Récupérer le tournoi
                    tournaments = self.db.table('tournaments').all()
                    if len(tournaments) != 0:
                        tournaments_id = []
                        # Récupérer tous les id
                        for t in tournaments:
                            tournaments_id.append(str(t.doc_id))
                        # Montrer les tournois
                        self.show_tournaments(tournaments_id)
                        # Demander l'id du tournoi
                        t_id = self.view.choose_tournament(tournaments_id)
                        t_id = int(t_id)
                        players_list = []
                        for player in tournaments[t_id - 1]['players']:
                            players_list.append(Player.deserialize_player(player))
                        self.show_tournament_players_by_rank(players_list)
                    else:
                        print("Aucun tournoi disponible ...")
                elif selection == 5:
                    tournaments = self.db.table('tournaments').all()
                    if len(tournaments) != 0:
                        tournaments_id = []
                        # Récupérer tous les id
                        for t in tournaments:
                            tournaments_id.append(str(t.doc_id))
                        # Montrer les tournois
                        self.show_tournaments(tournaments_id)
                    else:
                        print("Aucun tournoi ...")
                elif selection == 6:
                    print("Affichage des tours d'un tournoi")


            elif choice == 5:
                # Quitter
                running = False
