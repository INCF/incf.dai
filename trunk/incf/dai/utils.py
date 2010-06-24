# utilities to be offered by the central hub one day - in part at least

from config import HUBS
from hub import HubProxy

def listHubs():
    return list(HUBS.keys())

def getHubByName(name):
    try:
        base_url = HUBS[name]
    except KeyError:
        print "Hub '%s' not found in %s." % (name, listHubs())
        return None
    return HubProxy(base_url)
