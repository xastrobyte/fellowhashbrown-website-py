from database import database

from flask import Flask, render_template, request, jsonify, url_for
from random import randint
from threading import Thread

# Keep track of ranges for seasons and number of episodes
officeSeasons = [6, 22, 23, 14, 26, 24, 24, 24, 23]
parksSeasons = [6, 24, 16, 22, 22, 22, 13]
brooklynSeasons = [22, 23, 23, 22, 22, 18]


app = Flask("Fellow Hashbrown Website")

# # # # # # # # # # # # # # # # # # # # 
# Website Pages
# # # # # # # # # # # # # # # # # # # # 

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/api")
def api():
    return render_template("api.html")

# # # # # # # # # # # # # # # # # # # # 
# Subpages    
# # # # # # # # # # # # # # # # # # # # 

@app.route("/projects/omegaPsi")
def omegaPsi():
    return render_template("projects/omegaPsi.html")

# # # # # # # # # # # # # # # # # # # # 
# API Methods
# # # # # # # # # # # # # # # # # # # # 

@app.route("/api/hangman", methods = ["GET"])
def hangman():
    difficulty = request.args.get("difficulty", default = "easy", type = str)

    if difficulty not in ["easy", "medium", "hard", "random"]:
        result = {
            "success": False,
            "error": "Invalid Difficulty"
        }
        code = 400

    else:

        if difficulty == "random":
            difficulty = "easy"
            
        result = database.getHangmanWordSync(difficulty)
        result["success"] = True
        code = 200

    return jsonify(result), code

@app.route("/api/scramble", methods = ["GET"])
def scramble():
    return jsonify(database.getScrambleWordSync()), 200

@app.route("/api/morse/encode", methods = ["GET"])
def morseEncode():
    result = {
        "success": False,
        "error": "Not Implemented Yet"
    }
    return jsonify(result), 400

@app.route("/api/morse/decode", methods = ["GET"])
def morseDecode():
    result = {
        "success": False,
        "error": "Not Implemented Yet"
    }
    return jsonify(result), 400


@app.route("/api/office", methods = ["GET"])
def officeQuotes():
    season = request.args.get("season", default = 0, type = int)
    episode = request.args.get("episode", default = 0, type = int)
    quoteType = request.args.get("type", default = "aired", type = str)

    code = 200

    # Check if season does not exist
    if season == 0:

        # Check if episode does not exist
        if episode == 0:

            # Choose random season and random episode from season
            season = randint(1, 9)
            episode = randint(1, officeSeasons[season - 1])
        
        # Episode does exist; Throw 409 status
        else:
            result = {
                "success": False,
                "error": "Season not given. Episode was."
            }
            code = 400
    
    # Check if season exists
    else:

        # Make sure season is within range
        if season >= 1 and season <= 9:

            # Check if episode does not exist
            if episode == 0:

                # Choose random episode
                episode = randint(1, officeSeasons[season - 1])
            
            # Episode does exist
            else:

                # See if it is out of range; Throw 404 status
                if episode < 1 or episode > officeSeasons[season - 1]:
                    result = {
                        "success": False,
                        "error": "Invalid Episode."
                    }
                    code = 400
        
        # Season is out of range; Throw 416 status
        else:
            result = {
                "success": False,
                "error": "Invalid Season."
            }
            code = 400

    # Only run if error wasn't made
    if code == 200:

        # Validate quote type; Throw 400 status
        quoteTypes = ["deleted", "aired", "any"]
        if quoteType not in quoteTypes:
            result = {
                "success": False,
                "error": "Invalid Quote Type."
            }
            code = 400
        
        # Quote type was valid
        else:

            # Get quote
            result = database.getOfficeQuoteSync(season, episode, quoteType)
            result["success"] = True
            code = 200
    
    return jsonify(result), code

# # # # # # # # # # # # # # # # # # # # 
# The Other Stuff
# # # # # # # # # # # # # # # # # # # # 

def run():
    app.run(host = "0.0.0.0", port = 3000)

def keepAlive():
    thread = Thread(target = run)
    thread.start()

keepAlive()