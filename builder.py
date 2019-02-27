from website.website import Website
from website.page import Page, Credit
from website.section import Section, Extra
from website.apisection import APISection, Parameter, Response

def jsonToHTML(obj, depth = 1):

	result = ""

	if type(obj) == bool:
		result += "<code class=\"json-keyword\">{}</code>".format(
			str(obj).lower()
		)

	elif type(obj) == str:
		result += "<code class=\"json-string\">\"{}\"</code>".format(
			obj
		)

	elif type(obj) == dict:
		result += "{<br>\n"
		length = len(obj)
		count = 0
		for key in obj:
			result += ("&emsp; " * depth) + "<code class=\"json-string\">\"{}\"</code>".format(
				key
			)
			result += ": "
			result += jsonToHTML(obj[key], depth + 1)

			if count < length - 1:
				result += ",<br>\n"
			count += 1
		result += "<br>" + ("&emsp; " * (depth - 1)) + "\n}"

	elif type(obj) == list:
		result += "[<br>\n"
		length = len(obj)
		count = 0
		for item in obj:
			result += ("&emsp; " * depth) + jsonToHTML(item, depth + 1)

			if count < length - 1:
				result += ",<br>\n"
			count += 1
		result += "<br>" + ("&emsp; " * (depth - 1)) + "\n]"

	return result

