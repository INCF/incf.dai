"""Custom response object including parsed data fro xml responses"""

import xml.dom.minidom

from incf.dai.utils import xml2obj

class Response(object):
    """Custom response object including the parsed response in self.data"""

    def __init__(self, response, url):
        self.headers = response[0]
        self.content = response[1]
        self.url = url
        if 'application/xml' in self.headers['content-type']:
            self.data = xml2obj(response[1])
            self.__dict__.update(self.data)
        else:
            self.data = None
        self.process_exceptions()


    def __getitem__(self, key):
        return self.data[key]


    def __getattr__(self, attr):
        if attr in self.data.keys():
            return self.data[attr]
        else:
            raise AttributeError
    

    def __str__(self):
        doc = xml.dom.minidom.parseString(self.content)
        return doc.toprettyxml()


    def keys(self):
        """keys of the parsed data - if available"""
        if self.data is None:
            return []
        return self.data.keys()


    def content_type(self):
        """Return the content type from the header"""
        return self.headers['content-type']


    def process_exceptions(self):
        """Check for 4?? response codes raise by the service"""
        status = self.headers['status']
        if status.startswith('4'):
            return self.handle_exception()
        return None

    def handle_exception(self):
        """Raise custom exception"""
        raise ApplicationError(self.ows_Exception['exceptionCode'],
                               self.ows_Exception['ows_ExceptionText'],
                               self.url,
                               )



class ApplicationError(Exception):
    def __init__(self, code, text, url):
        self.code = code
        self.text = text
        self.url = url
    def __str__(self):
        return "\nCode: %s\nText: %s\nURL:  %s" % (self.code, 
                                                   self.text,
                                                   self.url,
                                                   )

