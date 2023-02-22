from datetime import datetime
from models.match import Match


class Round:

    def __init__(
            self,
            name,
            start_date_time=datetime.now().strftime("%d/%m/%Y à %H:%M"),
            end_date_time=""
    ):
        self.name = name
        self.matchs = []
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time

    def get_name(self):
        return self.name

    def get_matchs(self):
        return self.matchs

    def add_match(self, match):
        self.matchs.append(match)

    def get_start_date_time(self):
        return self.start_date_time

    def get_end_date_time(self):
        return self.end_date_time

    def stop_round(self):
        self.end_date_time = datetime.now().strftime("%d/%m/%Y à %H:%M")

    def serialize(self):
        serialized_matchs = []
        for match in self.matchs:
            serialized_matchs.append(match.serialize())

        round = {
            'name': self.name,
            'matchs': serialized_matchs,
            'start_date_time': self.start_date_time,
            'end_date_time': self.end_date_time
        }
        return round

    @staticmethod
    def deserialize_round(serialized_round):
        name = serialized_round['name']
        start_date_time = serialized_round['start_date_time']
        end_date_time = serialized_round['end_date_time']

        round = Round(name, start_date_time, end_date_time)
        for match in serialized_round['matchs']:
            round.add_match(Match.deserialize_match(match))
        return round
