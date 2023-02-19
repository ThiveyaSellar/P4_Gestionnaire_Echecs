from models.player import Player


class Match:

    def __init__(self, player_a, player_b, score_a=0, score_b=0):
        self.player_a = player_a
        self.player_b = player_b
        self.score_a = score_a
        self.score_b = score_b

    def __str__(self):
        return f"{self.match}"

    def get_player_a(self):
        return self.player_a

    def get_player_b(self):
        return self.player_b

    def get_score_a(self):
        return self.score_a

    def get_score_b(self):
        return self.score_b

    def add_score(self, score_a, score_b):
        self.score_a = score_a
        self.score_b = score_b

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
