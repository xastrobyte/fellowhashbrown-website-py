from flask import jsonify

charToMorse = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----."
}

morse_chars = [" ", "-", "."]

morseToChar = {v: k for k,v in charToMorse.items()}

def encodeAPI(text):
    if text:

        # Check if text is already morse code
        if len([char for char in text if char not in morse_chars]) == 0:
            result = {"error": "Cannot Encode Morse Code", "success": False}
            code = 400
        
        else:
    
            # Replace any %20 with spaces
            # Also upper() the text
            text = text.replace("%20", " ").upper()

            # Separate by words
            words = text.split(" ")

            # Convert text to morse code
            converted = ""
            for word in words:

                # Iterate through word
                for letter in word:
                    if letter in charToMorse:
                        converted += charToMorse[letter]
                    else:
                        converted += ""
                    converted += " "
                
                converted += " "
            
            result = {"value": converted.strip(), "success": True}
            code = 200
    
    else:
        result = {"error": "Cannot Encode Empty Text", "success": False}
        code = 400
    
    return jsonify(result), code

def decodeAPI(text):
    if text:

        # Check if text is not morse code
        if len([char for char in text if char not in morse_chars]) > 0:
            result = {"error": "Cannot Decode Regular Text", "success": False}
            code = 400
        
        else:

            # Replace any %20 with spaces
            text = text.replace("%20", " ")

            # Separate by letters
            letters = text.split(" ")

            # Convert morse code to text
            converted = ""
            for letter in letters:
                if len(letter) == 0:
                    converted += " "
                elif letter in morseToChar:
                    converted += morseToChar[letter]
            
            result = {"value": converted.strip().lower(), "success": True}
            code = 200
    
    else:
        result = {"error": "Cannot Decode Empty Text", "success": False}
        code = 400
    
    return jsonify(result), code