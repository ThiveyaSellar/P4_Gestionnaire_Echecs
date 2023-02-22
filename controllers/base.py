# import db
# import pprint
from tinydb import where


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
        # Vérifier que le classement n'existe pas déjà dans la bd
        players_table = self.db.table('players')
        players_table_all = players_table.all()
        infos = self.view.prompt_for_player(players_table_all)
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

    @staticmethod
    def get_key(element):
        return element[0]

    def show_players(self):
        players_table = self.db.table('players')
        serialized_players = players_table.all()
        players = []
        for sp in serialized_players:
            players.append(
                (
                    sp.doc_id,
                    Player(
                        sp["last_name"],
                        sp["first_name"],
                        sp["birth_date"],
                        sp["gender"],
                        sp["rank"]
                    )
                )
            )
        players = sorted(
            players,
            key=Controller.get_key
        )
        self.view.show_list_of_players(players)

    def show_players_by_rank(self):
        players_table = self.db.table('players')
        serialized_players = players_table.all()
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

        self.view.show_players1(players_list, "rang")

    def show_players_by_name(self):
        players_table = self.db.table('players')
        serialized_players = players_table.all()
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
        players_list = sorted(
            players_list,
            key=lambda x: (x.last_name, x.first_name)
        )
        self.view.show_players1(players_list, "ordre alphabétique")

    def show_tournaments(self, id_list):
        i = 1
        tournaments_table = self.db.table('tournaments')
        for id_nb in id_list:
            # Afficher le tournoi dont l'id correspond
            t = tournaments_table.get(doc_id=id_nb)
            if t['finished']:
                statut = "terminé"
            else:
                statut = "en cours"
            tournament = Tournament.deserialize_tournament(t)
            self.view.show_tournament(i, tournament, statut)
            i = i + 1
        print()

    def update_player_rank(self):
        # Récupérer le nom et prénom du joueur
        i = self.view.get_player_index()
        # Vérifier que le i est bien dans la bd sinon redemander
        # Demander le nouveau classement
        players_table = self.db.table('players')
        players_table_all = players_table.all()
        rank = self.view.get_new_rank(players_table_all)
        players_table.update({'rank': rank}, doc_ids=[i])

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
            self.view.show_players_to_add(players, players_id)
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
            msg = players[p_id-1]['last_name'] + " est ajouté au tournoi. \n"
            self.view.show_message(msg)
            # Retirer de la liste des joueurs
            players_id.remove(str(p_id))

    def update_players_scores(self, round):
        for match in round.get_matchs():
            scores = self.view.get_scores(
                match.get_player_a().get_names(),
                match.get_player_b().get_names()
            )
            match.add_score(scores[0], scores[1])
            match.get_player_a().update_score(scores[0])
            match.get_player_b().update_score(scores[1])

    def save_tournament(self, tournament, tournament_id=None):
        # Sérialiser le tournoi pour l'insertion dans TinyDB
        serialized_tournament = tournament.serialize()
        # Récupérer la table tournoi
        tournament_table = self.db.table('tournaments')
        # S'il n'y a pas d'id associé au tournoi
        # Il n'existe pas et donc on l'insère
        # Sinon on met à jour
        if tournament_id is None:
            tournament_table.insert(serialized_tournament)
        else:
            '''
            item = tournament_table.update(
                {str(tournament_id) : "serialized_tournament"},
                doc_ids=[tournament_id]
            )'''
            tournament_table.remove(doc_ids=[tournament_id])
            tournament_table.insert(serialized_tournament)

    def run_tournament(self, tournament):
        # Le tournoi est en cours
        play = True
        # Si aucun tour a été joué lancé le tour 1
        if tournament.remaining_rounds == tournament.NB_ROUNDS:
            self.view.show_players(tournament)
            # Demander le nom du premier tour
            round_name = self.view.ask_round_name()
            # Créer le premier tour et afficher les matchs
            round = tournament.prepare_round_one(round_name)
            if round is None:
                self.view.show_message(
                    "Le nombre de joueurs doit être pair ..."
                )
            else:
                self.view.show_round_infos(round)
                # Terminer le tour
                self.view.ending_round()
                round.stop_round()
                self.view.show_round_status(round)
                # Saisir les scores
                self.update_players_scores(round)
                # Ajouter le tour au tournoi
                tournament.add_round(round)
                # Demander si on continue
                play = self.view.ask_continuing()

        while play and tournament.has_remaining_rounds():
            self.view.show_players(tournament)
            # Demander le nom du round
            round_name = self.view.ask_round_name()
            # Créer le tour et afficher les matchs
            round = tournament.prepare_next_round(round_name)
            self.view.show_round_infos(round)
            # Terminer le tour
            self.view.ending_round()
            round.stop_round()
            self.view.show_round_status(round)
            # Saisir les scores
            self.update_players_scores(round)
            # Ajouter le tour au tournoi
            tournament.add_round(round)
            # S'il reste des tours demander si on continue
            if tournament.has_remaining_rounds():
                play = self.view.ask_continuing()

        # Afficher le statut
        if not play and tournament.has_remaining_rounds():
            self.view.show_message("Tournoi en pause")
        elif not tournament.has_remaining_rounds():
            # Fin du tournoi
            # Trier des joueurs par rapport au dernier classement et
            tournament.sort_players()
            # Récupérer le dernier classement
            final_ranking = tournament.get_final_ranking()
            # Mettre à jour le classement final du tournoi
            tournament.update_ranking(final_ranking)
            # Marquer le tournoi comme terminé
            self.view.show_results(tournament.get_players()[0], final_ranking)
            tournament.set_finished()

    def show_all_tournaments(self):
        # Afficher les tournois
        tournaments = self.db.table('tournaments').all()
        if len(tournaments) != 0:
            tournaments_id = []
            # Récupérer tous les id
            for t in tournaments:
                tournaments_id.append(str(t.doc_id))
            # Montrer les tournois
            self.show_tournaments(tournaments_id)
            return tournaments, tournaments_id
        else:
            self.view.show_message("Aucun tournoi ...")
            tournaments_id = None
            return tournaments, tournaments_id

    def select_tournament(self):
        tournaments, tournaments_id = self.show_all_tournaments()
        if tournaments_id is not None:
            # Demander l'id du tournoi
            t_id = self.view.choose_tournament(tournaments_id)
            # Récupérer le tournoi avec cet id
            tournaments_table = self.db.table('tournaments')
            t = tournaments_table.get(doc_id=t_id)
            rounds = []
            for round in t['rounds']:
                rounds.append(Round.deserialize_round(round))
            players = []
            for player in t['players']:
                players.append(Player.deserialize_player(player))
            tournament = Tournament(
                t['name'],
                t['location'],
                t['date'],
                t['time_control'],
                t['description'],
                int(t['nb_rounds']),
                int(t['remaining_rounds']),
                t['finished'],
                rounds,
                players,
                t['ranking']
            )
            self.view.show_tournament(t_id, tournament)
            return tournament
        else:
            return None

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
                players = self.db.table('players').all()
                if len(players) >= Tournament.NB_PLAYERS:
                    tournament = self.create_tournament()
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
                else:
                    msg = """
                    Avant de commencer un nouveau tournoi,
                    veuillez ajouter """ + str(Tournament.NB_PLAYERS) + """
                    joueurs au moins dans la base de données.
                    """
                    self.view.show_message(msg)
            elif choice == 3:
                # Reprendre le tournoi
                self.view.show_message("Reprendre le tournoi")
                # Récupérer les tournois dans la base de données
                # Afficher les tournois avec leurs ids
                # tournaments = self.db.table('tournaments').all()
                # tournaments = self.db.table('tournaments')
                tournaments = self.db.table('tournaments').search(
                    where('finished') == False
                )
                if len(tournaments) != 0:
                    tournaments_id = []
                    # Récupérer tous les id
                    for t in tournaments:
                        tournaments_id.append(str(t.doc_id))
                    # Montrer les tournois
                    self.show_tournaments(tournaments_id)
                    # Demander l'id du tournoi
                    t_id = self.view.choose_tournament(tournaments_id)
                    # Récupérer le tournoi avec cet id
                    tournaments_table = self.db.table('tournaments')
                    t = tournaments_table.get(doc_id=t_id)
                    tournament = Tournament.deserialize_tournament(t)
                    # print(tournament)
                    # Continuer
                    self.run_tournament(tournament)
                    self.save_tournament(tournament, t_id)
                else:
                    self.view.show_message("Aucun tournoi en cours ...")
            elif choice == 4:
                # Demander le rapport souhaité
                selection = self.view.select_report()
                if selection == 1:
                    # Lister les acteurs par ordre alphabétique
                    self.show_players_by_name()
                elif selection == 2:
                    # Lister les acteurs par classement
                    self.show_players_by_rank()
                elif selection == 3:
                    '''
                    Sélection d'un tournoi
                    Affichage des joueurs par ordre alphabétique
                    '''
                    tournament = self.select_tournament()
                    players_list = sorted(
                        self.players,
                        key=lambda x: (x.last_name, x.first_name)
                    )
                    if tournament is not None:
                        self.view.show_players2(
                            players_list,
                            "ordre alphabétique"
                        )
                elif selection == 4:
                    '''
                    Sélection d'un tournoi
                    Affichage des joueurs par classement
                    '''
                    tournament = self.select_tournament()
                    players_list = sorted(
                        self.players,
                        key=lambda x: x.rank
                    )
                    if tournament is not None:
                        self.view.show_players2(
                            players_list,
                            "rang"
                        )
                elif selection == 5:
                    '''
                    Lister tous les tournois
                    '''
                    self.show_all_tournaments()
                elif selection == 6:
                    '''
                    Sélection d'un tournoi
                    Affichage des tours de ce tournoi
                    '''
                    tournament = self.select_tournament()
                    if tournament is not None:
                        self.view.show_tournament_rounds(tournament)
                elif selection == 7:
                    '''
                    Sélection d'un tournoi
                    Affichage des matchs d'un tournoi
                    '''
                    tournament = self.select_tournament()
                    if tournament is not None:
                        self.view.show_matchs_and_rounds_in_tournament(
                            tournament
                        )
                elif selection == 8:
                    pass
            elif choice == 5:
                # Quitter
                running = False
