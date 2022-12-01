class Player:

    def __init__(self, last_name, first_name, birth_date, gender, rank):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.gender = gender
        self.rank = rank
        self.score = 0
        self.opponents = []

    def __str__(self):
        return f"{self.last_name}"

    def show_full_infos(self):
        if self.gender.lower() == "f":
            return f"Madame {self.first_name} {self.last_name} " \
                   f"née le {self.birth_date}, classement : {self.rank}, " \
                    f"score: {self.score}."
        elif self.gender.lower() == "m":
            return f"Monsieur {self.first_name} {self.last_name} " \
                   f"né le {self.birth_date}, classement : {self.rank}, " \
                    f"score: {self.score}."

    def show_infos(self):
        print(f"{self.rank}     {self.last_name}    {self.first_name}")

    def __repr__(self):
        return str(self)

    # Changer le classement du joueur
    def change_rank(self, new_rank):
        if new_rank > 0:
            self.rank = new_rank
            print("Nouveau classement : " + str(self.rank) + ".")
        else:
            print("Le classement doit être strictement positif.")

    def add_opponent(self, player):
        self.opponents.append(player)

    def show_opponents(self):
        for opponent in self.opponents:
            print(opponent.show_name(), end=" ")

    def show_name(self):
        return self.last_name

    def has_already_played_with(self, player):
        return player in self.opponents

    def has_already_played_with2(self, player):
        if player in self.opponents:
            print(self.last_name
                  + " et "
                  + player.show_name()
                  + " ont déjà joué ensemble.")
            return True
        else:
            print(self.last_name
                  + " et "
                  + player.last_name
                  + " n'ont pas joué ensemble.")
            return False

    def update_score(self, score):
        self.score = self.score + score

'''
print("------------------------ Test Player ---------------------------------")
# Créer des joueurs
playerA = Player("A", "", "15/12", "m", 100)
playerB = Player("B", "", "16/12", "f", 10)
playerC = Player("C", "", "23/10", "m", 34)

# Afficher les joueurs
print(str(playerA))
print(str(playerB))

# Changer le classement d'un joueur
playerA.change_rank(105)
playerB.change_rank(15)

playerB.add_opponent(playerA)
playerA.add_opponent(playerB)
playerA.show_opponents()
playerB.show_opponents()

playerA.has_already_played_with(playerB)
playerC.has_already_played_with(playerA)
'''