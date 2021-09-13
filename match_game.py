import psycopg2
import os
from title_matcher import TitleMatcher

class MatchGame():
    def __init__(self):
        self.title_matcher = TitleMatcher()

    def match_game(self, console, game):
        return self.title_matcher.check_match(game,console)

    def select_from_db(self, console, game):
        db = psycopg2.connect(f"dbname={os.environ['DB_NAME']} user={os.environ['DB_USER']} host={os.environ['DB_ADDRESS']} port=5432 password={os.environ['DB_PASSWORD']}")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM {console} WHERE title = '{game}'")
        rows = cursor.fetchall()
        return rows