"""Generic proxy to an INCF DAI hub"""

import urllib
import httplib2

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
                self.capabilities = self.get_capabilities()
                # dynamically generating associated methods
                for capability in self.capabilities:
                    if capability == "DescribeSRS":
                        add_method(self, capability, srsName="")
                    else:
                        add_method(self, capability)

    def __call__(self, service_id, version=None, **kw):
        """XXX: needs updating
        Generic call method invoking
        <base_url>&version=<version>&request=<service_id><querystring>
        where the <querystring> is constructed from the keyword arguments"""
        url = self.base_url
        if version is not None:
            version_string = "&version=%s" % version
            url += version_string
        url = url + '&request=' + service_id +'&'
        query_string = self.encode_datainputs(**kw)
        url += query_string
        LOGGER.info("Calling %s" % url)
        return Response(self.proxy.request(url, "GET"), url)

    def encode_datainputs(self, **kw):
        items = []
        for key, value in kw.items():
            items.append('='.join([key, value]))
        return "DataInputs=" + "@".join(items)

    # Every hub is required to provide this

    def GetCapabilities(self, output='xml'):
        """A list of all services provided by the hub"""
        return self('GetCapabilities', output=output)

    def DescribeProcess(self, version="1.0.0", output='xml'):
        """Detailed description of services at the hub"""
        return self('DescribeProcess', version=version, output=output)

    
    # some private helper methods

    def get_capabilities(self):
        """Call 'GetCapabilities' and return the extracted method ids"""
        response =  self('GetCapabilities', output='xml')
        key_1 = 'wps_ProcessOfferings'
        key_2 = 'wps_Process'
        return tuple([l['ows_Identifier']
                      for l in response[key_1][key_2]]
                     )


# XXX FIXME: no arguments supported yet
def add_method(inst, service_id, **kw):
    """helper function for adding methods to a hub instance at runtime"""
    service_id = str(service_id)     # potential cast from unicode to str
    def localmethod(**kw):
        """Doc string - to be overwritten below"""
        return HubProxy.__call__(inst, 
                                 'Execute', 
                                 Identifier=service_id, 
                                 version="1.0.0",
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
    
