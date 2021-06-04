from flask import Flask, render_template, url_for, redirect, request
from database import dbfunctions

# TO DO: Edit formatting

app = Flask(__name__)

def click():
    print("hello")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/personal", methods=["POST","GET"])
def stats():
    if request.method == "POST" and "nm" in request.form:
        name = request.form["nm"]
        if name == "":
            return render_template("search.html", users=[], len=0)
        users = dbfunctions.search_names(name)
        if not users:
            return render_template("search.html", users=[], len=0)
        return render_template("search.html", users=users, len=len(users))
    elif request.method == "POST" and "click" in request.form:
        return redirect(url_for('user_stats', user_id=request.form['click']))
    else:
        return render_template("search.html", users=[], len=0)

@app.route("/leaderboard")
def leaderboard():
    return render_template("stats.html", myfunction=dbfunctions.app_topboardgame(), len=len(dbfunctions.app_topboardgame()))

@app.route("/val")
def cash():
    return render_template("cash.html", myfunction=dbfunctions.app_topbal(), len=len(dbfunctions.app_topbal()))


@app.route("/personal/<user_id>")
def user_stats(user_id):
    games = dbfunctions.get_games()
    stats = []
    user = dbfunctions.get_user(user_id)
    total_stats = dbfunctions.total_boardgame_stats(user_id)
    for i in range(len(games)):
        stats.append(dbfunctions.get_stats(games[i][0], user_id))
    return render_template("personalStats.html", stats=stats, len=len(games), user=user, total_stats=total_stats)


if __name__ == "__main__":
    app.run(debug=True)
