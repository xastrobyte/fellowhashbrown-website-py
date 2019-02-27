from database import database
from flask import jsonify
from random import randint, choice

validAuthors = ["Paul", "Carl", "Sheep", "", "Paul mask", "Paul Mask"]

def llamasAPI(episode = None, author = None, getAny = False, fullScript = False):

    # Check if getting full script
    if fullScript:
        print("full")

        # check if episode is None
        if episode == None:
            result = {
                "success": False,
                "error": "No Episode Given."
            }
            code = 400
        
        # episode is not None
        else:
            episode = database.getLlamasScript(episode)
            episode["success"] = True
            result = episode
            code = 200
    
    # Check if getting quote
    else:
        print("single")

        # episode is None, choose random episode
        if episode == None:
            episode = randint(1, 12)

        # Make sure episode is within range
        if episode >= 1 and episode <= 12:

            # author is not None, make sure it's valid
            if author != None:
                if author not in validAuthors:
                    result = {
                        "success": False,
                        "error": "Invalid Author"
                    }
                    code = 400
                
                else:
                    
                    quote = database.getLlamasQuote(episode)
                    while (quote["author"] != author and author != None) or (not quote["ignore"] and not getAny):
                        quote = database.getLlamasQuote(episode)
                    
                    result = {
                        "success": True,
                        "value": quote["value"],
                        "author": quote["author"]
                    }
                    code = 200
            
            # author is None, choose from valid
            else:
                author = choice(validAuthors)
        
                quote = database.getLlamasQuote(episode)
                while (quote["author"] != author) and (quote["ignore"] and not getAny):
                    quote = database.getLlamasQuote(episode)
                
                result = {
                    "success": True,
                    "episode": episode,
                    "image": quote["image"],
                    "value": quote["value"],
                    "author": quote["author"]
                }
                code = 200
        
        # Episode is invalid
        else:
            result = {
                "success": False,
                "error": "Invalid Episode"
            }
            code = 400
    
    return jsonify(result), code