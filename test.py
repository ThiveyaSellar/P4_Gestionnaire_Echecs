from models.tournament import Tournament
from models.player import Player


# Afficher tous les acteurs
# par ordre alaphabétique
# par classement


def show_tournaments(list_of_tournament):
    for tournament in list_of_tournament:
        print(tournament)

print("--------------- Tournament ---------------")
tournoi = Tournament("Championnat1", "Paris", "15/11", "blitz", "test")
tournoi2 = Tournament("Championnat2", "Paris", "15/11", "blitz", "test")
tournoi3 = Tournament("Championnat3", "Paris", "15/11", "blitz", "test")

# Ajout de 8 joueurs au tournoi
playerA = Player("A", "a", "", "f", 100)
playerB = Player("B", "b", "", "m", 110)
playerC = Player("C", "c", "", "f", 120)
playerD = Player("D", "d", "", "m", 130)
playerE = Player("E", "e", "", "f", 119)
playerF = Player("F", "f", "", "m", 150)
playerG = Player("G", "g", "", "f", 148)
playerH = Player("H", "h", "", "m", 102)

tournoi.add_player(playerA)
tournoi.add_player(playerH)
tournoi.add_player(playerB)
tournoi.add_player(playerG)
tournoi.add_player(playerE)
tournoi.add_player(playerD)
tournoi.add_player(playerC)
tournoi.add_player(playerF)

tournoi.show_players()
tournoi.show_players_by_name()
tournoi.show_players_by_ranking()

tournaments = []
tournaments.extend([tournoi,tournoi2, tournoi3])

show_tournaments(tournaments)

