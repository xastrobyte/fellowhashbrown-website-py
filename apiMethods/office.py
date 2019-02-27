from database import database
from flask import jsonify
from random import randint

officeSeasons = [6, 22, 23, 14, 26, 24, 24, 24, 23]

def officeAPI(season, episode, quoteType):
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