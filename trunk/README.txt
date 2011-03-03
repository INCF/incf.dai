====================================
INCF Digital Atlasing Infrastructure
====================================

This package provides a Python API to the Digital Brain Atlasing web
services provided by the International Neuroinformatics Coordinating  
Facility (INCF_). To be useful and functional it requires a working
internet connection at runtime. The details of the core webservices 
within the INCF Digital Atlasing Infrastructure (incf.dai) are available 
from the specification_.

To explore the functioanlity of this package interactively it is strongly
recommended to use an enhanced interactive Python interpreter like
IPython_ or bpython_.


Discovering and Accessing Hubs
==============================

In a nutshell the INCF DAI consistes of a network of so-called
*hubs* providing whatever services the group managing the hub decided
to share. To discover available hubs there is a utility function

>>> from incf.dai.utils import list_hub_names
>>> sorted(list_hub_names())
['aba', 'central', 'emap', 'ucsd', 'whs']

This provides a list of currently known hub names. (Note: atm the list
is provided by the package since the INCF central hub managing the
registry is a fast moving target still.)

Knowing the names of available hubs one can optain proxy objects
specific for a particular hub by calling

>>> from incf.dai.utils import get_hub_by_name
>>> whs = get_hub_by_name('whs')
>>> whs # doctest: +ELLIPSIS
<incf.dai.hub.HubProxy object at ...>

If you call for an unknow hub (or make a typo) you will get a ``KeyError``

>>> foo = get_hub_by_name('foo')
Traceback (most recent call last):
KeyError

For introspection the URL to the service controller for this hub is
available as 

>>> whs.base_url
'http://incf-dev-local.crbs.ucsd.edu/whs/atlas?service=WPS'

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

>>> sorted(whs.capabilities)
[u'DescribeSRS', u'GetStructureNamesByPOI', u'ListSRSs', u'ListTransformations', u'TransformPOI']

and all methods listed are available on the hub proxy right away

>>> sorted(whs.__dict__.keys())   # doctest: +NORMALIZE_WHITESPACE
['DescribeSRS', 'GetStructureNamesByPOI', 'ListSRSs',
'ListTransformations', 'TransformPOI', 'base_url', 
'capabilities', 'process_descriptions', 'proxy']

like in 

>>> response = whs.ListSRSs()
>>> sorted(response.keys())  # doctest: +NORMALIZE_WHITESPACE
[u'service', u'serviceInstance', u'version', u'wps_Process', 
u'wps_ProcessOutputs', u'wps_Status', u'xml_lang', u'xmlns_ogc', 
u'xmlns_ows', u'xmlns_wps', u'xmlns_xlink', u'xmlns_xsi', 
u'xsi_schemaLocation']

