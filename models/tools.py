import datetime
from datetime import date
import time


def non_empty_input(msg):
    info = input(f"{msg} \n")
    while info == "":
        info = input(f"{msg} \n")


def valid_date():
    # La date actuelle
    current_time = datetime.datetime.now()
    year = int(input("Saisir l'année :"))
    # Vérifier que l'année n'est pas dépassée
    while year < current_time.year:
        year = int(input("Saisir l'année : \n"))
    month = int(input("Saisir le mois :"))
    while month > 12 or month < 1:
        month = int(input("Saisir le mois : \n"))
    day = int(input('Enter a day: '))
    while day < 1 or day > 31:
        day = int(input("Saisir le jour : \n"))
    d = date(year, month, day)
    return d


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