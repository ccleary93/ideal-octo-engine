import psycopg2
import os
from title_matcher import TitleMatcher
import datetime

current_date = datetime.datetime.now().date()
past = datetime.timedelta(days=14)
past_date = (current_date - past).strftime('%d/%m/%Y')

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

    def load_last_14_days(self, console):
        db = psycopg2.connect(f"dbname={os.environ['DB_NAME']} user={os.environ['DB_USER']} host={os.environ['DB_ADDRESS']} port=5432 password={os.environ['DB_PASSWORD']}")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM {console} WHERE date = '{past_date}' LIMIT 1;")
        start_index = cursor.fetchall()[0][0]
        cursor.execute(f"SELECT title, total_price, ebay_id FROM {console} WHERE id >= {start_index}")
        all_data = cursor.fetchall()
        return all_data

    def most_commonly_sold(self, sale_list):
        count_dict = {}
        for item in sale_list:
            try:
                count_dict[item[0]] += 1
            except KeyError:
                count_dict[item[0]] = 1
        top_dict = {key: value for key, value in sorted(count_dict.items(), key=lambda item: item[1], reverse=True)}
        top_titles = list(top_dict.keys())[:10]
        top_count = list(top_dict.values())[:10]
        top_dict = {top_titles[i]: top_count[i] for i in range(10)}
        return top_dict

    def highest_value(self,sale_list):
        top_values = sorted(sale_list, key=lambda sale: sale[1], reverse=True)
        #top_values = [sale for sale in sorted(sale_list, key=sale[1], reverse=True)]
        # highest_value = [sale for sale in sale_list[0:10]]
        # value_dict = {item: item[1] for item in sale_list}
        return top_values[:10]