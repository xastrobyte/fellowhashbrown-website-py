from .errors import InvalidJSONException
from .section import Extra

class APISection:

    def __init__(self, *, title = None, description = None, endpoint = None, parameters = [], responses = [], anchor = None, extras = [], json = None):
        if json != None:

            if "title" not in json:
                raise InvalidJSONException("There is a missing key: \"title\"")
            elif "description" not in json:
                raise InvalidJSONException("There is a missing key: \"description\"")
            
            title = json["title"]
            description = json["description"]
            endpoint = endpoint if "endpoint" not in json else json["endpoint"]
            if endpoint == None:
                endpoint = title.replace(" ", "_").lower()
            parameters = parameters if "parameters" not in json else [Parameter(json = parameter) for parameter in json["parameters"]]
            responses = responses if "responses" not in json else [Response(json = response) for response in json["responses"]]
            anchor = anchor if "anchor" not in json else json["anchor"]
            if anchor == None:
                anchor = title.replace(" ", "-").lower()
            extras = extras if "extra" not in json else [Extra(json = extra) for extra in json["extras"]]
        
        self._title = title
        self._description = description
        self._endpoint = endpoint
        self._parameters = parameters
        self._responses = responses
        self._anchor = anchor
        self._extras = extras
    
    def getTitle(self):
        return self._title
    
    def getDescription(self):
        return self._description
    
    def getEndpoint(self):
        return self._endpoint
    
    def getParameters(self):
        return self._parameters
    
    def getResponses(self):
        return self._responses
    
    def getAnchor(self):
        return self._anchor
    
    def getExtras(self):
        return self._extras
    
    def toJSON(self):
        return {
            "title": self.getTitle(),
            "description": self.getDescription(),
            "endpoint": self.getEndpoint(),
            "parameters": [parameter.toJSON() for parameter in self.getParameters()],
            "responses": [response.toJSON() for response in self.getResponses()],
            "anchor": self.getAnchor(),
            "extras": [extra.toJSON() for extra in self.getExtras()],
            "is_api": True
        }
    
    def generateHTML(self):
        html = (
                        """
                        <h2 class="page-section">
                            <a name="{}"></a>
                            <code class="field">page</code><code>.</code><code class="field">{}</code><code>();</code>
                        </h2>
                        <div class="page-section-block">
                            <p style="text-align: left;">
                                <code>GET {}</code>
                                <p style="text-align: left;">{}</p>
                                <p style="text-align: left; font-weight: bold;">Parameters</p>
                                {}
                                {}
                            </p>
                        </div>
                        """
        )

        parameters = ""
        for parameter in self.getParameters():
            parameters += parameter.generateHTML() + "\n"

        if len(parameters) == 0:
            parameters = "<p style=\"text-align: left;\">None</p>"
        else:
            parameters = (
                                """
                                <table width=\"100%\">
                                    <tbody>
                                        {}
                                    </tbody>
                                </table>
                                """
            ).format(
                parameters
            )
        
        responses = ""
        for response in self.getResponses():
            responses += response.generateHTML() + "\n"
        
        return html.format(
            self.getAnchor(),
            self.getTitle(),
            self.getEndpoint(),
            self.getDescription(),
            parameters,
            responses
        )
    
class Parameter:

    def __init__(self, *, name = None, data_type = None, description = None, json = None):
        if json != None:

            if "name" not in json:
                raise InvalidJSONException("There is a missing key: \"name\"")
            elif "data_type" not in json:
                raise InvalidJSONException("There is a missing key: \"data_type\"")
            elif "description" not in json:
                raise InvalidJSONException("There is a missing key: \"description\"")
            
            name = name if "name" not in json else json["name"]
            data_type = data_type if "data_type" not in json else json["data_type"]
            description = description if "description" not in json else json["description"]
        
        self._name = name
        self._data_type = data_type
        self._description = description
    
    def getName(self):
        return self._name
    
    def getDataType(self):
        return self._data_type
    
    def getDescription(self):
        return self._description
    
    def toJSON(self):
        return {
            "name": self.getName(),
            "data_type": self.getDataType(),
            "description": self.getDescription()
        }
    
    def generateHTML(self):
        html = (
                                        """
                                        <tr>
                                            <td>
                                                <code class="code">{}</code>
                                            </td>
                                            <td style="font-weight: normal">
                                                <p style="color: #E0E2E4;">
                                                    <code class="code-string">{}</code>
                                                    {}
                                                </p>
                                            </td>
                                        </tr>
                                        """
        )

        return html.format(
            self.getName(),
            self.getDataType(),
            self.getDescription()
        )
    
class Response:

    def __init__(self, *, code = None, model = None, json = None):
        if json != None:

            if "code" not in json:
                raise InvalidJSONException("There is a missing key: \"code\"")
            elif "model" not in json:
                raise InvalidJSONException("There is a missing key: \"model\"")
            
            code = code if "code" not in json else json["code"]
            model = model if "model" not in json else json["model"]
        
        self._code = code
        self._model = model
    
    def getCode(self):
        return self._code
    
    def getModel(self):
        return self._model
    
    def toJSON(self):
        return {
            "code": self.getCode(),
            "model": self.getModel()
        }
    
    def generateHTML(self):
        html = (
                                                    """
                                                    <p style="font-weight: bold;">
                                                        Response 
                                                        <code class="code-string">{}</code
                                                    </p>
                                                    <p>Body</p>
                                                    <div class="code-block">
                                                        {}
                                                    </div>
                                                    """
        )

        responseJSON = jsonToHTML(self.getModel())

        return html.format(
            self.getCode(),
            responseJSON
        )
    
def jsonToHTML(obj, depth = 1):

	result = ""

	if type(obj) in [bool, int, float]:
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