from datetime import datetime


class Round:

    def __init__(self, name):
        self.name = name
        self.matchs = []
        self.start_date_time = datetime.now().strftime("%d/%m/%Y à %H:%M")
        self.end_date_time = ""

    def show_status(self):
        print("Start time : ")
        print(self.start_date_time)
        if self.end_date_time == "":
            print("Le round est en cours")
        else:
            print("End time : ")
            print(self.end_date_time)

    def add_match(self, match):
        self.matchs.append(match)

    def stop_round(self):
        self.end_date_time = datetime.now().strftime("%d/%m/%Y à %H:%M")


print("------------------------ Test Round ---------------------------------")
tour = Round("Round 1")
scoreA = 1
scoreB = 0
match = (["joueurA", scoreA],["joueur2", scoreB])
tour.add_match(match)
tour.show_status()