"""Generic proxy to an INCF DAI hub"""

import httplib2
from odict import odict

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
                self.capabilities = [e.ows_Identifier for 
                                     e in self.process_descriptions]
                signatures = extract_signatures(self)
                # dynamically generating associated methods
                for capability in self.capabilities:
                    add_method(self, capability, signatures)


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

        if format is not None: 
            format = "&ResponseForm=%s" % format
            url.append(format)

        if kw:
            url.append(encode_datainputs(**kw))

        url = "".join(url)
        LOGGER.info("Calling %s" % url)
        return Response(self.proxy.request(url, "GET"), url)

    # Every hub is required to provide this

    def GetCapabilities(self):
        """A list of all services provided by the hub"""
        return self(version=None, request='GetCapabilities')

    def DescribeProcess(self, version="1.0.0", identifier='ALL'):
        """Detailed description of services at the hub.
        'identifier' specifies the service to be described.
        if 'ALL' (default) all services are described.
        """
        return self(version=version, 
                    request='DescribeProcess', 
                    identifier=identifier,
                    format=None,
                    )

    
    # some helper methods

    def get_process_descriptions(self):
        """Call 'DescribeProcess' and return the parsed xml"""
        response = self.DescribeProcess()
        return response.data.ProcessDescription

# helper functions

def encode_datainputs(**kw):
    """Construct the 'DataInputs' query string from the keyword arguments"""
    data = []
    for key, value in kw.items():
        data.append('='.join([key, value]))
    return "&DataInputs=" + ";".join(data)


def add_method(inst, service_id, signatures):
    """helper function for adding methods to a hub instance at runtime"""
    service_id = str(service_id)     # potential cast from unicode to str
    kwargs = signatures.get(service_id)
    def localmethod(**kwargs):
        """Doc string - to be overwritten below"""
        return HubProxy.__call__(inst, 
                                 version="1.0.0",
                                 request='Execute', 
                                 identifier=service_id, 
                                 **kwargs
                                 )
    if kwargs:
        args = ", ".join(kwargs.keys())
        localmethod.__doc__ = "Supported arguments: %s" % args
    else:
        localmethod.__doc__ = "This method takes no arguments"
    localmethod.__name__ = service_id
    setattr(inst, localmethod.__name__, localmethod)


def extract_signatures(hub):
    """Given the process descriptions infer the method signatures"""
    descriptions = hub.process_descriptions
    signatures = {}
    for description in descriptions:
        service = str(description.ows_Identifier)
        if description.DataInputs is None:
            continue
        if type(description.DataInputs.Input) is not type([]):   
            # happens if only one argument is supported
            description.DataInputs.Input = [description.DataInputs.Input]
        args = [str(e.ows_Identifier) for e in description.DataInputs.Input]
        kwargs = odict()
        default = ""     # Can we infer defaults from the process descriptions?
        for arg in args:
            kwargs[arg] = default
        signatures[service] = kwargs

    return signatures


# helper class for offline testing

class LocalProxy(object):
    """Dummy proxy for offline testing"""
    def request(self, url, *args): #, **kw):
        """Fake a request by printing the URL that would be called
        and returning a minimal response tuple."""
        print "Requested URL:", url
        if args:
            print "positional arguments:", args
#        if kw:
#            print "keyword arguments:", kw
        return ({'content-type':'text/plain',
                 'status':'200',
                 }, 
                "Some plain text")
    
