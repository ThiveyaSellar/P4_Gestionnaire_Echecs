import datetime
from datetime import date
import time


def non_empty_input(msg):
    info = input(f"{msg} \n")
    while info == "":
        info = input(f"{msg} \n")



def valid_date():
    current_time = datetime.datetime.now()
    year = int(input("Saisir l'année :"))
    while year < current_time.year:
        year = int(input("Saisir l'année :"))
    month = int(input("Saisir le mois :"))
    while month > 12 or month < 1:
        month = int(input("Saisir le mois :"))
    day = int(input('Enter a day: '))

    d = date(year, month, day)
    print(d)
