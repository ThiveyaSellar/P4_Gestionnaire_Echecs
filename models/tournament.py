from models.match import Match
from models.player import Player
from models.round import Round


class Tournament:

    NB_PLAYERS = 8
    NB_ROUNDS = 4
    TIME = ("blitz", "bullet", "coup rapide")

    def __init__(
        self,
        name,
        location,
        date,
        time_control,
        description,
        nb_rounds=NB_ROUNDS,
        remaining_rounds=NB_ROUNDS,
        finished=False,
        rounds=[],
        players=[],
        ranking=[]
    ):
        # Saisies par l'utilisateur
        self.name = name
        self.location = location
        self.date = date
        self.time_control = time_control
        self.description = description
        # Valeur par défaut
        self.nb_rounds = nb_rounds
        self.remaining_rounds = remaining_rounds
        # Modifié quand le tournoi est terminé
        self.finished = finished
        # Ajoutés au cours du tournoi
        self.rounds = rounds
        self.players = players
        # Classement final saisi par le manager
        self.ranking = ranking

    def get_name(self):
        return self.name

    def get_date(self):
        return self.date

    def get_location(self):
        return self.location

    def get_rounds(self):
        return self.rounds

    def get_players(self):
        return self.players

    def get_players_size(self):
        return len(self.players)

    def add_player(self, player):
        self.players.append(player)

    def update_ranking(self, ranking):
        self.ranking = ranking

    def get_final_ranking(self):
        final_ranking = ""
        # Le gagnant est le premier de la liste
        winner = self.players[0].get_names()
        for n in range(len(self.players)):
            final_ranking = \
                final_ranking + self.players[n].get_names() + " "
        return final_ranking

    def sort_players(self):
        self.players = sorted(self.players, key=lambda x: (-x.score, x.rank))

    def add_round(self, round):
        self.rounds.append(round)
        self.remaining_rounds = self.remaining_rounds - 1

    def has_remaining_rounds(self):
        return True if self.remaining_rounds > 0 else False

    def clear_all(self):
        self.players.clear()
        self.rounds.clear()
        self.ranking.clear()

    def set_finished(self):
        self.finished = True

    def prepare_round_one(self, round_name):
        """
        Créer le premier round, trier les joueurs selon rang
        Diviser les joueurs en deux
        Associer les joueurs de la partie supérieure avec ceux de la partie
        inférieure et les faire jouer ensemble
        """
        self.sort_players()
        round = Round(round_name)
        nb_player = len(self.players)
        if nb_player % 2 == 0:
            half = int(nb_player/2)
            self.players.sort(key=lambda x: x.rank)
            for p in range(half):
                player_a = self.players[p]
                player_b = self.players[p+half]
                match = Match(player_a, player_b)
                player_a.add_opponent(player_b)
                player_b.add_opponent(player_a)
                round.add_match(match)
            return round
        else:
            return None

    def prepare_next_round(self, round_name):
        # Ajoutées au lieu de decorate
        self.sort_players()
        round = Round(round_name)
        # Liste des joueurs qu'il reste à coupler
        remaining_players = []
        for i in range(len(self.players)):
            remaining_players.append(self.players[i])
        # Nouvelle liste de couples de joueurs temporaire
        temp = []

        while len(remaining_players) > 0:
            if len(remaining_players) == 2:
                player = remaining_players[0]
                opponent = remaining_players[1]
                if player.has_already_played_with(opponent):
                    for i in range(len(temp)-1, -1, -1):
                        a = temp[i][0]
                        b = temp[i][1]
                        if not (
                                player.has_already_played_with(a) or
                                opponent.has_already_played_with(b)
                        ):
                            temp.remove([a, b])
                            temp.extend([[a, player], [b, opponent]])
                            remaining_players.remove(player)
                            remaining_players.remove(opponent)
                            break
                        elif not (
                                player.has_already_played_with(b) or
                                opponent.has_already_played_with(a)
                        ):
                            temp.remove([a, b])
                            temp.extend([[b, player], [a, opponent]])
                            remaining_players.remove(player)
                            remaining_players.remove(opponent)
                            break
                else:
                    temp.append([player, opponent])
                    remaining_players.remove(player)
                    remaining_players.remove(opponent)
            else:
                player = remaining_players[0]
                for opponent in remaining_players[1:len(remaining_players)]:
                    if player.has_already_played_with(opponent):
                        continue
                    else:
                        temp.append([player, opponent])
                        remaining_players.remove(player)
                        remaining_players.remove(opponent)
                        break

        for pair in range(len(temp)):
            player_a = temp[pair][0]
            player_b = temp[pair][1]
            player_a.add_opponent(player_b)
            player_b.add_opponent(player_a)
            match = Match(player_a, player_b)
            round.add_match(match)

        return round

    def serialize(self):
        rounds = []
        for r in self.rounds:
            rounds.append(r.serialize())
        players = []
        for p in self.players:
            players.append(p.serialize())

        tournament = {
            "name": self.name,
            "location": self.location,
            "date": str(self.date),
            "time_control": self.time_control,
            "description": self.description,
            "nb_rounds": self.nb_rounds,
            "finished": self.finished,
            "remaining_rounds": self.remaining_rounds,
            "rounds": rounds,
            "players": players,
            "ranking": self.ranking
        }
        return tournament

    @staticmethod
    def deserialize_tournament(serialized_tournament):
        name = serialized_tournament["name"]
        location = serialized_tournament["location"]
        date = serialized_tournament["date"]
        time_control = serialized_tournament["time_control"]
        description = serialized_tournament["description"]
        nb_rounds = serialized_tournament["nb_rounds"]
        remaining_rounds = serialized_tournament["remaining_rounds"]
        finished = serialized_tournament["finished"]
        rounds = []
        for r in serialized_tournament["rounds"]:
            rounds.append(Round.deserialize_round(r))
        players = []
        for p in serialized_tournament["players"]:
            players.append(Player.deserialize_player(p))
        ranking = serialized_tournament["ranking"]

        tournament = Tournament(
            name,
            location,
            date,
            time_control,
            description,
            nb_rounds,
            remaining_rounds,
            finished,
            rounds,
            players,
            ranking
        )

        return tournament

