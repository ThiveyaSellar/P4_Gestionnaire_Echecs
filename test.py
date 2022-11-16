# Enter Python code here and hit the Run button

# Enter Python code here and hit the Run button.

class Player:

    def __init__(self, last_name, rank, score):
        self.last_name = last_name
        self.score = score
        self.rank = rank

    def __str__(self):
        if self.gender.lower() == "f":
            return f"Madame {self.first_name} {self.last_name} " \
                   f"née le {self.birth_date}, classement : {self.rank}."
        elif self.gender.lower() == "h":
            return f"Monsieur {self.first_name} {self.last_name} " \
                   f"né le {self.birth_date}, classement : {self.rank}."

    def __repr__(self):
        return str(self)

    # Changer le classement du joueur
    def change_rank(self, new_rank):
        if new_rank > 0:
            self.rank = new_rank
        else:
            print("Le classement doit être strictement positif.")


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

    def add_round(self, round):
        self.rounds.append(round)

    def sort_player_rank(self):
        """
        Trier les joueurs selon leurs rangs
        """
        self.players.sort(key=lambda x: x.rank)

    def sort_player_score(self):
        self.players.sort(key=lambda x: x.score)

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
            half = nb_player / 2
            self.sort_player_rank()
            for i in range(half):
                player_a = self.players[i]
                player_b = self.players[i + half]
                match = match(player_a, player_b)
                round_one.add_match(match)
        else:
            print("Nombre impaire de joueurs pour le tournoi")
        self.rounds.append(round_one)

    def add_next_round(self, round_name):
        round = Round(round_name)
        self.players = sorted(self.players, key=lambda x: (x.score, x.rank))

    def afficher_joueurs_trier(self):
        print("Avant le tri")
        for p in self.players:
            print(p.last_name + " " + str(p.score) + " " + str(p.rank))
        self.players = sorted(self.players, key=lambda x: (-x.score, x.rank))
        print("Après le tri")
        for p in self.players:
            print(p.last_name + " " + str(p.score) + " " + str(p.rank))


tournoi = Tournament("test", "test", "test", "test", "test")

a = Player("Caramely", 100, 10)
b = Player("Trla", 16, 2)
c = Player("Simba", 99, 10)

tournoi.add_player(a)
tournoi.add_player(b)
tournoi.add_player(c)

# Avant : a b c Après c a b
tournoi.afficher_joueurs_trier()


