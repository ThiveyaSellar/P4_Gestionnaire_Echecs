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
    def prompt_for_player(players):
        infos = {
            "last_name": input("Nom : \n").upper(),
            "first_name": input("Prénom: \n"),
            "birth_date": str(ask_date("Date de naissance")),
            "gender": input("Sexe : \n"),
            "rank": int(View.get_new_rank(players))
        }
        return infos

    @staticmethod
    def ask_new_player():
        answer = input("Ajouter un autre joueur ? (Y/N)\n").upper()
        while answer != "Y" and answer != "N":
            answer = input("Ajouter un autre joueur ? (Y/N)\n").upper()
        return True if answer == "Y" else False

    @staticmethod
    def get_player_index():
        print()
        return int(input('Quel est le numéro du joueur ? \n'))

    @staticmethod
    def get_new_rank(players):
        update = True
        rank = int(input('Quel est le classement de ce joueur ? \n'))
        for p in range(len(players)):
            if players[p]['rank'] == rank:
                update = False
                break
        while not update:
            update = True
            print("Ce classement existe déjà.")
            rank = int(
                input('Quel est le classement de ce joueur ? \n'))
            for p in range(len(players)):
                if players[p]['rank'] == rank:
                    update = False
                    break
        print()
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
        else:
            time_control = ""
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
    def show_players_to_add(players, players_id):
        for nb in range(len(players)):
            if str(nb+1) in players_id:
                print(
                    f"{str(nb+1)}     "
                    f"{players[nb]['last_name']} "
                    f"{players[nb]['first_name']} "
                    f"({players[nb]['rank']})"
                )
        print()

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
        score_b = 0
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

    @staticmethod
    def show_message(message):
        print(message)

    @staticmethod
    def show_players(tournament):
        players = tournament.get_players()
        print("\nClassement des joueurs : ")
        for n in range(len(players)):
            print(players[n].get_last_name(), end=" ")
        print("\n")

    @staticmethod
    def show_matchs_in_round(round):
        for match in round.get_matchs():
            print(
                match.get_player_a().get_last_name()
                + " vs "
                + match.get_player_b().get_last_name()
            )

    @staticmethod
    def show_round_status(round):
        debut = round.get_start_date_time()
        end = round.get_end_date_time()
        if end == "":
            end_msg = 'en cours'
        else:
            end_msg = end
        print(
            f'{round.get_name()} --- '
            f'début : {debut} --- '
            f'fin : {end_msg}'
        )

    @staticmethod
    def show_round_infos(round):
        print(" ----------- " + round.get_name() + " ----------- ")
        View.show_matchs_in_round(round)
        View.show_round_status(round)

    @staticmethod
    def show_results(winner, ranking):
        print("Le gagnant du tournoi : " + winner.get_names())
        print("Le classement final du tournoi : ")
        print(ranking)

    @staticmethod
    def show_list_of_players(players):
        for p in players:
            print(
                f"{p[0]}\t"
                f"{p[1].get_last_name()} " 
                f"{p[1].get_first_name()}\t\t"
                f"({p[1].get_rank()})"
            )

    @staticmethod
    def show_players1(players_list, order):
        if len(players_list) == 0:
            print("Aucun joueur inscrit...")
        else:
            print(f"\nListe des joueurs par {order} : ")
            for n in range(len(players_list)):
                print(
                    f"{players_list[n].get_rank()}\t"
                    f"{players_list[n].get_last_name()}\t"
                    f"{players_list[n].get_first_name()}\n",
                    end=""
                )
            print("\n")

    @staticmethod
    def show_tournament(i, tournament, statut=""):
        print(
            f"{i}\t"
            f"{tournament.get_name()}\t"
            f"{tournament.get_date()}\t"
            f"{tournament.get_location()}\t"
            f"{statut}"
        )

    @staticmethod
    def show_players2(players_list, order):
        print(f"\nListe des joueurs par {order} : ")
        for n in range(len(players_list)):
            print(
                f"{players_list[n].get_rank()}\t"
                f"{players_list[n].get_last_name()}\t"
                f"{players_list[n].get_first_name()}"
            )
        print("\n")

    @staticmethod
    def show_tournament_rounds(tournament):
        print("Liste de tous les tours :")
        for round in tournament.get_rounds():
            View.show_round_status(round)

    @staticmethod
    def show_matchs_and_rounds_in_tournament(tournament):
        print("\nListe de tous les tours d'un tournoi avec leurs matchs :")
        for round in tournament.get_rounds():
            print(round.get_name() + ":")
            for match in round.get_matchs():
                player_name_a = match.get_player_a().get_names()
                player_name_b = match.get_player_b().get_names()
                if match.score_a == 0.5:
                    msg = "match nul"
                elif match.score_a == 1.0:
                    msg = "gagnant: " + player_name_a
                else:
                    msg = "gagnant: " + player_name_b
                print(f"{player_name_a} vs {player_name_b}\t\t{msg}")
            print("\n")
