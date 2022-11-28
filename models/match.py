class Match:

    def __init__(self, player_a, player_b):
        self.player_a = player_a
        self.player_b = player_b
        self.score_a = 0
        self.score_b = 0
        self.finished = False
        self.match = tuple()

    def __str__(self):
        return f"{self.match}"

    def add_score(self, score_a, score_b):
        self.score_a = score_a
        self.score_b = score_b
        self.match = (
            [self.player_a, self.score_a], [self.player_b, self.score_b]
        )
        self.finished = True

    def show_infos(self):
        print(self.player_a.show_name() + " vs " + self.player_b.show_name())
'''
print("------------------------ Test Match ---------------------------------")
match = Match("joueur1", "joueur2")
print(match)
match.add_score(1, 0)
print(match)
'''

