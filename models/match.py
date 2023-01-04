class Match:

    def __init__(self, player_a, player_b, score_a=0, score_b=0):
        self.player_a = player_a
        self.player_b = player_b
        self.score_a = score_a
        self.score_b = score_b
        # self.match = tuple()

    def __str__(self):
        return f"{self.match}"

    def add_score(self, score_a, score_b):
        self.score_a = score_a
        self.score_b = score_b


        '''self.match = (
            [self.player_a, self.score_a], [self.player_b, self.score_b]
        )'''

    def show_infos(self):
        print(self.player_a.show_name() + " vs " + self.player_b.show_name())

    def serialize(self):
        match = {
            "player_a": self.player_a,
            "player_b": self.player_b,
            "score_a": self.score_a,
            "score_b": self.score_b
        }
        return match

    @staticmethod
    def deserialize_match(serialized_match):
        player_a = serialized_match["player_a"]
        player_b = serialized_match["player_b"]
        score_a = serialized_match["score_a"]
        score_b = serialized_match["score_b"]
        match = Match(player_a, player_b, score_a, score_b)
        return match
