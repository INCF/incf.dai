"""Custom response object including parsed data fro xml responses"""

import xml.dom.minidom

from incf.dai.utils import xml2obj

class Response(object):
    """Custom response object including the parsed response in self.data"""

    def __init__(self, response):
        self.headers = response[0]
        self.content = response[1]
        self.data = xml2obj(response[1])

    def __getitem__(self, key):
        return self.data[key]
    
    def __str__(self):
        doc = xml.dom.minidom.parseString(self.content)
        return doc.toprettyxml()

    def keys(self):
        """keys of the parsed data - if available"""
        if self.data is None:
            return []
        return self.data.keys()