>>> response['wps_ProcessOutputs']['wps_Output']['wps_Data']['wps_ComplexData']['ListSRSResponse']['SRSCollection']['SRSList']  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
{SRS:[{Area:{structureName:u'Whole Brain'}, 
       Author:{authorCode:u'WHS', ...

For further convenience, the response object also supports attribute-like 
access to the data as in

>>> response.wps_Status  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
{creationTime:...

Note how the namespaces are preserved as prefixes of the key and attribute names.

Omitting required arguments raises an ``ApplicationError``

>>> response = whs.DescribeSRS()  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
Traceback (most recent call last):
...
ApplicationError: 
Code: NoApplicableCode
Text: Unexpected exception occured
URL:  http://incf-dev-local.crbs.ucsd.edu/whs/atlas?service=WPS&version=1.0.0&request=Execute&Identifier=DescribeSRS&ResponseForm=xml

whereas calling a method correctly gives and appropriate response (hopefully)

>>> response = whs.GetStructureNamesByPOI(format=None, srsName="Mouse_paxinos_1.0", x='1', y='4.3', z='1.78')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
>>> response.keys()
[u'xmlns_xlink', u'wps_Process', u'xml_lang', u'wps_Status', u'wps_ProcessOutputs', u'service', u'xmlns_xsi', u'xmlns_ows', u'xsi_schemaLocation', u'version', u'xmlns_ogc', u'xmlns_wps', u'serviceInstance']
>>> response.wps_ProcessOutputs.wps_Output.wps_Data.wps_ComplexData.StructureTermsResponse.StructureTerms.StructureTerm.Code.data
u'Cx'

The ``format=None`` here works around issue
http://code.google.com/p/incf-dai/issues/detail?id=14


The Response in detail
======================

The custom response object returned from service calls provides
a variety of useful information like the HTTP response headers

>>> sorted(response.headers.keys())  # doctest: +NORMALIZE_WHITESPACE
['connection', 'content-location', 'content-type', 'date', 'status', 
'transfer-encoding']

and for convenience there is a short-cut to the content type

>>> response.content_type
'text/xml;charset=UTF-8'

The source of the returned response page is available as

>>> response.content # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
'<?xml version="1.0" encoding="UTF-8"?>\n...

which is probably more readable when printed (for this doc test
calling ``print response`` is avoided but in an interactive session 
it should work just fine)

>>> str(response)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
'<?xml version="1.0" ?><wps:ExecuteResponse service="WPS"  ...

If the content type is XML there will also be a 'data' attribute
holding the parsed response 

>>> type(response.data)
<class 'incf.dai.utils.DataNode'>

which acts like a nested dictionary 

>>> response.data.keys() # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
[u'xmlns_xlink', u'wps_Process', u'xml_lang', u'wps_Status', 
u'wps_ProcessOutputs', u'service', u'xmlns_xsi', u'xmlns_ows', 
u'xsi_schemaLocation', u'version', u'xmlns_ogc', u'xmlns_wps', 
u'serviceInstance']

>>> wps_Data = response.data['wps_ProcessOutputs']['wps_Output']['wps_Data']
>>> wps_Data['wps_ComplexData']['StructureTermsResponse']['StructureTerms']  # doctest: +NORMALIZE_WHITESPACE
{StructureTerm:{Code:{codeSpace:u'Mouse_paxinos_1.0', 
isDefault:u'true', data:u'Cx'}, Description:u'Term - Cx
derived from WHS hub based on the supplied POI.', Name:''}, hubCode:u'WHS'}

but also supports attribute-like access (as long as the keys don't
contain characters that make them unsuited as attribute names - in
those cases only subscription access works)

>>> response.data.xmlns_xsi
u'http://www.w3.org/2001/XMLSchema-instance'

Again for convenience, the ``data`` attribute can be bypassed
as the ``data`` content is lifted" to the response object itself

>>> response.data.keys() == response.keys()
True

and

>>> response.xmlns_xsi
u'http://www.w3.org/2001/XMLSchema-instance'

Digging deeper into the response data requires knowledge of
the response schema which is available from http://incf.org/WaxML
or introspection of the content of the ``response.data`` attribute.


Improving Performance
=====================

Accessing a hub by calling ``get_hub_by_name`` as presented above 
triggers calling ``DescribeProcess`` on hub proxy initialization to 
infer the hubs capabilities and to dynamically create methods making 
those capabilities readily available on the hub proxy. 
Depending on context and intended usage you may want to avoid that 
overhead and rather prefer a "naked" hub proxy as in

>>> whs_minimal = get_hub_by_name('whs', minimal=True)

This avoids calling ``DescribeProcess`` on initialization but in
return all you are left with is the generic call method that
requires you to pass all arguments needed to construct the 
proper WPS request

>>> response = whs_minimal(version='1.0.0', request='Execute', identifier='ListSRSs')
>>> sorted(response.keys()) # doctest: +NORMALIZE_WHITESPACE 
[u'service', u'serviceInstance', u'version', u'wps_Process',
u'wps_ProcessOutputs', u'wps_Status', u'xml_lang', u'xmlns_ogc',
u'xmlns_ows', u'xmlns_wps', u'xmlns_xlink', u'xmlns_xsi',
u'xsi_schemaLocation']

Once you know what you need to call from your own code you
may prefer this approach.


Logging
=======

Per default, all service calls are logged at ``INFO`` level to a custom log 
file (``incf.dai.log``)in the current working directory including a time stamp, 
the package name, the log level and the URL called.


Accessing Hubs not registered at INCF
=====================================

To connect to a hub not registered with INCF Central (e.g., a local
hub under development) one can instanciate the proxy explicitly as in 
(setting ``offline=True`` avoids ever calling the url)

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
is not supported for ``GetCapabilities`` calls. Second is the name of the 
request to be invoked at the hub.
For convenience ``GetCapabilities`` is also provided as a method
on the hub proxy itself.

>>> myhub.GetCapabilities()  # doctest: +ELLIPSIS
Requested URL: http://some.url?service=WPS&request=GetCapabilities&ResponseForm=xml
positional arguments: ('GET',)
<incf.dai.response.Response object at ...>



.. _INCF: http://incf.org
.. _specification: http://code.google.com/p/incf-dai/wiki/INCFProjectSpecification
.. _IPython: http://ipython.scipy.org/moin/
.. _bpython: http://bpython-interpreter.org/
