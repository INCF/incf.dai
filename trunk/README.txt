INCF Digital Atlasing Infrastructure
======================

This package provides a Python API to the Digital Brain Atlasing web
services provided by the International Neuroinformatics Coordinating  
Facility (INCF). To be useful and functional it requires a working
internet connection at runtime. The specification of the core
webservices within the INCF Digital Atlasing Infrastructure (incf.dai)
are available from <url to specification goes here>. 

In a nutshell the INCF DAI consistes of a network of so-called
*hubs* providing whatever services the group managing the hub decided
to share. To discover available hubs there is a utility function

>>> from incf.dai.utils import listHubNames
>>> hub_names = listHubNames()
>>> hub_names.sort()
>>> hub_names
['aba', 'emage', 'ucsd', 'whs']

This provides a list of currently known hub names. (Note: atm the list
is provided by the package since the INCF central hub managing the
registry is a fast moving target still.)

Knowing the names of available hubs one can optain proxies objects
specific for a particular hub by calling

>>> from incf.dai.utils import getHubByName
>>> whs = getHubByName('whs')
>>> whs 
<incf.dai.hub.HubProxy object at ...>

For introspection the URL to the service controller fort this hub is
available as 
>>> whs.base_url
'http://incf-dev.crbs.ucsd.edu:8080/atlas-whs?service=WPS'

There are two methods all hubs are expected to provide:
>>> whs.GetCapabilities
<bound method HubProxy.GetCapabilities of ...>

>>> whs.DescribeProcess
<bound method HubProxy.DescribeProcess of ...>

Calling any of those methods returns a custom response object
>>> response = whs.GetCapabilities()
>>> response
<incf.dai.response.Response object at 0x...>

To connect to a hub not registered with INCF Central (e.g., a local
hub under development) one can instanciate the proxy explicitly as in 
(setting offline=True avoids ever calling the url)

>>> from incf.dai.hub import HubProxy
>>> myhub = HubProxy('http://some.url?service=WPS', offline=True)
>>> myhub
<incf.dai.hub.HubProxy object at ...>

The hub proxy provides a generic call method to be invoked as in 

>>> capabilities = myhub('GetCapabilities',output='xml')
Calling http://some.url?service=WPS&request=GetCapabilities&output=xml

The first argument here is a name of the function to be invoked at the
hub but for convenience 'GetCapabilities' is also provided as a method
on the hub proxy itself.

>>> myhub.GetCapabilities()
Calling http://some.url?service=WPS&request=GetCapabilities&output=xml
<incf.dai.response.Response object at ...>




