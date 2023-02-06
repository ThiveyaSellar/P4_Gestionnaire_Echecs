import datetime
from datetime import date
import time


def non_empty_input(msg):
    info = input(f"{msg} ")
    while info == "":
        info = input(f"{msg} ")
    return info


def ask_date(msg):
    chosen_date = input(msg + " (JJ/MM/AAAA) : ")
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

