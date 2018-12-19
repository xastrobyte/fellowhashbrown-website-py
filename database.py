from pymongo import MongoClient
from random import choice
import asyncio, os

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
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Hangman
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    def __get_hangman_words(self, difficulty = None):
        """A helper method to get the words in the API.
        """

        if difficulty == None:
            words = []
            for difficulty in ["easy", "medium", "hard"]:
                words.append(self.__get_hangman_words(difficulty))

        else:
            words = self._data.find_one({"_id": "hangman"})[difficulty]

        return words
    
    async def getHangmanWords(self, difficulty = None):
        """Gets the hangman words in the API.

        Parameters:
            difficulty (str): The specific difficulty to get the words for.
        """
        return await loop.run_in_executor(None, self.__get_hangman_words, difficulty)
    
    async def getHangmanWord(self, difficulty = None):
        """Returns a random word from the specified difficulty.

        Parameters:
            difficulty (str): The specified difficulty to get the words for. (Defaults to easy)
        """

        if difficulty == None:
            difficulty = "easy"

        words = await self.getHangmanWords(difficulty)
        return choice(words)
    
    def getHangmanWordsSync(self, difficulty = None):
        """Gets the hangman words in the API.

        Parameters:
            difficulty (str): The specific difficulty to get the words for.
        """
        return self.__get_hangman_words(difficulty)

    def getHangmanWordSync(self, difficulty = None):
        """Returns a random word from the specified difficulty.

        Parameters:
            difficulty (str): The specified difficulty to get the words for. (Defaults to easy)
        """

        if difficulty == None:
            difficulty = "easy"
        
        words = self.getHangmanWordsSync(difficulty)
        return choice(words)
    
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
    
    def getScrambleWordsSync(self, difficulty = None):
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

database = Database()