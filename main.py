import apiMethods.hangman
import apiMethods.scramble
import apiMethods.logic
import apiMethods.morse
import apiMethods.profanity
import apiMethods.llamas
import apiMethods.office

import builder, os

from database import database
from datetime import datetime
from flask import Flask, render_template, request, jsonify, url_for, send_file, after_this_request
from random import randint
from threading import Thread

# Keep track of ranges for seasons and number of episodes
parksSeasons = [6, 24, 16, 22, 22, 22, 13]
brooklynSeasons = [22, 23, 23, 22, 22, 18]

app = Flask("Fellow Hashbrown Website")

# # # # # # # # # # # # # # # # # # # # 
# Website Pages
# # # # # # # # # # # # # # # # # # # # 

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/archives")
def archives():
    return render_template("archives.html")

@app.route("/api")
def api():
    return render_template("api.html")

# # # # # # # # # # # # # # # # # # # # 
# Subpages    
# # # # # # # # # # # # # # # # # # # # 

# # # # # # # # # # # # # # # # # # # # 
# Error Pages
# # # # # # # # # # # # # # # # # # # # 

@app.errorhandler(404)
def page_not_found(error):
    return render_template("pageNotFound.html"), 404

# # # # # # # # # # # # # # # # # # # # 
# API Methods
# # # # # # # # # # # # # # # # # # # # 

@app.route("/api/hangman", methods = ["GET", "POST"])
def hangman():

    if request.method == "GET":
        return apiMethods.hangman.hangmanAPI()
    
    else:
        is_developer = request.headers.get("X-Fellow-Key", default = None, type = str) == os.environ["WEBSITE_API_KEY"]

        if is_developer:
            data = request.json

            if "difficulty" not in data or "phrase" not in data:
                result = {"success": False, "error": "There needs to be a difficulty and a phrase to add."}
                code = 400
            
            else:

                database.addHangman(data["difficulty"], data["phrase"])
                result = {"success": True, "value": "Phrase was added to the specified difficulty in Hangman."}
                code = 200
        
        else:
            result = {"success": False, "error": "You are not a developer and cannot add to this database."}
            code = 400
        
        return jsonify(result), code

@app.route("/api/scramble", methods = ["GET", "POST"])
def scramble():

    if request.method == "GET":
        return apiMethods.scramble.scrambleAPI()
    
    else:
        is_developer = request.headers["X-Fellow-Key"] == os.environ["WEBSITE_API_KEY"]

        if is_developer:
            data = request.json

            if "phrase" not in data or "hints" not in data:
                result = {"success": False, "error": "There needs to be a difficulty and a phrase to add."}
                code = 400
            
            else:

                database.addScramble(data["phrase"], data["hints"])
                result = {"success": True, "value": "Phrase was added in Scramble."}
                code = 200
        
        else:
            result = {"success": False, "error": "You are not a developer and cannot add to this database."}
            code = 400
        
        return jsonify(result), code
        

@app.route("/api/morse/encode", methods = ["GET"])
def morseEncode():
    text = request.args.get("text", default = None, type = str)
    return apiMethods.morse.encodeAPI(text)

@app.route("/api/morse/decode", methods = ["GET"])
def morseDecode():
    text = request.args.get("text", default = None, type = str)
    return apiMethods.morse.decodeAPI(text)

@app.route("/api/logic", methods = ["GET"])
def logic():
    expression = request.args.get("expression", default = None, type = str)
    compare = request.args.get("compare", default = None, type = str)

    as_table = request.args.get("table", default = False, type = bool)

    download = request.args.get("download", default = False, type = bool)
    raw = request.args.get("raw", default = False, type = bool)

    # See if user agent is connected
    has_user_agent = False
    for key in request.headers:
        if key[0].lower() == "user-agent":
            has_user_agent = True
            break

    # See if download or raw parameters exist
    # These should only be accessed by someone with a user-agent connected
    if (download or raw) and has_user_agent:
        response = apiMethods.logic.logicAPI(expression, None, True)[0].json

        # Create file
        filename = "static/logic_requests/logic_request_{}.txt".format(datetime.now().timestamp())
        temp = open(filename, "w")
        temp.write("\n".join(response["value"]))
        temp.close()

        # Delete the file afterwards; We don't want to keep it
        @after_this_request
        def remove_file(response):
            try:
                os.remove(filename)
            except Exception as e:
                print(str(e))
            return response

        # Send file for raw viewing
        if raw:
            return send_file(filename)
        
        # Send file for download
        return send_file(filename, as_attachment = True)

    return apiMethods.logic.logicAPI(expression, as_table = as_table)

@app.route("/api/profanity", methods = ["GET"])
def profanity():
    text = request.args.get("text", default = None, type = str)
    return apiMethods.profanity.profanityAPI(text)

@app.route("/api/llamas", methods = ["GET"])
def llamas():
    episode = request.args.get("episode", default = None, type = int)
    author = request.args.get("author", default = None, type = str)
    getAny = request.args.get("any", default = False, type = bool)
    fullScript = request.args.get("fullScript", default = False, type = bool)
    return apiMethods.llamas.llamasAPI(episode, author, getAny, fullScript)

@app.route("/api/office", methods = ["GET"])
def office():
    season = request.args.get("season", default = 0, type = int)
    episode = request.args.get("episode", default = 0, type = int)
    quoteType = request.args.get("type", default = "aired", type = str)
    return apiMethods.office.officeAPI(season, episode, quoteType)

# # # # # # # # # # # # # # # # # # # #
# Webhooks
# # # # # # # # # # # # # # # # # # # # 

# # # # # # # # # # # # # # # # # # # # 
# The Other Stuff
# # # # # # # # # # # # # # # # # # # # 

def run():
    app.run(host = "0.0.0.0", port = randint(1000, 9999))

def keepAlive():
    thread = Thread(target = run)
    thread.start()

keepAlive()