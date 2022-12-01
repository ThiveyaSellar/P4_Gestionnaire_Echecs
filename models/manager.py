from models.player import Player
from models.tournament import Tournament


class Manager:

    def __init__(self, serialized_players, serialized_tournaments):
        players = []
        tournaments = []

        for sp in serialized_players:
            player = Player(
                sp["last_name"],
                sp["first_name"],
                sp["birth_date"],
                sp["gender"],
                sp["rank"]
            )
            players.append(player)
        self.players = players

        for st in serialized_tournaments:
            tournament = Tournament(
                st["name"],
                st["location"],
                st["date"],
                st["time_control"],
                st["description"],
                st["nb_turns"],
            )
            tournaments.append(tournament)
        self.tournaments = tournaments
