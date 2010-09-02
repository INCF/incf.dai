import xml.dom.minidom

from incf.dai.utils import xml2obj

class Response(object):
    """Top-level response object"""

    def __init__(self, response):
        self.headers = response[0]
        self.content = response[1]
        self._dict = xml2obj(response[1])

    def __getitem__(self, key):
        return self._dict[key]
    
    def __str__(self):
        doc = xml.dom.minidom.parseString(self.content)
        return doc.toprettyxml()

