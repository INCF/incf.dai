INCF Digital Atlasing
===============

(intro to go here)

>>> from incf.dai.hub import HubProxy
>>> aba = HubProxy('http://some.url')
>>> aba
<incf.dai.hub.HubProxy object at ...>

The internal generic call method

>>> capabilities = aba('GetCapabilities',format='xml')
Calling http://some.url/GetCapabilities?format=xml

where 'GetCapabilities' is also available as method

>>> aba.GetCapabilities()
Calling http://some.url/GetCapabilities?format=xml

