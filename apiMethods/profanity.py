from flask import jsonify

charDict = {
    "a": "a4@",
    "b": "b8&",
    "c": "c(",
    "d": "d)",
    "e": "e3\u03a3",
    "f": "f",
    "g": "g6",
    "h": "h",
    "i": "i1|",
    "j": "j",
    "k": "k",
    "l": "l",
    "m": "m",
    "n": "n",
    "o": "o0",
    "p": "p",
    "q": "q",
    "r": "r",
    "s": "s$5",
    "t": "t7",
    "u": "u",
    "v": "v",
    "w": "w",
    "x": "x",
    "y": "y",
    "z": "z"
}

PROFANE_WORDS = [
    "asshole",
    "bastard",
    "bitch",
    "cock",
    "dick",
    "cunt", 
    "pussy",
    "fuck", 
    "shit", 
    "chode", 
    "choad", 
    "wanker", 
    "twat", 
    "nigger", 
    "nigga",
    "jizz", 
    "dildo", 
    "douche"
]

def profanityAPI(text):
    if text == None:
        result = {
            "success": False,
            "error": "Cannot Filter Empty Text."
        }
        code = 400
    
    else:
        text = text.lower()
        word = ""
        for letter in text:
            for char in charDict:
                if letter == char or letter in charDict[char]:
                    word += char
                    break
        
        if word in PROFANE_WORDS:
            result = {
                "success": True,
                "profane": True,
                "likely_word": word
            }
            code = 200
        else:
            result = {
                "success": True,
                "profane": False
            }
            code = 200
    
    return jsonify(result), code