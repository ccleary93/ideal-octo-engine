from flask import Flask, render_template, request, redirect, url_for
from match_game import MatchGame
from data_cleanser import DataCleanser
from selected_game import SelectedGame
import math

app = Flask(__name__)

match_game = MatchGame()
data_cleanser = DataCleanser()
selected_game = SelectedGame()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    console = request.form["console"]
    game = request.form["game"]
    game = data_cleanser.remove_punctuation(game)
    selected_game.game = game
    selected_game.console = console
    matched_titles = match_game.match_game(selected_game.console, selected_game.game)
    if len(matched_titles) > 0:
        if len(matched_titles) == 1:
            rows = match_game.select_from_db(selected_game.console,matched_titles[0])
            rows.reverse()
            if len(rows) >= 15:
                mean_average = round(sum([row[5] for row in rows[:15]])/15,2)
                sorted_prices = sorted([row[5] for row in rows[:15]])
                median_average = round(sorted_prices[6], 2)
            elif len(rows) > 0:
                mean_average = round(sum([row[5] for row in rows]) / len(rows),2)
                sorted_prices = sorted([row[5] for row in rows])
                median_average = round(sorted_prices[math.floor(len(rows) / 2)])
            else:
                return render_template("error.html")
            return render_template("results.html", game=selected_game.game, console=selected_game.console, rows=rows, len_rows=len(rows), mean_average=mean_average, median_average=median_average)
        else:
            return render_template("multiple.html", matches=matched_titles)
    else:
        return render_template("error.html")

@app.route("/select", methods=["POST"])
def select():
    game = request.form["game"]
    print(game)
    selected_game.game = game
    rows = match_game.select_from_db(selected_game.console, selected_game.game)
    rows.reverse()
    if len(rows) > 0:
        if len(rows) >= 15:
            mean_average = round(sum([row[5] for row in rows[:15]]) / 15, 2)
            sorted_prices = sorted([row[5] for row in rows[:15]])
            print(sorted_prices)
            median_average = sorted_prices[6]
        else:
            mean_average = round(sum([row[5] for row in rows]) / len(rows), 2)
            sorted_prices = sorted([row[5] for row in rows])
            median_average = sorted_prices[math.floor(len(rows) / 2)]
        return render_template("results.html", game=selected_game.game, console=selected_game.console, rows=rows, len_rows=len(rows), mean_average=mean_average, median_average=median_average)
    else:
        return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True)