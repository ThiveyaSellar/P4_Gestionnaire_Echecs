from models.player import Player

class Match:

    def __init__(self, player_a, player_b, score_a=0, score_b=0):
        self.player_a = player_a
        self.player_b = player_b
        self.score_a = score_a
        self.score_b = score_b

    def __str__(self):
        return f"{self.match}"

    def add_score(self, score_a, score_b):
        self.score_a = score_a
        self.score_b = score_b

    def show_infos(self):
        print(
            self.player_a.show_name()
            + " vs "
            + self.player_b.show_name()
        )

    def show_match_winner(self):
        if (self.score_a or self.score_b) == 1.0:
            score_a = str(int(self.score_a))
            score_b = str(int(self.score_b))
        else:
            score_a = str(self.score_a)
            score_b = str(self.score_b)

        if self.score_a == 0.5:
            msg = "match nul"
        elif self.score_a == 1.0:
            msg = "gagnant: " + self.player_a.show_name()
        else:
            msg = "gagnant: " + self.player_b.show_name()

        print(
            self.player_a.show_name()
            + " vs "
            + self.player_b.show_name()
            + "\t\t"
            + msg
        )

    def serialize(self):
        player_a = self.player_a.serialize()
        player_b = self.player_b.serialize()
        match = {
            "player_a": player_a,
            "player_b": player_b,
            "score_a": self.score_a,
            "score_b": self.score_b
        }
        return match

    @staticmethod
    def deserialize_match(serialized_match):
        player_a = Player.deserialize_player(serialized_match["player_a"])
        player_b = Player.deserialize_player(serialized_match["player_b"])
        score_a = serialized_match["score_a"]
        score_b = serialized_match["score_b"]
        match = Match(player_a, player_b, score_a, score_b)
        return match
