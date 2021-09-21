import os
from ebaysdk.finding import Connection as finding
from datetime import timedelta, datetime as dt
import psycopg2
from title_matcher import TitleMatcher
from data_cleanser import DataCleanser
import math

title_matcher = TitleMatcher()
data_cleanser = DataCleanser()

class SnipeUpcoming:
    def __init__(self):
        self.consoles = {
            "PLAYSTATION 2":"PS2",
            "PS2":"PS2",
            "PLAYSTATION 3":"PS3",
            "PS3":"PS3",
            "PS4":"PS4",
            "PLAYSTATION 4":"PS4",
            "XBOX ONE":"XBOX ONE",
            "XBOX 360":"XBOX 360",
            "GAMECUBE":"GAMECUBE"
        }
        self.api = finding(siteid='EBAY-GB', appid=str(os.environ["EBAY_API_KEY"]), config_file=None)
        self.database_schema = {
            "PS4":"ps4",
            "PS3":"ps3",
            "PS2":"ps2",
            "XBOX ONE":"xbox_one",
            "XBOX 360":"xbox_360",
            "GAMECUBE":"gamecube"
        }

    def find_upcoming(self):
        now = dt.now() - timedelta(minutes=60)
        in_fifteen_mins = now + timedelta(minutes=15)
        continue_call = True
        pgn = 1
        game_list = []

        while continue_call:
            self.api.execute('findItemsAdvanced', {
                'categoryId': ['139973'],
                'itemFilter': [
                    {'name': 'ListingType', 'value': 'Auction'},
                    {'name': 'LocatedIn', 'value': 'GB'}
                ],
                'paginationInput': {
                    'entriesPerPage': '100',
                    'pageNumber': str(pgn)
                },
                'sortOrder': 'EndTimeSoonest'
            })

            dictstr = self.api.response_dict()
            search_result = dictstr.searchResult

            for result in dictstr.searchResult.item:
                if result.listingInfo.endTime > in_fifteen_mins:
                    break
                stripped_description = data_cleanser.remove_punctuation(result.title)
                for console in self.consoles.keys():
                    if result.title.lower().find(console.lower()) >= 0:
                        game_list.append({"description": stripped_description,
                                  "console": self.consoles[console],
                                  "price": float(result.sellingStatus.convertedCurrentPrice.value),
                                  "postage": float(result.shippingInfo.shippingServiceCost.value),
                                  "total_price": round(float(result.sellingStatus.convertedCurrentPrice.value) +
                                                 float(result.shippingInfo.shippingServiceCost.value),2),
                                  "ebay_id": result.itemId,
                                  "end_time": result.listingInfo.endTime,
                                  "title": ""
                                  })
                        break

            pgn += 1
            if in_fifteen_mins < dictstr.searchResult.item[99].listingInfo.endTime:
                continue_call = False

        for console in self.consoles.keys():
            #iterate over consoles, then create list of found games for that console
            for game in [game for game in game_list if game["console"] == console]:
                # match game method adds the 'title' field to the game
                title_matcher.match_game(game)

        # only return items that have been correctly matched to a title
        game_list = [game for game in game_list if game["title"] != ""]
        return game_list

    def find_average(self, game):
        db = psycopg2.connect(
            f"dbname={os.environ['DB_NAME']} user={os.environ['DB_USER']} host={os.environ['DB_ADDRESS']} port=5432 password={os.environ['DB_PASSWORD']}")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM {self.database_schema[game['console']]} WHERE title = '{game['title']}'")
        rows = cursor.fetchall()
        rows.reverse()
        if len(rows) >= 15:
            game['mean_average'] = round(sum([row[5] for row in rows[:15]]) / 15, 2)
            sorted_prices = sorted([row[5] for row in rows[:15]])
            game['median_average'] = round(sorted_prices[6], 2)
            game['num_results'] = len(rows)
            game['results'] = rows[:15]
        elif len(rows) > 0:
            game['mean_average'] = round(sum([row[5] for row in rows]) / len(rows), 2)
            sorted_prices = sorted([row[5] for row in rows])
            game['median_average'] = round(sorted_prices[math.floor(len(rows) / 2)])
            game['num_results'] = len(rows)
            game['results'] = rows
        else:
            game['mean_average'] = 0
            game['median_average'] = 0
        return game

    def current_below_average(self, game):
        if game['mean_average'] > game['total_price'] or game['median_average'] > game['total_price']:
            return True
        else:
            return False