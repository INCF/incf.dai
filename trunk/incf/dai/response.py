"""Custom response object including parsed data fro xml responses"""

import xml.dom.minidom

from incf.dai.utils import xml2obj

class Response(object):
    """Custom response object including the parsed response in self.data"""

    def __init__(self, response, url):
        self.headers = response[0]
        self.content = response[1]
        self.url = url
        if '/xml' in self.content_type:
            self.data = xml2obj(response[1])
            self.__dict__.update(self.data)
        else:
            self.data = None
        self.process_exceptions()


    def __getitem__(self, key):
        return self.data[key]
    

    def __str__(self):
        if '/xml' in self.content_type:
            doc = xml.dom.minidom.parseString(self.content)
            return doc.toprettyxml(indent='', newl='')
        return self.content


    def keys(self):
        """keys of the parsed data - if available"""
        if self.data is None:
            return []
        return self.data.keys()

    @property
    def content_type(self):
        """Return the content type from the header"""
        return self.headers['content-type']


    def process_exceptions(self):
        """Check for 4?? response codes raised by the service as well
        as 'ProcessFailed' in WPS Status"""
        status = self.headers['status']
        if status.startswith('4'):
            return self.handle_exception()
        if self.data is None:   # nothing left to process further
            return None
        wps_status = self.data.wps_Status
        if wps_status and 'wps_ProcessFailed' in wps_status.keys():
            return self.handle_exception()
        return None

    def handle_exception(self):
        """Raise custom exception"""
        if self.data is not None:
            report = self.data.wps_Status.wps_ProcessFailed.ows_ExceptionReport
            raise ApplicationError(report.ows_Exception['exceptionCode'],
                                   report.ows_Exception['ows_ExceptionText'],
                                   self.url,
                                   )
        else:
            raise Exception, self.headers
 

class ApplicationError(Exception):
    """Custom error to be raised when a hub service returns an error message"""

    def __init__(self, code, text, url):
        self.code = code
        self.text = text
        self.url = url
        super(ApplicationError, self).__init__()

        
    def __str__(self):
        return "\nCode: %s\nText: %s\nURL:  %s" % (self.code, 
                                                   self.text,
                                                   self.url,
                                                   )

