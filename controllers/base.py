import db
import pprint
from models.tournament import Tournament
from models.match import Match
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
        for id in id_list:
            # Afficher le tournoi dont l'id correspond
            tournaments_table = self.db.table('tournaments')
            t = tournaments_table.get(doc_id=id)
            print(
                f"{t.doc_id}    "
                f"{t['name']} "
                f"{t['date']} "
                f"{t['location']} "
            )
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

    def save_tournament(self, tournament):
        dict_tournament = tournament.__dict__
        s_rounds = []
        for r in tournament.rounds:
            dict_round = r.__dict__
            s_matchs = []
            for m in r.matchs:
                dict_match = m.__dict__
                dict_match['player_a'] = \
                    dict_match['player_a'].__dict__
                dict_match['player_b'] = \
                    dict_match['player_b'].__dict__
                s_matchs.append(dict_match)
            dict_round['matchs'] = s_matchs
            s_rounds.append(r.__dict__)
        dict_tournament['rounds'] = s_rounds
        s_players = []
        for p in tournament.players:
            dict_player = p.__dict__
            s_players.append(dict_player)
        dict_tournament['players'] = s_players
        dict_tournament['date'] = str(dict_tournament['date'])
        pprint.pprint(dict_tournament)
        serialized_tournament = dict_tournament
        tournament_table = self.db.table('tournaments')
        tournament_table.insert(dict_tournament)

    @staticmethod
    def deserialize_tournament(serialized_tournament: dict) -> 'Tournament':
        """
        :param serialized_tournament: Takes a Tournament dict with all key,
               value information
        :return: Returns an object of Tournament class
        """
        id = serialized_tournament['id']
        name = serialized_tournament["name"]
        venue = serialized_tournament["venue"]
        date = serialized_tournament["date"]
        number_of_rounds = serialized_tournament["number_of_rounds"]
        time_control = serialized_tournament["time_control"]
        description = serialized_tournament["description"]
        list_of_rounds = [Round.deserialize_round(round_dict) for round_dict in
                          serialized_tournament["list_of_rounds"]]
        participant_list = [Player.deserialize(player_dict) for player_dict in
                            serialized_tournament["participant_list"]]
        participant_score = serialized_tournament["participant_score"]
        return Tournament(id,
                          name,
                          venue,
                          date,
                          number_of_rounds,
                          time_control,
                          description,
                          list_of_rounds,
                          participant_score,
                          participant_list)

    def serialize(self) -> dict:
        """
        :return: Returns a dict with all Tournament key, value information
        """
        tournament_data = {'id': self.id,
                           'name': self.name,
                           'venue': self.venue,
                           'date': self.date,
                           'number_of_rounds': self.number_of_rounds,
                           'time_control': self.time_control,
                           'description': self.description,
                           'list_of_rounds': [round.serialize() for round in
                                              self.list_of_rounds],
                           'participant_score': self.participant_score,
                           'participant_list': [player.serialize() for player
                                                in
                                                self.participant_list]}
        return tournament_data

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
                # Ajouter 8 joueurs au tournoi créé
                self.add_players(tournament)
                # Demander si on commence le tournoi
                start = self.view.ask_starting()
                # Si oui commence sinon retour au menu principal
                if start:
                    # Le tournoi est en cours
                    play = True
                    # Si aucun tour a été joué lancé le tour 1
                    if tournament.remaining_rounds == tournament.NB_ROUNDS:
                        # self.first_round()
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
                        print("Fin du tournoi")

                    # Enregistrer l'état du tournoi
                    self.save_tournament(tournament)

                    '''    
                    # Premier round
                    round_name = self.view.ask_round_name()
                    round = tournament.prepare_round_one(round_name)
                    tournament.add_round(round)
                    # Terminer le tour
                    self.view.ending_round()
                    # Saisir les scores
                    self.update_players_scores(tournament)
                    # Demander si on passe au tour suivant
                    continuing = self.view.ask_continuing()
                    while continuing and tournament.is_remaining_rounds():
                        # Demander le nom du round
                        round_name = self.view.ask_round_name()
                        round = tournament.prepare_next_round(round_name)
                        tournament.add_round(round)
                        # Demander si le tour est terminé
                        self.view.ending_round()
                        # Saisir les scores
                        self.update_players_scores(tournament)
                        # Demander si on passe au tour suivant
                        continuing = self.view.ask_continuing()
                    if tournament.is_remaining_rounds():
                        print("Tournoi mis en pause")
                    else:
                        print("Fin du tournoi")
                    '''
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
                tournaments_id = []
                # Récupérer tous les id
                for t in tournaments:
                    tournaments_id.append(str(t.doc_id))
                # Montrer les tournois
                self.show_tournaments(tournaments_id)
                # Demander l'id du tournoi
                t_id = self.view.choose_tournament(tournaments_id)
                # Créer le joueur et l'ajouter au tournoi grâce à l'id
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


            elif choice == 4:
                # Liste de rapports
                print("Liste des rapports")
            elif choice == 5:
                # Quitter
                running = False
