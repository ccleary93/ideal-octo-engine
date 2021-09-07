import sqlite3
from title_matcher import TitleMatcher

class MatchGame():
    def __init__(self):
        self.title_matcher = TitleMatcher()

    def match_game(self, console, game):
        return self.title_matcher.check_match(game,console)

    def select_from_db(self, console, game):
        print(console)
        db = sqlite3.connect(<ROUTE TO DB HERE>)
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM {console} WHERE title = '{game}'")
        rows = cursor.fetchall()
        return rows