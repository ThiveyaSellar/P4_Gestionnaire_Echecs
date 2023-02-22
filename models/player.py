class Player:

    def __init__(self, last_name, first_name, birth_date, gender, rank):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.gender = gender
        self.rank = rank
        self.score = 0
        self.opponents = []

    """def __str__(self):
        return f"{self.last_name}"""

    def get_last_name(self):
        return self.last_name

    def get_first_name(self):
        return self.first_name

    def get_names(self):
        return self.first_name + " " + self.last_name

    def get_rank(self):
        return self.rank

    def add_opponent(self, player):
        self.opponents.append(player.rank)

    def add_opponent_in_deserialize(self, rank):
        self.opponents.append(rank)

    def has_already_played_with(self, player):
        return player.rank in self.opponents

    def update_score(self, score):
        self.score = self.score + score

    def serialize(self):
        player = {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "rank": self.rank,
            "score": self.score,
            "opponents": self.opponents
        }
        return player

    @staticmethod
    def deserialize_player(serialized_player):
        last_name = serialized_player["last_name"]
        first_name = serialized_player["first_name"]
        birth_date = serialized_player["birth_date"]
        gender = serialized_player["gender"]
        rank = serialized_player["rank"]
        score = serialized_player["score"]
        opponents = serialized_player["opponents"]

        player = Player(
            last_name,
            first_name,
            birth_date,
            gender,
            rank
        )

        player.update_score(score)
        for o in opponents:
            player.add_opponent_in_deserialize(o)
        return player
