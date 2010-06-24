# Generic proxy to an INCF DAI hub

import urllib
import httplib2

class HubProxy(object):
    """ Generic proxy to an INCF DAI hub """

    def __init__(self, base):
        self.base = base
        self.proxy = httplib2.Http('.cache')   

    def __call__(self, service_id, **kw):
        """Generic call method invoking <base_url>/<service_id>?<querystring>
        where the <querystring> is constructed from the keyword arguments"""
        url = self.base + '/' + service_id +'?'
        qs = urllib.urlencode(kw)
        url += qs
        print "Calling %s" % url
