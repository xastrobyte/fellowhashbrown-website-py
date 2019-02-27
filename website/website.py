from .errors import InvalidJSONException
from .page import Page

class Website:

    def __init__(self, *, pages = [], json = None):

        if type(json) == dict:

            if "pages" not in json:
                raise InvalidJSONException("There is a missing key: \"pages\"")
            
            pages = [Page(json = page) for page in json["pages"]]
        
        self._pages = pages
    
    def getPages(self):
        return self._pages
    
    def toJSON(self):
        return {
            "pages": [page.toJSON() for page in self.getPages()]
        }
    
    def generateHTML(self):
        head = (
"""
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="/static/styles.css" rel="stylesheet" type="text/css">

    {}

    <link rel="shortcut icon" href="{{ url_for('static', filename='/favicon.ico') }}">
    <link rel="apple-touch-icon" sizes="180x180" href="{{ url_for('static', filename='/apple-touch-icon.png') }}">
    <link rel="icon" type="image/png" sizes="32x32" href="{{ url_for('static', filename='/favicon-32x32.png') }}">
    <link rel="icon" type="image/png" sizes="16x16" href="{{ url_for('static', filename='/favicon-16x16.png') }}">
    <link rel="manifest" href="{{ url_for('static', filename='/site.webmanifest') }}">
    <link rel="mask-icon" href="{{ url_for('static', filename='/safari-pinned-tab.svg') }}" color="#202020">
    <meta name="msapplication-TileColor" content="#202020">
    <meta name="msapplication-TileImage" content="{{ url_for('static', filename='/mstile-144x144.png') }}">
    <meta name="theme-color" content="#202020">
    <meta name="msapplication-config" content="{{ url_for('static', filename='/browserconfig.xml') }}">
</head>
"""
        )

        meta = (
    """
    <meta property="theme-color" content="#EC7600" />
    <meta property="og:title" content="website.{}();" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://www.fellowhashbrown.com/{}" />
    <meta property="og:image" content="https://i.imgur.com/QkPf372.png" />

    <meta property="og:description" content="{}" />
    <meta property="og:site_name" content="Fellow Hashbrown" />
    <title>Fellow Hashbrown</title>
    """
        )
        
        html = (
"""
<html>

    {}

    <body>
        <div class="page-body">

            <!-- Navigation Bar -->
            <nav class="nav-bar">
                <img src="https://i.imgur.com/QkPf372.png" class="social-image" style="width: 50px; height: 50px;">
                <ul class="nav-links">
                    {}
                </ul>
            </nav>

            <!-- Content -->
            <div class="content">
                {}
            </div>
        </div>
    </body>
</html>
"""
        )

        navigation_bar = {}

        for page in self.getPages():
            navigation_bar[page.getTitle()] = ""

            for nav_page in self.getPages():
                if not nav_page.ignore():

                    navigation_link = (
                """
                <li class=\"nav-item\">
                    <a class="nav-link{}\" href=\"/{}\">{}</a>
                </li>\n
                """
                    )

                    navigation_bar[page.getTitle()] += navigation_link.format(
                        " active" if (page == nav_page) else "",
                        nav_page.getTitle() if not nav_page.isHomepage() else "",
                        nav_page.getTitle()
                    )

        for page in self.getPages():
            htmlCopy = html.format(
                head.replace(
                    "{}",
                    meta.format(
                        page.getTitle().lower(),
                        page.getTitle() if page.isHomepage() else "",
                        page.getDescription()
                    )
                ),
                navigation_bar[page.getTitle()],
                page.generateHTML()
            )

            f = open("templates/{}.html".format(
                page.getTitle()
            ), "w")
            f.write(htmlCopy)
            f.close()