from database import database
from flask import jsonify

def scrambleAPI():
    return jsonify(database.getScrambleWordSync()), 200