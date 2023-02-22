from controllers.base import Controller
from views.base import View
from tinydb import TinyDB
from models.manager import Manager


def main():
    # db = TinyDB('chess_db.json')
    db = TinyDB(
        'chess_db.json',
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    )
    # Récupérer tous les joueurs
    players = db.table('players').all()
    # Récupérer tous les tournois
    tournaments = db.table('tournaments').all()
    manager = Manager(players, tournaments)
    view = View()
    chess_management = Controller(db, manager, view)
    chess_management.run()


if __name__ == "__main__":
    main()
