from models.tournament import Tournament
from models.match import Match
from models.round import Round
from models.player import Player

class Controller:

    def __init__(self, tournament: Tournament, view):
        # models
        self.players = []
        self.tournament = tournament

        # views
        self.view = None

    def get_players(self):
        while len(self.players) < 8:
            infos = self.view.prompt_for_player()
            if not infos:
                return
            player = Player(
                infos["last_name"],
                infos["first_name"],
                infos["birth_date"],
                infos["gender"],
                infos["rank"]
            )
            self.players.append(player)

    def create_tournament(self):
        pass

    def display_menu(self):
        # Créer un tournoi
        # Mettre en pause le tournoi
        # Arrêter le tournoi
        # Afficher les stats
        # MAJ classement
        # Ajouter des joueurs


    def run(self):
        self.display_menu()
        self.create_tournament()
        self.get_players()