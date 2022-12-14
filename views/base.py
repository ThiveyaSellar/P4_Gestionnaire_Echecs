from models.tools import non_empty_input, valid_date, multiline_input


class View:

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def prompt_for_player(self):
        infos = {
            "last_name": input("Nom : \n"),
            "first_name": input("Prénom: \n"),
            "birth_date": input("Date de naissance: \n"),
            "gender": input("Sexe : \n"),
            "rank": int(input("Classement : \n"))
        }
        return infos

    @staticmethod
    def ask_new_player(self):
        answer = input("Ajouter un autre joueur ? (Y/N)\n").upper()
        while answer != "Y" and answer != "N":
            answer = input("Ajouter un autre joueur ? (Y/N)\n").upper()
        return True if answer == "Y" else False

    @staticmethod
    def display_all_players(self, players):
        for player in players:
            player.show_infos()

    @staticmethod
    def get_player_index(self):
        return int(input('Quel est le numéro du joueur ? \n'))

    @staticmethod
    def get_new_rank(self):
        return int(input('Quel est le nouveau classement de ce joueur ? \n'))

    @staticmethod
    def get_tournament_infos(self):
        name = non_empty_input("Nom du tournoi :")
        location = non_empty_input("Lieu du tournoi :")
        # Vérifier la saisie valide d'une date
        date = valid_date()
        time_control = int(input(
            """ 
            Choisir le contrôle du temps :
            1 - Blitz
            2 - Bullet
            3 - Coup rapide    
            """
        ))
        while time_control != 1 and time_control != 2 and time_control != 3:
            time_control = int(input(
                """ 
                Choisir le contrôle du temps :
                1 - Blitz
                2 - Bullet
                3 - Coup rapide    
                """
            ))
        print("Ajouter une description : ")
        description = multiline_input()

        infos = {
            "name": name,
            "location": location,
            "date": date,
            "time_control": time_control,
            "description": description
        }
        return infos

    @staticmethod
    def add_player(self, ids):
        pid = input("Numéro du joueur : \n")
        correct = True if pid in ids else False
        while not correct:
            print("Numéro non présent ou déjà choisi. \n")
            pid = input("Numéro du joueur : \n")
            correct = True if pid in ids else False
        return pid

    @staticmethod
    def ask_starting(self):

        answer = input(
            "Voulez-vous commencer le tournoi ? (Oui/Non)"
        ).upper()
        '''
        while True:
            answer = input(
                "Voulez-vous commencer le tournoi ? (Y/N)"
            )
            if answer == 'Y':
                break
            elif answer == 'N':
                break
        '''
        while answer != "OUI" and answer != "NON":
            answer = input(
                "Voulez-vous commencer le tournoi ? (Oui/Non)"
            ).upper()
        return True if answer == "OUI" else False

    @staticmethod
    def ending_round(self):
        print("Tour en cours ... ")
        answer = input(
            "Quand le tour est terminé saisir 'FIN'.  \n"
        ).upper()
        while answer != 'FIN':
            answer = input(
                 "Quand le tour est terminé saisir 'FIN'.  \n"
            ).upper()

    @staticmethod
    def ask_score(self, player_name):
        print(f"Quel est le score de {player_name}?")
        score = int(input(
            f"Victoire: 1, Nul: 0.5, Échec: 0. \n"
        ))
        while score != 1 and score != 0.5 and score != 0:
            print(f"Quel est le score de {player_name}?")
            score = int(input(
                f"Victoire: 1, Nul: 0.5, Échec: 0. \n"
            ))
        return score

    @staticmethod
    def ask_continuing(self):
        answer = input(
            "Voulez-vous passer au tour suivant ? (Oui/Non)  \n"
        ).upper()
        while answer != "OUI" and answer != "NON":
            answer = input(
                "Voulez-vous passer au tour suivant ? (Oui/Non)  \n"
            ).upper()
        return True if answer == "OUI" else False

    @staticmethod
    def ask_round_name(self):
        round_name = input(
            "Quel est le nom du round ? \n"
        )
        return round_name

'''
v = View()

v.display_main_menu()
v.display_player_management_options()
infos = v.prompt_for_player()
print(infos["last_name"])
print(v.ask_new_player())
'''