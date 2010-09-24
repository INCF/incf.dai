====================================
INCF Digital Atlasing Infrastructure
====================================

This package provides a Python API to the Digital Brain Atlasing web
services provided by the International Neuroinformatics Coordinating  
Facility (INCF). To be useful and functional it requires a working
internet connection at runtime. The details of the core webservices 
within the INCF Digital Atlasing Infrastructure (incf.dai) are available 
from the specification_.


Discovering and Accessing Hubs
==============================

In a nutshell the INCF DAI consistes of a network of so-called
*hubs* providing whatever services the group managing the hub decided
to share. To discover available hubs there is a utility function

>>> from incf.dai.utils import list_hub_names
>>> hub_names = list_hub_names()
>>> hub_names.sort()
>>> hub_names
['aba', 'emap', 'ucsd', 'whs']

This provides a list of currently known hub names. (Note: atm the list
is provided by the package since the INCF central hub managing the
registry is a fast moving target still.)

Knowing the names of available hubs one can optain proxies objects
specific for a particular hub by calling

>>> from incf.dai.utils import get_hub_by_name
>>> whs = get_hub_by_name('whs')
>>> whs # doctest: +ELLIPSIS
<incf.dai.hub.HubProxy object at ...>

If you call for an unknow hub (or make a typo) you will get a KeyError

>>> foo = get_hub_by_name('foo')
Traceback (most recent call last):
KeyError


For introspection the URL to the service controller for this hub is
available as 
>>> whs.base_url
'http://incf-dev.crbs.ucsd.edu:8080/atlas-whs?service=WPS'

There are two methods all hubs are expected to provide:
>>> whs.GetCapabilities  # doctest: +ELLIPSIS
<bound method HubProxy.GetCapabilities of ...>

>>> whs.DescribeProcess # doctest: +ELLIPSIS
<bound method HubProxy.DescribeProcess of ...>

Calling any of those methods returns a custom response object
>>> response = whs.GetCapabilities()
>>> response  # doctest: +ELLIPSIS
<incf.dai.response.Response object at 0x...>

>>> response = whs.DescribeProcess()
>>> response  # doctest: +ELLIPSIS
<incf.dai.response.Response object at 0x...>

Usually, there is no need to call any of the two methods mentioned 
above as their main information returned is available anyway via

>>> whs.capabilities
[u'DescribeSRS', u'GetStructureNamesByPOI', u'ListSRSs']

and all methods listed are available on the hub proxy right away

>>> sorted(whs.__dict__.keys())   # doctest: +NORMALIZE_WHITESPACE
['DescribeSRS', 'GetStructureNamesByPOI', 'ListSRSs', 'base_url', 
'capabilities', 'process_descriptions', 'proxy']

like in 

>>> response = whs.ListSRSs()
>>> sorted(response.keys())
[u'Orientations', u'QueryInfo', u'SRSList', u'xmlns', u'xmlns_gml']

>>> response['SRSList']  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
{SRS:[{Area:{structureName:u'whole brain'}, 
       Author:{authorCode:u'WHS', ...

For further convenience, the response object also supports attribute-like 
access to the data as in

>>> response.QueryInfo
{QueryUrl:u'http://incf-dev.crbs.ucsd.edu:8080/atlas-whs?service=WPS&version=1.0.0&request=Execute&Identifier=ListSRSs&ResponseForm=xml'}

Omitting required arguments raises an 'ApplicationError'

>>> response = whs.DescribeSRS()  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
Traceback (most recent call last):
...
ApplicationError: 
Code: NotApplicableCode
Text: Unrecognized URI.
URL:  http://incf-dev.crbs.ucsd.edu:8080/atlas-whs?service=WPS&version=1.0.0&request=Execute&Identifier=DescribeSRS&ResponseForm=xml

whereas providing the required argument (srsName here) results in

# commented out because the service is not up yet???
#>>> response = whs.DescribeSRS(srsName="")  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
#>>> response.keys()


Accessing Hubs not registered at INCF
=====================================

To connect to a hub not registered with INCF Central (e.g., a local
hub under development) one can instanciate the proxy explicitly as in 
(setting offline=True avoids ever calling the url)

>>> from incf.dai.hub import HubProxy
>>> myhub = HubProxy('http://some.url?service=WPS', offline=True)
>>> myhub   # doctest: +ELLIPSIS
<incf.dai.hub.HubProxy object at ...>

At the very least the generic call method to be invoked as in 

>>> capabilities = myhub(version=None, request='GetCapabilities')
Requested URL: http://some.url?service=WPS&request=GetCapabilities&ResponseForm=xml
positional arguments: ('GET',)

should always be available.
The first argument here is to override the version specification which
is not supported for 'GetCapabilities' calls. Second is the name of the 
request to be invoked at the hub.
For convenience 'GetCapabilities' is also provided as a method
on the hub proxy itself.

>>> myhub.GetCapabilities()  # doctest: +ELLIPSIS
Requested URL: http://some.url?service=WPS&request=GetCapabilities&ResponseForm=xml
positional arguments: ('GET',)
<incf.dai.response.Response object at ...>




.. _specification: http://code.google.com/p/incf-dai/wiki/INCFProjectSpecification