website = Website(
    pages = [
        Page(
            title = "home", 
            description = "this is my website! cool.",
            homepage = True,
            sections = [
                Section(
                    title = "about",
                    description = "nice, ya found me. well my name is jonah. i am currently a sophomore in college. i am majoring in computer science. and that's about it.\noh yeah, i also have a few coding projects that you can find on the projects page."
                ),
                Section(
                    title = "social",
                    description = "if ya wanna contact me on other social media, go right ahead. here are all my links for absolutely everything that i have from gaming to social media to coding.\nall the good stuff.",
                    extras = [
                        Extra(
                            data_type = Extra.LINKED_IMAGE,
                            url = "https://instagram.com/FellowHashbrown",
                            data = "https://image.flaticon.com/icons/svg/174/174855.svg"
                        ),
                        Extra(
                            data_type = Extra.LINKED_IMAGE,
                            url = "https://facebook.com/FellowHashbrown",
                            data = "https://image.flaticon.com/icons/svg/174/174848.svg"
                        ),
                        Extra(
                            data_type = Extra.LINKED_IMAGE,
                            url = "https://twitter.com/FellowHashbrown",
                            data = "https://image.flaticon.com/icons/svg/174/174876.svg"
                        ),
                        Extra(
                            data_type = Extra.LINKED_IMAGE,
                            url = "https://tumblr.com/blog/FellowHashbrown",
                            data = "https://image.flaticon.com/icons/svg/174/174875.svg"
                        ),
                        Extra(
                            data_type = Extra.LINKED_IMAGE,
                            url = "https://steamcommunity.com/id/FellowHashbrown",
                            data = "https://www.freeiconspng.com/uploads/steam-icon-19.png"
                        ),
                        Extra(
                            data_type = Extra.LINKED_IMAGE,
                            url = "https://twitch.tv/FellowHashbrown",
                            data = "https://image.flaticon.com/icons/svg/733/733577.svg"
                        ),
                        Extra(
                            data_type = Extra.LINKED_IMAGE,
                            url = "https://pypi.org/user/FellowHashbrown",
                            data = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/2000px-Python-logo-notext.svg.png"
                        ),
                        Extra(
                            data_type = Extra.LINKED_IMAGE,
                            url = "https://github.com/FellowHashbrown",
                            data = "https://image.flaticon.com/icons/svg/733/733553.svg"
                        ),
                        Extra(
                            data_type = Extra.LINKED_IMAGE,
                            url = "https://repl.it/@FellowHashbrown",
                            data = "https://avatars3.githubusercontent.com/u/983194?s=280&v=4"
                        )
                    ]
                ),
                Section(
                    title = "discord",
                    description = "here is my discord server for all my projects too. that might be helpful eh?\nany bug reports, feature requests, and whatever else can be submitted through here. each project of mine is in its own category with its own channels so you can talk through there.\ndon't be afraid to mention me if you need help with something.",
                    extras = [
                        Extra(
                            data_type = Extra.FRAME,
                            url = "https://discordapp.com/widget?id=521185038969208850&theme=dark"
                        )
                    ]
                )
            ],
            credits = [
                Credit(
                    text = "Icons made by {} from {} is licensed by {}",
                    credits = [
                        {
                            "url": "https://www.freepik.com",
                            "title": "Freepik",
                            "text": "Freepik"
                        },
                        {
                            "url": "https://www.flaticon.com",
                            "title": "Flaticon",
                            "text": "www.flaticon.com"
                        },
                        {
                            "url": "https://creativecommons.org/licenses/by/3.0/",
                            "title": "Creative Commons BY 3.0",
                            "text": "CC 3.0 BY"
                        }
                    ]
                ),
                Credit(
                    text = "Icons made by {} from {} is licensed by {}",
                    credits = [
                        {
                            "url": "https://www.flaticon.com/authors/pixel-perfect",
                            "title": "Pixel Perfect",
                            "text": "Pixel Perfect"
                        },
                        {
                            "url": "https://www.flaticon.com",
                            "title": "Flaticon",
                            "text": "www.flaticon.com"
                        },
                        {
                            "url": "https://creativecommons.org/licenses/by/3.0/",
                            "title": "Creative Commons BY 3.0",
                            "text": "CC 3.0 BY"
                        }
                    ]
                )
            ]
        ),
        Page(
            title = "projects",
            description = "this is the page where all my projects are at! it's nice to see you've reached this. if you ever use any of them or whatnot, i appreciate the support.",
            sections = [
                Section(
                    title = "omegaPsi",
                    description = "omega psi is a discord bot i created and have been working on since september of 2018. originally, it was not called omega psi. however, i updated the code to use discord.py's rewrite library and therefore, omega psi was the new name. <a href=\"https://omegapsi.fellowhashbrown.com/commands\" class=\"link\">here</a> is a page for the commands and below is a blog for updates. join my <a href=\"https://discord.gg/W8yVrHt\" class=\"link\" target=\"_blank\">discord server</a> to see more.",
                    anchor = "omegaPsi",
                    extras = [
                        Extra(
                            data_type = Extra.FRAME,
                            url = "https://fellowhashbrown.tumblr.com/tagged/omegapsi"
                        )
                    ]
                ),
                Section(
                    title = "get2054",
                    description = "2054 is a decision-based game that is not finished yet. it is not even close. but i am currently working on it and most major milestones i make will be shown below in my blog :)",
                    anchor = "2054",
                    extras = [
                        Extra(
                            data_type = Extra.FRAME,
                            url = "https://fellowhashbrown.tumblr.com/tagged/2054"
                        )
                    ]
                ),
                Section(
                    title = "invasion",
                    description = "invasion is a cool game that i am also working on. i used to have one written but it was when i first discovered how to make a game in Python. i didn't understand classes or object-oriented programming yet. that made my code look terribly confusing and it was also horribly undocumented. for that reason, i deleted it and now im rewriting it in a way that is far easier to read and is highly documented. once i setup a github repo for it, you'll see the link here.<br>below is a blog for invasion!",
                    anchor = "invasion",
                    extras = [
                        Extra(
                            data_type = Extra.FRAME,
                            url = "https://fellowhashbrown.tumblr.com/tagged/invasion"
                        )
                    ]
                ),
                Section(
                    title = "elementGenerator",
                    description = "element generator is one of my most major java projects. all it really is is an application that simplifies adding new elements and minerals in <a href=\"https://minecraft.net/en-us/download/\" class=\"link\" target=\"_blank\">Minecraft: Java Edition</a>. here is the <a href=\"https://drive.google.com/uc?export=download&id=1GBE9MqUt9FLldiQFhNMqiFham-F4ttaG\" target=\"_blank\" class=\"link\">download link</a> and my code is available at my <a href=\"https://github.com/FellowHashbrown/element-generator\" target=\"_blank\" class=\"link\">github repo</a> for it.",
                    anchor = "element-generator"
                )
            ]
        ),
        Page(
            title = "archives",
            description = "oh look! an archive for any projects of mine!",
            sections = [
                Section(
                    title = "supercog",
                    description = "while developing my discord bot, i realized i was reusing code so i created a few classes for it to simplify it. then i realized how useful my shortened code was and decided to write a Python library for it. unfortunately, my own project caused problems for my discord bot and so i don't use it anymore.",
                    anchor = "supercog"
                ),
            ]
        ),
        Page(
            title = "api",
            description = "if you're a developer, you've reached my available APIs that i've written! if you're not a developer, you won't understand how this works but you're free to try.",
            sections = [
                APISection(
                    title = "hangmanAPI",
                    description = "Gets a random word to use in a hangman game.",
                    endpoint = "/hangman",
                    anchor = "hangman",
                    responses = [
                        Response(
                            code = 200,
                            model = {
                                "success": True,
                                "value": "wheel",
                                "level": "easy"
                            }
                        )
                    ]
                ),
                APISection(
                    title = "scrambleAPI",
                    description = "Gets a random word to use in a scramble game.",
                    endpoint = "/scramble",
                    anchor = "scramble",
                    responses = [
                        Response(
                            code = 200,
                            model = {
                                "success": True,
                                "value": "unused",
                                "hints": [
                                    "unutilized",
                                    "unemployed",
                                    "unexploited",
                                    "spare",
                                    "surplus"
                                ]
                            }
                        )
                    ]
                ),
                APISection(
                    title = "morseEncodeAPI",
                    description = "Converts text you give into International Morse Code.",
                    endpoint = "/morse/encode",
                    anchor = "morse-encode",
                    parameters = [
                        Parameter(
                            name = "text",
                            data_type = "string",
                            description = "The text to convert into morse code. Can be uppercase or lowercase letters between A-Z or numbers between 1-9."
                        )
                    ],
                    responses = [
                        Response(
                            code = 200,
                            model = {
                                "success": True,
                                "value": ".... . .-.. .-.. ---"
                            }
                        ),
                        Response(
                            code = 400,
                            model = {
                                "success": False,
                                "error": "Cannot Encode Empty Text."
                            }
                        ),
                        Response(
                            code = 400,
                            model = {
                                "success": False,
                                "error": "Cannot Encode Morse Code."
                            }
                        )
                    ]
                ),
                APISection(
                    title = "morseDecodeAPI",
                    description = "Converts International Morse Code you give into text.",
                    endpoint = "/morse/decode",
                    anchor = "morse-decode",
                    parameters = [
                        Parameter(
                            name = "text",
                            data_type = "string",
                            description = "The morse code to convert into regular text."
                        )
                    ],
                    responses = [
                        Response(
                            code = 200,
                            model = {
                                "success": True,
                                "value": "hello"
                            }
                        ),
                        Response(
                            code = 400,
                            model = {
                                "success": False,
                                "error": "Cannot Decode Empty Text."
                            }
                        ),
                        Response(
                            code = 400,
                            model = {
                                "success": False,
                                "error": "Cannot Decode Regular Text."
                            }
                        )
                    ]
                ),
                APISection(
                    title = "logicAPI",
                    description = "Parses and evaluates a logical expression whether in pseudocode, code, or logic.<br>NOTE: When typing in the URL manually, you'll need to encode the & symbols and the | symbols.<br>Before calling the API, parse the expression so it is URL-safe.<br>The <code class=\"code\">download</code> and <code class=\"code\">raw</code> parameters can only be used by someone in the browser.",
                    endpoint = "/logic",
                    anchor = "logic",
                    parameters = [
                        Parameter(
                            name = "expression",
                            data_type = "string",
                            description = "The logical expression to parse and evaluate."
                        ),
                        Parameter(
                            name = "table",
                            data_type = "boolean",
                            description = "Whether or not to receive a truth table for the logical expression. Defaults to false."
                        ),
                        Parameter(
                            name = "download",
                            data_type = "boolean",
                            description = "Whether or not to download the file directly to your device."
                        ),
                        Parameter(
                            name = "raw",
                            data_type = "boolean",
                            description = "Whether or not to show the raw truth table in the browser."
                        )
                    ],
                    responses = [
                        Response(
                            code = 200,
                            model = {
                                "success": True,
                                "value": [
                                    {
                                        "expression": "a",
                                        "truth_value": {
                                            "a": True
                                        },
                                        "value": True
                                    },
                                    "... More Expressions ..."
                                ]
                            }
                        ),
                        Response(
                            code = 200,
                            model = {
                                "success": True,
                                "value": [
                                    "| a | b | a ^ b |",
                                    "+---+---+-------+",
                                    "| T | T |   T   |",
                                    "| T | F |   F   |",
                                    "| F | T |   F   |",
                                    "| F | F |   F   |"
                                ]
                            }
                        ),
                        Response(
                            code = 400,
                            model = {
                                "success": False, 
                                "error": "You need an expression to parse."
                            }
                        ),
                        Response(
                            code = 400,
                            model = {
                                "success": False,
                                "error": "You need a truth value for the variable \"a\""
                            }
                        ),
                        Response(
                            code = 400,
                            model = {
                                "success": False, 
                                "error": "An unknown error has occurred and has been sent to the developer."
                            }
                        )
                    ]
                ),
                APISection(
                    title = "profanityAPI",
                    description = "Filters text to test whether or not it is a truncated profane word.",
                    endpoint = "/profanity",
                    anchor = "profanity",
                    parameters = [
                        Parameter(
                            name = "text",
                            data_type = "string",
                            description = "The text to test for any profanity."
                        )
                    ],
                    responses = [
                        Response(
                            code = 200,
                            model = {
                                "success": True,
                                "profane": True,
                                "likely_word": "asshole"
                            }
                        ),
                        Response(
                            code = 200,
                            model = {
                                "success": True,
                                "profane": False
                            }
                        ),
                        Response(
                            code = 400,
                            model = {
                                "success": False,
                                "error": "Cannot Filter Empty Text."
                            }
                        )
                    ]
                ),
                APISection(
                    title = "llamaAPI",
                    description = "Retrieves a random line of dialogue from Llamas With Hats.",
                    endpoint = "/llamas",
                    anchor = "llamas",
                    parameters = [
                        Parameter(
                            name = "episode",
                            data_type = "integer",
                            description = "The episode number to get a line from. Can be between 1-12. Chooses random episode by default."
                        ),
                        Parameter(
                            name = "author",
                            data_type = "string",
                            description = "The speaker to get text from. Can be Carl or Paul. Chooses random author by default."
                        ),
                        Parameter(
                            name = "any",
                            data_type = "boolean",
                            description = "Whether or not to choose any type of quote. Even one-worded quotes or action lines. Defaults to false."
                        ),
                        Parameter(
                            name = "fullScript",
                            data_type = "boolean",
                            description = "Whether or not to get the full script of quotes. To use this, you must provide an episode to get the full script from. Defaults to false."
                        )
                    ],
                    responses = [
                        Response(
                            code = 200,
                            model = {
                                "success": True,
                                "episode": 1,
                                "image": "https://i.quotev.com/img/q/u/16/5/30/e37ac6e9b1-supe.jpg",
                                "author": "Carl",
                                "value": "My stomach was making the rumblies."
                            }
                        ),
                        Response(
                            code = 200,
                            model = {
                                "success": True,
                                "episode": 1,
                                "image": "https://i.quotev.com/img/q/u/16/5/30/e37ac6e9b1-supe.jpg",
                                "quotes": [
                                    {
                                        "author": "Paul",
                                        "value": "CAAAARL! THERE IS A DEAD HUMAN IN OUR HOUSE!!"
                                    },
                                    "... More Quotes ..."
                                ]
                            }
                        ),
                        Response(
                            code = 400,
                            model = {
                                "success": False,
                                "error": "No Episode Given."
                            }
                        ),
                        Response(
                            code = 400,
                            model = {
                                "success": False,
                                "error": "Invalid Author."
                            }
                        ),
                        Response(
                            code = 400,
                            model = {
                                "success": False,
                                "error": "Invalid Episode."
                            }
                        )
                    ]
                ),
                APISection(
                    title = "officeAPI",
                    description = "Gets a random line of dialogue from The Office.",
                    endpoint = "/office",
                    anchor = "office",
                    parameters = [
                        Parameter(
                            name = "season",
                            data_type = "integer",
                            description = "Must be a season in the range 1-9."
                        ),
                        Parameter(
                            name = "episode",
                            data_type = "integer",
                            description = "The number of the episode to get. If the episode number exceeds the amount of episodes in the given season, an error will be given."
                        ),
                        Parameter(
                            name = "type",
                            data_type = "string",
                            description = "The type of quote to get. Can be either aired, deleted, or any. Defaults to aired."
                        )
                    ],
                    responses = [
                        Response(
                            code = 200,
                            model = {
                                "success": True,
                                "value": "Oh that's Andy. He's just hanging out.",
                                "author": "Erin",
                                "season": 8,
                                "episode": 22,
                                "deleted": False
                            }
                        ),
                        Response(
                            code = 400,
                            model = {
                                "success": False,
                                "error": "Season Not Given. Episode Was."
                            }
                        ),
                        Response(
                            code = 400,
                            model = {
                                "success": False,
                                "error": "Invalid Episode."
                            }
                        ),
                        Response(
                            code = 400,
                            model = {
                                "success": False,
                                "error": "Invalid Season."
                            }
                        ),
                        Response(
                            code = 400,
                            model = {
                                "success": False,
                                "error": "Invalid Quote Type."
                            }
                        )
                    ]
                )
            ]
        ),
        Page(
            title = "pageNotFound",
            description = "oooof. i think you took a wrong turn. better beep boop beep boop and go back.",
            ignore = True
        )
    ]
)

website.generateHTML()