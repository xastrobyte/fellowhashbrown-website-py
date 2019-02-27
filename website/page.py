from .errors import InvalidJSONException, UnmatchedFormatting
from .section import Section

class Page:
    
    def __init__(self, *, title = None, description = None, homepage = False, sections = [], snippets = [], ignore = False, credits = [], json = None):

        if json != None:
            
            if "title" not in json:
                raise InvalidJSONException("There is a missing key: \"title\"")
            elif "description" not in json:
                raise InvalidJSONException("There is a missing key: \"description\"")
            
            title = json["title"]
            description = json["description"]

            homepage = homepage if "homepage" not in json else json["homepage"]
            sections = sections if "sections" not in json else [Section(json = section) for section in json["sections"]]
            snippets = snippets if "snippets" not in json else [CodeSnippet(json = snippet) for snippet in json["snippets"]]
            ignore = ignore if "ignore" not in json else json["ignore"]
            credits = credits if "credits" not in json else [Credit(json = credit) for credit in json["credits"]]

        self._title = title
        self._description = description
        self._homepage = homepage
        self._sections = sections
        self._snippets = snippets
        self._ignore = ignore
        self._credits = credits
    
    def getTitle(self):
        return self._title
    
    def getDescription(self):
        return self._description
    
    def isHomepage(self):
        return self._homepage
    
    def getSections(self):
        return self._sections
    
    def getSnippets(self):
        return self._snippets
    
    def ignore(self):
        return self._ignore

    def getCredits(self):
        return self._credits
    
    def toJSON(self):
        return {
            "title": self.getTitle(),
            "description": self.getDescription(),
            "homepage": self.isHomepage(),
            "sections": [section.toJSON() for section in self.getSections()],
            "ignore": self.ignore(),
            "credits": [credit.toJSON() for credit in self.getCredits()]
        }
    
    def generateHTML(self):
        html = (
                """
                {}

                <h1 class="page-title">
                    <code class="field">website</code><code>.</code><code class="field">{}</code><code>();</code>
                </h1>

                <div class="page-title-block" style="max-width: 75%;">
                    <p style="text-align: center;">
                        {}
                    </p>
                </div>

                {}

                <br>

                <!--Credit 3rd Party Objects-->
                {}

                <br>
                <br>
                """
        )

        snippets = ""
        for snippet in self.getSnippets():
            snippets += snippet.generateHTML()

        sections = ""
        for section in self.getSections():
            sections += section.generateHTML()
        
        credits = ""
        for credit in self.getCredits():
            credits += credit.generateHTML()
        
        return html.format(
            snippets,
            self.getTitle(),
            self.getDescription(),
            sections,
            credits
        )
    
class Credit:

    def __init__(self, text = None, credits = None, json = None):
        if json != None:

            if "text" not in json:
                raise InvalidJSONException("There is a missing key: \"text\"")
            elif "credits" not in json:
                raise InvalidJSONException("There is a missing key: \"credits\"")
            
            text = json["text"]
            credits = json["credits"]
        
        if text.count("{}") != len(credits) and not(text == credits == None):
            raise UnmatchedFormatting("The number of braces ({}) do not match the number of credits.")

        self._text = text
        self._credits = credits
    
    def getText(self):
        return self._text
    
    def getCredits(self):
        return self._credits
    
    def toJSON(self):
        return {
            "text": self.getText(),
            "credits": self.getCredits()
        }
    
    def generateHTML(self):
        text = self.getText()

        for credit in self.getCredits():
            credit = "<a href=\"{}\" class=\"link\" title=\"{}\">{}</a>".format(
                credit["url"],
                credit["title"],
                credit["text"]
            )
            text = text.replace("{}", credit, 1)
        
        return (
            """
            <div style="text-align: center;"><code class="regular">
                {}
            </code></div>\n
            """
        ).format(text)

class CodeSnippet:

    def __init__(self, snippet):
        self._snippet = snippet
    
    def generateHTML(self):
        return self._snippet