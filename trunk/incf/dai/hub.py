# Generic proxy to an INCF DAI hub

import urllib
import httplib2

class HubProxy(object):
    """ Generic proxy to an INCF DAI hub """

    def __init__(self, base_url):
        self.base_url = base_url
        self.proxy = httplib2.Http('.cache')   

    def __call__(self, service_id, **kw):
        """Generic call method invoking <base_url>/<service_id>?<querystring>
        where the <querystring> is constructed from the keyword arguments"""
        url = self.base_url + '/' + service_id +'?'
        qs = urllib.urlencode(kw)
        url += qs
        print "Calling %s" % url

    # Every hub is required to provide this

    def GetCapabilities(self, format='xml'):
        """A list of all services provided by the hub"""
        return self('GetCapabilities', format=format)
    
