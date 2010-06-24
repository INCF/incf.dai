# Generic proxy to an INCF DAI hub

import httplib2

class HubProxy(object):
    """ Generic proxy to an INCF DAI hub """

    def __init__(self, base):
        self.base = base
        self.proxy = httplib2.Http('.cache')   

