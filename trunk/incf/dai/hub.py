"""Generic proxy to an INCF DAI hub"""

import httplib2
import urllib

from incf.dai.config import LOGGER
from incf.dai.response import Response


class HubProxy(object):
    """ Generic proxy to an INCF DAI hub """

    def __init__(self, base_url, minimal=False, offline=False):
        self.base_url = base_url
        # no cache for the time being
        # self.proxy = httplib2.Http('.cache')
        if offline:
            self.proxy = LocalProxy()
        else:
            self.proxy = httplib2.Http()
            if not minimal:
                self.process_descriptions = self.get_process_descriptions()
                self.capabilities = [e.ows_Identifier for e in self.process_descriptions]
                # dynamically generating associated methods
                for capability in self.capabilities:
                    if capability == "DescribeSRS":
                        add_method(self, capability, srsName="")
                    else:
                        add_method(self, capability)

    def __call__(self, 
                 version="1.0.0",
                 request="Execute",
                 identifier=None,
                 format="xml",
                 **kw
                 ):
        """Generic call method invoking

        <base_url>&version=<version>&request=<request>&Identifier=<identifier>
        &ResponseForm={format}&DataInputs={EncodedInputs}

        where the {EncodedInputs} are constructed from the keyword arguments.
        version defaults to '1.0.0' and can be omitted by passing None.
        """
        url = [self.base_url]

        if version is not None:
            version = "&version=%s" % version
            url.append(version)

        request = '&request=%s' % request
        url.append(request)

        if identifier is not None:
            identifier = "&Identifier=%s" % identifier
            url.append(identifier)

        format = "&ResponseForm=%s" % format
        url.append(format)

        if kw:
            print kw
            url.append(encode_datainputs(**kw))

        url = "".join(url)
        LOGGER.info("Calling %s" % url)
        return Response(self.proxy.request(url, "GET"), url)

    # Every hub is required to provide this

    def GetCapabilities(self):
        """A list of all services provided by the hub"""
        return self(version=None, request='GetCapabilities')

    def DescribeProcess(self, version="1.0.0", identifier=None):
        """Detailed description of services at the hub.
        'identifier' specifies the service to be described.
        if None (default) all services are described.
        """
        return self(version=version, 
                    request='DescribeProcess', 
                    identifier=identifier,
                    )

    
    # some helper methods

    def get_process_descriptions(self):
        """Call 'DescribeProcess' and return the parsed xml"""
        response = self.DescribeProcess()
        return response.data.ProcessDescription

# helper functions

def encode_datainputs(**kw):
    """Construct the 'DataInputs' query string from the keyword arguments"""
    encode = urllib.urlencode
    items = []
    for key, value in kw.items():
        items.append('='.join([key, value]))
        return "&DataInputs=" + "@".join(items)


def add_method(inst, service_id, **kw):
    """helper function for adding methods to a hub instance at runtime"""
    service_id = str(service_id)     # potential cast from unicode to str
    def localmethod(**kw):
        """Doc string - to be overwritten below"""
        return HubProxy.__call__(inst, 
                                 version="1.0.0",
                                 request='Execute', 
                                 identifier=service_id, 
                                 **kw
                                 )
    localmethod.__doc__ = "Supported arguments: %s" % ", ".join(kw.keys())
    localmethod.__name__ = service_id
    setattr(inst, localmethod.__name__, localmethod)


# helper class for offline testing

class LocalProxy(object):
    """Dummy proxy for offline testing"""
    def request(self, url, *args, **kw):
        """Fake a request by printing the URL that would be called
        and returning a minimal response tuple."""
        print "Requested URL:", url
        if args:
            print "positional arguments:", args
        if kw:
            print "keyword arguments:", kw
        return ({'content-type':'text/plain',
                 'status':'200',
                 }, 
                "Some plain text")
    
