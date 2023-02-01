import datetime
from datetime import date
import time


def non_empty_input(msg):
    info = input(f"{msg} ")
    while info == "":
        info = input(f"{msg} ")
    return info


def valid_date():
    # La date actuelle
    current_time = datetime.datetime.now()
    year = int(input("Saisir l'année : "))
    # Vérifier que l'année n'est pas dépassée
    while year < current_time.year:
        year = int(input("Saisir l'année : "))
    month = int(input("Saisir le mois : "))
    while month > 12 or month < 1:
        month = int(input("Saisir le mois : "))
    day = int(input('Saisir le jour : '))
    while day < 1 or day > 31:
        day = int(input("Saisir le jour : "))
    d = date(year, month, day)
    return d


def ask_date():
    chosen_date = input("Date (JJ/MM/AAAA) : ")
    chosen_date = datetime.datetime.strptime(chosen_date, "%d/%m/%Y").date()
    return chosen_date

def multiline_input():
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    text = '\n'.join(lines)
    return text
