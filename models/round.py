from datetime import datetime


class Round:

    def __init__(self, name):
        self.name = name
        self.matchs = []
        self.start_date_time = datetime.now().strftime("%d/%m/%Y à %H:%M")
        self.end_date_time = ""

    def show_status(self):
        print("Début : ")
        print(self.start_date_time)
        if self.end_date_time == "":
            print("Le round est en cours.")
        else:
            print("Fin : ")
            print(self.end_date_time)

    def add_match(self, match):
        self.matchs.append(match)

    def stop_round(self):
        self.end_date_time = datetime.now().strftime("%d/%m/%Y à %H:%M")

    def show_matchs(self):
        for match in self.matchs:
            match.show_infos()

    def show_name(self):
        return self.name


