from round import Round
from match import Match
from player import Player

TIME = ("blitz", "bullet", "coup rapide")


class Tournament:

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

    def __str__(self):
        return f"Tournoi {self.name} à {self.location} le {self.date}."

    def __repr__(self):
        return str(self)

    def add_player(self, player):
        self.players.append(player)
        print(player.show_name() + " est ajouté au tournoi.")

    def show_players(self):
        print("Liste des joueurs : ")
        for n in range(len(self.players)):
            print(self.players[n].show_name(), end=" ")
        print("\n")

    def add_round_one(self):
        """
        Créer le premier round, trier les joueurs selon rang
        Diviser les joueurs en deux
        Associer les joueurs de la partie supérieure avec ceux de la partie
        inférieure et les faire jouer ensemble
        """
        round_one = Round("Round 1")
        nb_player = len(self.players)
        if nb_player % 2 == 0:
            half = int(nb_player/2)
            self.players.sort(key=lambda x: x.rank)
            print("Les matchs du premier round : ")
            for p in range(half):
                player_a = self.players[p]
                player_b = self.players[p+half]
                print(player_a.show_name() + " - " + player_b.show_name())
                match = Match(player_a, player_b)
                player_a.add_opponent(player_b)
                player_b.add_opponent(player_a)
                round_one.add_match(match)
        else:
            print("Nombre impaire de joueurs pour le tournoi")
        self.rounds.append(round_one)

    def add_next_round(self, round_name):
        round = Round(round_name)
        # Trier les joueurs selon le score puis le rang
        print("* Avant le tri : ")
        self.show_players()
        self.players = sorted(self.players, key=lambda x: (-x.score, x.rank))
        print("* Après le tri : ")
        self.show_players()

        # Liste initiale des joueurs
        players = self.players
        # Liste des joueurs qu'il reste à coupler
        remaining_players = self.players
        print("* Liste des joueurs qui reste à coupler :")
        for r in range(len(remaining_players)):
            print(remaining_players[r].show_name(), end=" ")

        # Nouvelle liste de couples de joueurs temporaire
        temp = []
        print("\n* Liste des couples de joueurs :")
        print(temp)
        print()

        while len(remaining_players) > 0:
            if len(remaining_players) == 2:
                print("Il reste deux joueurs.")
                break
            else:
                player = remaining_players[0]
                print("Joueur : " + player.show_name())
                for opponent in remaining_players[1:len(remaining_players)]:
                    if player.has_already_played_with(opponent):
                        continue
                    else:
                        temp.append([
                            player.show_name(),
                            opponent.show_name()
                        ])

                        print("\n* Liste des couples de joueurs :")
                        print(temp)
                        print()

                        remaining_players.remove(player)
                        remaining_players.remove(opponent)

                        print("* Liste des joueurs qui reste à coupler :")
                        for r in range(len(remaining_players)):
                            print(remaining_players[r].show_name(), end=" ")
                        print("\n")
                        break

       # When temp is official add opponents in players
    '''
        for p in range(len(players)):
            print("p : " + players[p].show_name())
            # Vérifier que le joueur n'est pas déjà couplé à un autre joueur
            player_in_temp = False
            for i in range(len(temp)):
                if players[p].show_name() in temp[i]:
                    player_in_temp = True
                    break
            if len(remaining_players) == 2:
                print("Il reste deux joueurs")
            else:
                if player_in_temp:
                    continue
                else:
                    for v in range(p+1, len(players)):
                        # Vérifier qu'il n'a pas déjà joué avec son voisin
                        # S'il a déjà joué on passe au voisin suivant
                        # Sinon on les ajoute ensemble à temp
                        if players[p].has_already_played_with(players[v]):
                            continue
                        else:
                            temp.append([
                                players[p].show_name(),
                                players[v].show_name()
                            ])
                            remaining_players.remove(players[p].show_name())
                            remaining_players.remove(players[v].show_name())
                            break
            print(remaining_players)
        print(temp)
    '''

    def test_update_score(self):
        self.players[0].update_score(1)
        self.players[1].update_score(0.5)
        self.players[2].update_score(0)
        self.players[3].update_score(0)
        self.players[4].update_score(0)
        self.players[5].update_score(0.5)
        self.players[6].update_score(1)
        self.players[7].update_score(1)


tournoi = Tournament("Championnat", "Paris", "15/11", "blitz", "test")

# Ajout de 8 joueurs au tournoi
lettre = 'A'
classement = 100
for i in range(8):
    participant = Player(lettre, "", "", "f", classement)
    lettre = chr(ord(lettre)+1)
    classement = classement + 10
    tournoi.add_player(participant)

# Affichage des noms des joueurs du tournoi
tournoi.show_players()

# Ajout du premier round
tournoi.add_round_one()

# MAJ score
tournoi.test_update_score()

print("\nTest round 2:\n")
tournoi.add_next_round("Round 2")
