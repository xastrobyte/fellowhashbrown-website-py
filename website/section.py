from .errors import InvalidJSONException

class Section:

    def __init__(self, *, title = None, description = None, anchor = None, extras = [], json = None):
        if json != None:

            if "title" not in json:
                raise InvalidJSONException("There is a missing key: \"title\"")
            elif "description" not in json:
                raise InvalidJSONException("There is a missing key: \"description\"")
            
            title = json["title"]
            description = json["description"]
            anchor = anchor if "anchor" not in json else json["anchor"]
            if anchor == None:
                anchor = title.replace(" ", "-").lower()
            extras = extras if "extra" not in json else [Extra(json = extra) for extra in json["extras"]]
        
        self._title = title
        self._description = description
        self._anchor = anchor
        self._extras = extras
    
    def getTitle(self):
        return self._title
    
    def getDescription(self):
        return self._description
    
    def getAnchor(self):
        return self._anchor
    
    def getExtras(self):
        return self._extras
    
    def toJSON(self):
        return {
            "title": self.getTitle(),
            "description": self.getDescription(),
            "anchor": self.getAnchor(),
            "extras": [extra.toJSON() for extra in self.getExtras()],
            "is_api": False
        }
    
    def generateHTML(self):
        html = (
                """
                <h2 class="page-section">
                    <a name="{}"></a>
                    <code class="field">page</code><code>.</code><code class="field">{}</code><code>();</code>
                </h2>
                <div class="page-section-block" style="text-align: center;">
                    <p style="text-align: left;">
                        {}
                    </p>
                    {}
                </div>
                """
        )

        return html.format(
            self.getAnchor(),
            self.getTitle(),
            self.getDescription(),
            "\n".join([extra.generateHTML() for extra in self.getExtras()])
        )

class Entry:

    def __init__(self, default_text, *, action = None):
        pass
    
class Extra:

    LINK = 0
    IMAGE = 1
    LINKED_IMAGE = 2
    FRAME = 3

    def __init__(self, *, data_type = None, url = None, data = None, json = None):
        if json != None:

            if "data_type" not in json:
                raise InvalidJSONException("There is a missing key: \"data_type\"")
            elif "url" not in json:
                raise InvalidJSONException("There is a missing key: \"url\"")
            
            if "data" not in json and json["data_type"] != Extra.LINK:
                raise InvalidJSONException("There is a missing key. You provided \"data_type\" as an image but you gave no \"data\"")
            
            data_type = data_type if "data_type" not in json else json["data_type"]
            url = url if "url" not in json else json["url"]
            data = data if "data" not in json else json["data"]
        
        self._data_type = data_type
        self._url = url
        self._data = data
    
    def getDataType(self):
        return self._data_type
    
    def getURL(self):
        return self._url
    
    def getData(self):
        return self._data
    
    def toJSON(self):
        return {
            "data_type": self.getDataType(),
            "url": self.getURL(),
            "data": self.getImageURL()
        }
    
    def generateHTML(self):
        if self.getDataType() == Extra.LINK:
            return "<a href=\"{}\" class=\"link\" target=\"_blank\">{}</a>".format(
                self.getURL(),
                self.getData()
            )
        
        elif self.getDataType() == Extra.IMAGE:
            return "<img src=\"{}\">".format(
                self.getURL()
            )
        
        elif self.getDataType() == Extra.LINKED_IMAGE:
            return "<a href=\"{}\" class=\"social-button\" target=\"_blank\"><img src=\"{}\" class=\"social-image\"></a>".format(
                self.getURL(),
                self.getData()
            )
        
        elif self.getDataType() == Extra.FRAME:
            return "<p style=\"text-align: center;\"><iframe src=\"{}\" width=\"100%\" height=\"500\" allowtransparency=\"true\" frameborder=\"0\"></iframe>".format(
                self.getURL()
            )