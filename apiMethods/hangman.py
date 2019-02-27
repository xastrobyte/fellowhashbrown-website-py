from database import database
from flask import jsonify

def hangmanAPI():
    result = database.getHangmanWordSync()
    result["success"] = True
    code = 200
    
    return jsonify(result), code