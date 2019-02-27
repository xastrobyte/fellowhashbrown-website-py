from pymongo import MongoClient
from random import choice
import asyncio, base64, os

# Create event loop
loop = asyncio.get_event_loop()

class Database:

    def __init__(self):
        """Initializes the Database to be used.
        """

        # Create the Connection and Get the Database from Omega Psi
        self._omegaPsiConnection = MongoClient("ds115244.mlab.com", 15244, connect = False)
        self._omegapsi = self._omegaPsiConnection["omegapsi"]

        # Get the username and password to authenticate database access
        username = os.environ["DATABASE_USERNAME"]
        password = os.environ["DATABASE_PASSWORD"]
        self._omegapsi.authenticate(username, password)

        # Keep track of data
        self._data = self._omegapsi.data

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #    

        # Create the Connection and Get the Database from Quotes
        self._quotesConnection = MongoClient("ds151973.mlab.com", 51973, connect = False)
        self._quotes = self._quotesConnection["quotes"]

        # Get the username and password to authenticate database access
        username = os.environ["DATABASE_USERNAME"]
        password = os.environ["DATABASE_PASSWORD"]
        self._quotes.authenticate(username, password)

        # Keep track of The Office Quotes
        self._theOffice = self._quotes.theOffice

        # Keep track of Llamas With Hats Quotes
        self._llamasWithHats = self._quotes.llamasWithHats
    
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # Create the Connection and Get the Database from Website
        self._websiteConnection = MongoClient("ds159574.mlab.com", 59574, connect = False)
        self._website = self._websiteConnection["website"]

        # Get the username and password to authenticate database access
        username = os.environ["WEBSITE_USERNAME"]
        password = os.environ["WEBSITE_PASSWORD"]
        self._website.authenticate(username, password)

        # Keep track of 2054 data
        self._moderators = self._website.moderators
        self._subscriptions = self._website.subscriptions
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Hangman
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    def __get_hangman_words(self):
        """A helper method to get the words in the API.
        """

        words = self._data.find_one({"_id": "hangman"})

        return words["words"]
    
    async def getHangmanWords(self):
        """Gets the hangman words in the API.

        Parameters:
            difficulty (str): The specific difficulty to get the words for.
        """
        return await loop.run_in_executor(None, self.__get_hangman_words)
    
    async def getHangmanWord(self):
        """Returns a random word from the specified difficulty.

        Parameters:
            difficulty (str): The specified difficulty to get the words for. (Defaults to easy)
        """

        words = await self.getHangmanWords()
        return choice(words)
    
    def getHangmanWordsSync(self):
        """Gets the hangman words in the API.

        Parameters:
            difficulty (str): The specific difficulty to get the words for.
        """
        return self.__get_hangman_words()

    def getHangmanWordSync(self):
        """Returns a random word from the specified difficulty.

        Parameters:
            difficulty (str): The specified difficulty to get the words for. (Defaults to easy)
        """
        words = self.getHangmanWordsSync()
        return choice(words)
    
    def setHangmanWordsSync(self, words):
        self._data.update_one({"_id": "hangman"}, {"$set": {"words": words}}, upsert = False)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Scramble
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __get_scramble_words(self):
        """A helper method to get the words in the API.
        """
        words = self._data.find_one({"_id": "scramble"})["words"]
        return words
    
    async def getScrambleWords(self):
        """Gets the scramble words in the API.
        """
        return await loop.run_in_executor(None, self.__get_scramble_words)
    
    async def getScrambleWord(self):
        """Returns a random word from the specified difficulty.
        """
        words = await self.getScrambleWords()
        return choice(words)
    
    def getScrambleWordsSync(self):
        """Gets the hangman words in the API.

        Parameters:
            difficulty (str): The specific difficulty to get the words for.
        """
        return self.__get_scramble_words()

    def getScrambleWordSync(self):
        """Returns a random word from the specified difficulty.
        """
        words = self.getScrambleWordsSync()
        return choice(words)
    
    def setScrambleWordsSync(self, words):
        self._data.update_one({"_id": "scramble"}, {"$set": {"words": words}}, upsert = False)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Llamas With Hats
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __get_llamas_script(self, episodeNumber):
        """A helper method to get the script for an episode in the API.
        """
        script = self._llamasWithHats.find_one({"_id": f"episode{episodeNumber}"})
        script.pop("_id")
        return script

    def __get_llamas_quote(self, episodeNumber):
        """A helper method to get a quote from an episode in the API.
        """
        script = self.__get_llamas_script(episodeNumber)
        quote = choice(script["quotes"])
        quote["image"] = script["image"]
        return quote

    def getLlamasScript(self, episodeNumber):
        """Returns the script for an episode
        """
        return self.__get_llamas_script(episodeNumber)
    
    def getLlamasQuote(self, episodeNumber):
        """Returns a quote for an episode
        """
        return self.__get_llamas_quote(episodeNumber)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # The Office
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __get_office_quotes(self, season, episode):
        """A helper method to get The Office quotes from a specific season and episode in the API.
        """
        season = self._theOffice.find_one({"_id": f"season{season}"})
        return season["episodes"][episode - 1]["quotes"]
    
    async def getOfficeQuotes(self, season, episode):
        """Gets The Office quotes from a specific season and episode in the API.
        """
        return await loop.run_in_executor(None, self.__get_office_quotes, season, episode)
    
    async def getOfficeQuote(self, season, episode, quoteType = "aired"):
        """Returns a random The Office quote from a specific season and episode in the API.
        """
        quotes = await self.getOfficeQuotes(season, episode)
        quote = choice(quotes)
        while quote["deleted"] and quoteType == "aired":
            quote = choice(quotes)
        return quote
    
    def getOfficeQuotesSync(self, season, episode):
        """Gets The Office quotes from a specific season and episode in the API.

        Parameters:
            season (int): The season to get the quotes from.
            episode (int): The episode to get the quotes from.
        """
        return self.__get_office_quotes(season, episode)
    
    def getOfficeQuoteSync(self, season, episode, quoteType = "aired"):
        """Gets a random The Office quote from a specific season and episode in the API.
        """
        quotes = self.getOfficeQuotesSync(season, episode)
        quote = choice(quotes)
        if quoteType == "deleted":
            while not quote["deleted"]:
                quote = choice(quotes)
        else:
            while quote["deleted"] and quoteType == "aired":
                quote = choice(quotes)
        return quote

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Parks and Rec
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Brooklyn 99
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Moderators
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def getModerators(self):
        """Gets a list of moderators that can access the inner website.
        """

        # Get list of moderators
        moderators = self._moderators.find_one({"_id": "moderators"})
        if moderators == None:
            moderators = {"moderators": {}}
            self._moderators.insert_one({"_id": "moderators"})
            self.setModerators(moderators)
        
        return moderators
    
    def setModerators(self, moderators):
        """Sets the list of moderators that can access the inner website.
        """

        # Set list of moderators
        self._moderators.update_one({"_id": "moderators"}, {"$set": moderators}, upsert = False)
    
    def isModerator(self, authentication):
        """Determines whether or not the authentication given is a valid user who can access the inner website.
        """

        # Get moderators
        moderators = self.getModerators()

        # Remove Basic from the authentication
        authentication = authentication[len("Basic"):]

        # Decrypt from Base64
        authentication = base64.b64decode(authentication.encode()).decode()

        # Get username and password
        colon = authentication.find(":")
        username = authentication[:colon]
        password = authentication[colon + 1:]

        # See if username exists as a moderator
        if username in moderators:
            return moderators[username] == password
        
        return False

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Add Hangman
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def addHangman(self, difficulty, phrase):

        # Get hangman words
        hangmanWords = self.getHangmanWordsSync(difficulty)

        # Add hangman word to list
        hangmanWords.append({
            "value": phrase,
            "level": difficulty
        })

        # Update hangman words
        self.setHangmanWordsSync(difficulty, hangmanWords)
    
    def addScramble(self, phrase, hints):

        # Get scramble words
        scrambleWords = self.getScrambleWordsSync()

        # Add scramble word to list
        scrambleWords.append({
            "value": phrase,
            "hints": hints
        })

        # Update scramble words
        self.setScrambleWordsSync(scrambleWords)

database = Database()