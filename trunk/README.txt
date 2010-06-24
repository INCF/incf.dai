INCF Digital Atlasing
===============

(intro to go here)

>>> from incf.dai.hub import HubProxy
>>> aba = HubProxy('http://some.url')
>>> aba
<incf.dai.hub.HubProxy object at ...>

The internal generic call method

>>> capabilities = aba('GetCapabilities',output='xml')
Calling http://some.url/GetCapabilities?output=xml

where 'GetCapabilities' is also available as method

>>> aba.GetCapabilities()
Calling http://some.url/GetCapabilities?output=xml

Instead of constructing HubProxies directly some are known to exist
and available from the utilities

>>> from incf.dai.utils import listHubs
>>> hubs = listHubs()
>>> hubs.sort()
>>> hubs
['aba', 'emage', 'ucsd', 'whs']

provides a list of known hub ids and proxies are optained by

>>> from incf.dai.utils import getHubByName
>>> emage = getHubByName('emage')
>>> emage 
<incf.dai.hub.HubProxy object at ...>
>>> emage.base_url
'http://whs0.pdc.kth.se:8080/incf-services/service/EmageServiceController'



