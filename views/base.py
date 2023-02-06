from models.tools import non_empty_input, ask_date, multiline_input


class View:

    @staticmethod
    def display_main_menu():
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
    def display_player_management_options():
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
    def prompt_for_player():
        infos = {
            "last_name": input("Nom : \n").upper(),
            "first_name": input("Prénom: \n"),
            "birth_date": ask_date("Date de naissance"),
            "gender": input("Sexe : \n"),
            "rank": int(input("Classement : \n"))
        }
        return infos

    @staticmethod
    def ask_new_player():
        answer = input("Ajouter un autre joueur ? (Y/N)\n").upper()
        while answer != "Y" and answer != "N":
            answer = input("Ajouter un autre joueur ? (Y/N)\n").upper()
        return True if answer == "Y" else False

    @staticmethod
    def display_all_players(players):
        for player in players:
            player.show_infos()

    @staticmethod
    def get_player_index():
        print()
        return int(input('Quel est le numéro du joueur ? \n'))

    @staticmethod
    def get_new_rank(players):
        update = True
        rank = int(input('Quel est le nouveau classement de ce joueur ? \n'))
        for p in range(len(players)):
            if players[p]['rank'] == rank:
                update = False
                break
        while not update:
            update = True
            print("Ce classement existe déjà!")
            rank = int(
                input('Quel est le nouveau classement de ce joueur ? \n'))
            for p in range(len(players)):
                if players[p]['rank'] == rank:
                    update = False
                    break

        return rank

    @staticmethod
    def get_tournament_infos():
        name = non_empty_input("Nom du tournoi : ")
        location = non_empty_input("Lieu du tournoi : ")
        # Vérifier la saisie valide d'une date
        date = ask_date("Date du tournoi")
        choice = int(input(
            "Contrôle du temps :\n1 - Blitz\n2 - Bullet\n3 - Coup rapide\n"
        ))
        while choice != 1 and choice != 2 and choice != 3:
            choice = int(input(
                "Contrôle du temps :\n1 - Blitz\n2 - Bullet\n3 - Coup rapide\n"
            ))
        if choice == 1:
            time_control = "Blitz"
        elif choice == 2:
            time_control = "Bullet"
        elif choice == 3:
            time_control = "Coup rapide"
        print(
            "Description : (une fois la saisie terminée, appuyez sur Entrée)")
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
    def add_player(ids):
        pid = input("Numéro du joueur : \n")
        correct = True if pid in ids else False
        while not correct:
            print("Numéro non présent ou déjà choisi. \n")
            pid = input("Numéro du joueur : \n")
            correct = True if pid in ids else False
        return pid

    @staticmethod
    def choose_tournament(tournaments_id):
        nb_tournaments = len(tournaments_id)
        # Création d'une liste de tuple
        # Associant l'indice affiché du tournoi avec le doc_id du tournoi
        correspondances = []
        for nb in range(nb_tournaments):
            correspondances.append((nb + 1, tournaments_id[nb]))

        # Demander l'indice et vérifier la saisie
        choice = input("Numéro du tournoi : \n")
        # correct = True if tid in ids else False
        correct = True if (nb_tournaments >= int(choice) >= 1) else False
        while not correct:
            print("Numéro non présent dans la liste. \n")
            choice = input("Numéro du tournoi : \n")
            correct = True if (nb_tournaments >= int(choice) >= 1) else False

        # Récupérer le doc_id associé à l'indice choisi
        for c in correspondances:
            if c[0] == int(choice):
                tid = c[1]
                break
        return int(tid)

    @staticmethod
    def ask_starting():

        answer = input(
            "Voulez-vous commencer le tournoi ? (Oui/Non)\n"
        ).upper()
        '''
        while True:
            answer = input(
                "Voulez-vous commencer le tournoi ? (Y/N)\n"
            )
            if answer == 'Y':
                break
            elif answer == 'N':
                break
        '''
        while answer != "OUI" and answer != "NON":
            answer = input(
                "Voulez-vous commencer le tournoi ? (Oui/Non)\n"
            ).upper()
        return True if answer == "OUI" else False

    @staticmethod
    def ending_round():
        print("Tour en cours ... ")
        answer = input(
            "Quand le tour est terminé saisir 'FIN'.  \n"
        ).upper()
        while answer != 'FIN':
            answer = input(
                "Quand le tour est terminé saisir 'FIN'.  \n"
            ).upper()

    @staticmethod
    def ask_score(player_name):
        print(f"Quel est le score de {player_name}?")
        score = float(input(
            f"Victoire: 1, Nul: 0.5, Échec: 0. \n"
        ))
        while score != 1.0 and score != 0.5 and score != 0.0:
            print(f"Quel est le score de {player_name}?")
            score = float(input(
                f"Victoire: 1, Nul: 0.5, Échec: 0. \n"
            ))
        return score

    @staticmethod
    def get_scores(name_a, name_b):
        print(f"Quel est le score de {name_a}?")
        score_a = float(input(
            f"Victoire: 1, Nul: 0.5, Échec: 0. \n"
        ))
        while score_a != 1.0 and score_a != 0.5 and score_a != 0.0:
            print(f"Quel est le score de {name_a}?")
            score_a = float(input(
                f"Victoire: 1, Nul: 0.5, Échec: 0. \n"
            ))
        if score_a == 1:
            score_b = 0
        elif score_a == 0.5:
            score_b = 0.5
        elif score_a == 0:
            score_b = 1
        print(f"Le score de {name_b} est {score_b}. \n")
        return [score_a, score_b]

    @staticmethod
    def ask_continuing():
        answer = input(
            "Voulez-vous passer au tour suivant ? (Oui/Non)  \n"
        ).upper()
        while answer != "OUI" and answer != "NON":
            answer = input(
                "Voulez-vous passer au tour suivant ? (Oui/Non)  \n"
            ).upper()
        return True if answer == "OUI" else False

    @staticmethod
    def ask_round_name():
        round_name = input(
            "Quel est le nom du round ? \n"
        )
        return round_name

    @staticmethod
    def select_report():
        menu = """
        ----- Rapports -----
                    
        * Acteurs :
            1 - par ordre alphabétique
            2 - par classement
        * Joueurs d'un tournoi :
            3 - par ordre alphabétique
            4 - par classement
        5 - Tournois
        6 - Tours d'un tournoi
        7 - Matchs d'un tournoi
        8 - Retour au menu principal    
        """
        print(menu)
        choice = input("Votre choix : \n")
        while int(choice) <= 0 or int(choice) >= 9:
            print(menu)
            choice = input("Votre choix : \n")
        return int(choice)
