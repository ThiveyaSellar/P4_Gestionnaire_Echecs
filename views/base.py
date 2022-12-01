from models.player import Player

class View:

    def __init__(self):
        pass

    def display_main_menu(self):
        menu = """
        ----- Menu principal -----
        
        1 - Gestion des joueurs
        2 - Nouveau tournoi
        3 - Reprendre un tournoi en cours
        4 - Rapports
        5 - Quitter
        """
        print(menu)
        choice = input("Votre choix : \n")
        print()
        return choice

    def display_player_management_options(self):
        menu = """
        ----- Gestion des joueurs -----
        
        1 - Ajouter un nouveau joueur
        2 - Modifier le classement d'un joueur
        3 - Afficher les joueurs
        4 - Retour au menu principal
        """
        print(menu)
        choice = input("Votre choix : \n")
        print()
        return choice

    def prompt_for_player(self):
        infos = {
            "last_name": input("Nom : \n"),
            "first_name": input("Prénom: \n"),
            "birth_date": input("Date de naissance: \n"),
            "gender": input("Sexe : \n"),
            "rank": input("Classement : \n")
        }
        return infos

    def ask_new_player(self):
        answer = input("Ajouter un autre joueur ? (Y/N)\n").upper()
        while answer != "Y" and answer != "N":
            answer = input("Ajouter un autre joueur ? (Y/N)\n").upper()
        return True if answer == "Y" else False

    def display_all_players(self, players):
        for player in players:
            player.show_infos()

    def get_player_index(self):
        return input("Quel est le numéro du joueur à modifier ? \n")

    def get_new_rank(self):
        return input('Quel est le nouveau classement de ce joueur ? \n')



v = View()
'''
v.display_main_menu()
v.display_player_management_options()
infos = v.prompt_for_player()
print(infos["last_name"])
print(v.ask_new_player())
'''