from models.round import Round
from models.match import Match
from models.player import Player

TIME = ("blitz", "bullet", "coup rapide")


class Tournament:

    NB_PLAYERS = 8
    NB_ROUNDS = 4

    def __init__(
        self,
        name,
        location,
        date,
        time_control,
        description,
        nb_turns=4
    ):
        self.name = name
        self.location = location
        self.date = date
        self.nb_turns = nb_turns
        self.rounds = []
        self.players = []
        self.time_control = time_control
        self.description = description
        self.ranking = []
        self.remaining_rounds = self.NB_ROUNDS

    def __str__(self):
        return f"Tournoi {self.name} à {self.location} le {self.date}."

    def __repr__(self):
        return str(self)

    def add_player(self, player):
        self.players.append(player)
        print(player.show_name() + " est ajouté au tournoi.")

    def show_players(self):
        print("\nClassement provisoire des joueurs : ")
        for n in range(len(self.players)):
            print(self.players[n], end=" ")
        print("\n")

    def sort_players(self):
        self.players = sorted(self.players, key=lambda x: (-x.score, x.rank))

    '''
    def decorate(function):
        def wrapper(tournament):
            # Trier les joueurs selon leurs scores et leurs classements
            tournament.sort_players()
            # Afficher le classement provisoire du tournoi
            tournament.show_players()
            result = function()
            return result
        return wrapper
    '''
    def add_round(self, round):
        self.rounds.append(round)
        self.remaining_rounds = self.remaining_rounds - 1

    def prepare_round_one(self, round_name):
        """
        Créer le premier round, trier les joueurs selon rang
        Diviser les joueurs en deux
        Associer les joueurs de la partie supérieure avec ceux de la partie
        inférieure et les faire jouer ensemble
        """
        # Ajoutées au lieu de decorate
        self.sort_players()
        self.show_players()

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
        else:
            print("Nombre impaire de joueurs pour le tournoi")
        # self.rounds.append(round)
        print(" ----------- " + round.show_name() + " ----------- ")
        round.show_matchs()
        return round

    def prepare_next_round(self, round_name):
        # Ajoutées au lieu de decorate
        self.sort_players()
        self.show_players()
        round = Round(round_name)
        print(" ----------- " + round.show_name() + " ----------- ")
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
                                player.has_already_played_with(a) and
                                opponent.has_already_played_with(b)
                        ):
                            temp.remove([a, b])
                            temp.extend([[a, player], [b, opponent]])
                            remaining_players.remove(player)
                            remaining_players.remove(opponent)
                            break
                        elif not (
                                player.has_already_played_with(b) and
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
        round.show_matchs()
        # self.rounds.append(round)

        return round

    def show_rounds(self):
        print("Liste de tous les tours d'un tournoi")
        for round in self.rounds:
            print(round.show_status())

    def show_rounds_and_matchs(self):
        print("Liste de tous les tours d'un tournoi avec leurs matchs")
        for round in self.rounds:
            print(round.show_name() + ":")
            round.show_matchs()

    def update_ranking(self, ranking):
        self.ranking = ranking

    def show_players_by_ranking(self):
        players = sorted(self.players, key=lambda x: x.rank)
        for player in players:
            print(player.show_name(), end=" ")
        print()

    def show_players_by_name(self):
        players = sorted(self.players, key=lambda x: x.last_name)
        for player in players:
            print(player.show_name(), end=" ")
        print()

    def get_players(self):
        return self.players

    def is_remaining_rounds(self):
        return True if self.remaining_rounds > 0 else False

'''

print("--------------- Tournament ---------------")
tournoi = Tournament("Championnat", "Paris", "15/11", "blitz", "test")

# Ajout de 8 joueurs au tournoi
playerA = Player("A", "a", "", "f", 100)
playerB = Player("B", "b", "", "m", 110)
playerC = Player("C", "c", "", "f", 120)
playerD = Player("D", "d", "", "m", 130)
playerE = Player("E", "e", "", "f", 140)
playerF = Player("F", "f", "", "m", 150)
playerG = Player("G", "g", "", "f", 160)
playerH = Player("H", "h", "", "m", 170)
tournoi.add_player(playerA)
tournoi.add_player(playerB)
tournoi.add_player(playerC)
tournoi.add_player(playerD)
tournoi.add_player(playerE)
tournoi.add_player(playerF)
tournoi.add_player(playerG)
tournoi.add_player(playerH)


# Premier round
tournoi.sort_players()
tournoi.show_players()
tournoi.add_round_one()
playerA.update_score(1)
playerB.update_score(0.5)
playerC.update_score(0)
playerD.update_score(0)
playerE.update_score(0)
playerF.update_score(0.5)
playerG.update_score(1)
playerH.update_score(1)

# Deuxième round
tournoi.sort_players()
tournoi.show_players()
tournoi.add_next_round("Round 2")
playerA.update_score(0.5)
playerB.update_score(0)
playerC.update_score(0.5)
playerD.update_score(0)
playerE.update_score(1)
playerF.update_score(0.5)
playerG.update_score(0.5)
playerH.update_score(1)

tournoi.sort_players()
tournoi.show_players()
tournoi.add_next_round("Round 3")
playerA.update_score(0)
playerB.update_score(0.5)
playerC.update_score(0.5)
playerD.update_score(1)
playerE.update_score(0.5)
playerF.update_score(0)
playerG.update_score(0.5)
playerH.update_score(1)

tournoi.sort_players()
tournoi.show_players()
tournoi.add_next_round("Round 4")

tournoi.show_rounds()
tournoi.show_rounds_and_matchs()





'''