from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"

    winner = None

    for ses in session["board"]:
        if ses[0] == ses[1] == ses[2] and ses[0] != None and ses[1] != None and ses[2] != None:
            winner = ses[0]
            return render_template("game.html", game=session["board"], turn=session["turn"], winner=winner)
    
    for i in range(3):
        if (session["board"][0][i] == session["board"][1][i] == session["board"][2][i]) and session["board"][0][i] != None and session["board"][1][i] != None and session["board"][2][i] != None:
            winner = session["board"][0][i]
            return render_template("game.html", game=session["board"], turn=session["turn"], winner=winner)

    if (session["board"][0][0] == session["board"][1][1] == session["board"][2][2]) and session["board"][0][0] != None and session["board"][1][1] != None and session["board"][2][2] != None:
        winner = session["board"][0][0]

    if (session["board"][0][2] == session["board"][1][1] == session["board"][2][0]) and session["board"][0][2] != None and session["board"][1][1] != None and session["board"][2][0] != None:
        winner = session["board"][0][2]

    return render_template("game.html", game=session["board"], turn=session["turn"], winner=winner)

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    session["board"][row][col] = session["turn"]
    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    session.clear()
    return redirect("/")