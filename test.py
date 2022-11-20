def add_next_round(self, round_name):
    round = Round(round_name)
    # Trier les joueurs selon le score puis le rang
    # self.sort_players()
    # Liste initiale des joueurs
    players = self.players
    # Liste des joueurs qu'il reste à coupler
    remaining_players = []
    for i in range(len(self.players)):
        remaining_players.append(self.players[i])

    print("test remaining")
    print(remaining_players)
    print("* Liste des joueurs qui reste à coupler :")
    for r in range(len(remaining_players)):
        print(remaining_players[r])

    # Nouvelle liste de couples de joueurs temporaire
    temp = []
    print("\n* Liste des couples de joueurs :")
    print(temp)
    print()

    while len(remaining_players) > 0:
        if len(remaining_players) == 2:
            print("Il reste deux joueurs.")
            player = remaining_players[0]
            opponent = remaining_players[1]
            if player.has_already_played_with(opponent):
                print("Les deux joueurs restants ont déjà joué ensemble")
                for i in range(len(temp), 0, -1):
                    if (
                            player.has_already_played_with(temp[i][0]) and
                            opponent.has_already_played_with(temp[i][1])
                    ):
                        print("Situation A")
                        break
                    elif (
                            player.has_already_played_with(temp[i][0]) and
                            opponent.has_already_played_with(temp[i][1])
                    ):
                        print("Situation B")
                        break
                break
            else:
                temp.append([
                    player,
                    opponent
                ])

                print("\n* Liste des couples de joueurs :")
                print(temp)
                print()

                remaining_players.remove(player)
                remaining_players.remove(opponent)

                print("* Liste des joueurs qui reste à coupler :")
                for r in range(len(remaining_players)):
                    print(remaining_players[r])
                print("\n")
                break
        else:
            player = remaining_players[0]
            print("Joueur : " + player.show_name())
            for opponent in remaining_players[1:len(remaining_players)]:
                if player.has_already_played_with(opponent):
                    continue
                else:
                    temp.append([
                        player,
                        opponent
                    ])

                    print("\n* Liste des couples de joueurs :")
                    print(temp)
                    print()

                    remaining_players.remove(player)
                    remaining_players.remove(opponent)

                    print("* Liste des joueurs qui reste à coupler :")
                    for r in range(len(remaining_players)):
                        print(remaining_players[r])
                    print("\n")
                    break

    for b in range(len(self.players)):
        print("Les adversaires de " + self.players[b].show_name())
        self.players[b].show_opponents()
        print("\n")

    for pair in range(len(temp)):
        temp[pair][0].add_opponent(temp[pair][1])
        temp[pair][1].add_opponent(temp[pair][0])

    print("test")
    for a in range(len(self.players)):
        print("Les adversaires de " + self.players[a].show_name())
        self.players[a].show_opponents()


def add_next_round(self, round_name):
    # Créer un nouveau round
    round = Round(round_name)

    # Liste initiale des joueurs
    players = self.players

    # Liste des joueurs qu'il reste à coupler
    # Ajouter tout le monde au début
    remaining_players = []
    for i in range(len(players)):
        remaining_players.append(players[i])

    print("*** Liste des joueurs qui restent à coupler ***")
    show_remaining_players(remaining_players)
    print()

    # Nouvelle liste de couples temporaire
    temp = []
    print("*** Liste des couples de joueurs ***")
    print(temp)

    num = 0
    while len(remaining_players) > 0:
        player = remaining_players[num]
        for opponent in remaining_players[num + 1:len(remaining_players)]:
            if not player.has_already_played_with(opponent):
                temp.append([
                    player,
                    opponent
                ])
                remaining_players.remove(player)
                remaining_players.remove(opponent)
            else:
                pass
        num = num + 1

    # Joueur n
    # A-t-il déjà joué avec son voisin de droite ?
    # Non :
    # coupler avec son voisin de droite : ajouter le couple dans la liste temporaire
    # retirer ces deux joueurs des restants
    # Oui :
    # A-t-il au moins un voisin a droite avec qui il n'a pas joué ?
    # Oui :
    # coupler avec son voisin de droite : ajouter le couple dans la liste temporaire
    # retirer ces deux joueurs des restants
    # Non :
    # récupérer le dernier couple ajouté à temp
    #
    # a b c d
    # c - a ou b - d
    # Non : coupler
    # Oui : c - b ou a - d
    # Non : coupler
    # Oui : e f c d


# Trier les joueurs en dehors du round ou créer une méthode qu'on appellera dans round
def show_remaining_players(players):
    for r in range(len(players)):
        print(players[r])