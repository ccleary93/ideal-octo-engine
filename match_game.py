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
        # TitleMatcher contains game lists, pass to TitleMatcher method
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
        # select the first database entry for the console where the date field is equal to 14 days prior
        cursor.execute(f"SELECT * FROM {console} WHERE date = '{past_date}' LIMIT 1;")
        # capture the primary key ID of this top result
        start_index = cursor.fetchall()[0][0]
        # return all entries with a PK > the start index
        cursor.execute(f"SELECT title, total_price, ebay_id FROM {console} WHERE id >= {start_index}")
        all_data = cursor.fetchall()
        return all_data

    def most_commonly_sold(self, sale_list):
        # iterate through the list of all sales and load a dict with name:number_of_sales
        count_dict = {}
        for item in sale_list:
            try:
                count_dict[item[0]] += 1
            except KeyError:
                count_dict[item[0]] = 1
        # sort the dict by the highest values
        top_dict = {key: value for key, value in sorted(count_dict.items(), key=lambda item: item[1], reverse=True)}
        top_titles = list(top_dict.keys())[:10]
        top_count = list(top_dict.values())[:10]
        # return the top ten
        top_dict = {top_titles[i]: top_count[i] for i in range(10)}
        return top_dict

    def highest_value(self,sale_list):
        # sort list by highest sale[1] (total_price in the database) field
        top_values = sorted(sale_list, key=lambda sale: sale[1], reverse=True)
        return top_values[:10]