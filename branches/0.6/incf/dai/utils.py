"""utilities to be offered by the central hub one day - in part at least"""

from incf.dai.config import HUBS

def list_hub_names():
    """Return list of ids/names of all known hubs"""
    return list(HUBS.keys())

def get_hub_by_name(name, minimal=False):
    """Return a HubProxy for the requested hub
    Raises KeyError if no hub by that name is found"""
    try:
        base_url = HUBS[name]
    except KeyError:
        print "Hub '%s' not found in %s." % (name, list_hub_names())
        raise KeyError
    import incf.dai.hub
    return incf.dai.hub.HubProxy(base_url, minimal)


# http://code.activestate.com/recipes/534109-xml-to-python-data-structure/
# Thanks Wai Yip Tung!

import re
import xml.sax.handler


NON_ID_CHAR = re.compile('[^_0-9a-zA-Z]')
def _name_mangle(name):
    """Get rid of unwanted characters in keys/ids"""
    return NON_ID_CHAR.sub('_', name)


class DataNode(object):
    """Custom data node object"""
    def __init__(self):
        self.attrs = {}    # XML attributes and child elements
        self.data = None    # child text data
    def __len__(self):
        """treat single element as a list of 1"""
        return 1
    def __getitem__(self, key):
        if isinstance(key, basestring):
            return self.attrs.get(key, None)
        else:
            return [self][key]
    def __contains__(self, name):
        return self.attrs.has_key(name)
    def keys(self):
        """Keys of the attrs dict"""
        return self.attrs.keys()
    def __nonzero__(self):
        return bool(self.attrs or self.data)
    def __getattr__(self, name):
        if name.startswith('__'):
            # need to do this for Python special methods???
            raise AttributeError(name)
        return self.attrs.get(name, None)
    def add_xml_attr(self, name, value):
        """Populating the attrs dict"""
        if name in self.attrs:
            # multiple attribute of the same name are represented 
            # by a list
            children = self.attrs[name]
            if not isinstance(children, list):
                children = [children]
                self.attrs[name] = children
            children.append(value)
        else:
            self.attrs[name] = value
    def __str__(self):
        return self.data or ''
    def __repr__(self):
        items = sorted(self.attrs.items())
        if self.data:
            items.append(('data', self.data))
        return u'{%s}' % ', '.join([u'%s:%s' % 
                                    (k, repr(v)) for k, v in items])

class TreeBuilder(xml.sax.handler.ContentHandler):
    """Custom Tree Builder"""
    def __init__(self):
        self.stack = []
        self.root = DataNode()
        self.current = self.root
        self.text_parts = []
        
    def startElement(self, name, attrs):
        self.stack.append((self.current, self.text_parts))
        self.current = DataNode()
        self.text_parts = []
        # xml attributes --> python attributes
        for key, value in attrs.items():
            self.current.add_xml_attr(_name_mangle(key), value)
            
    def endElement(self, name):
        text = ''.join(self.text_parts).strip()
        if text:
            self.current.data = text
        if self.current.attrs:
            obj = self.current
        else:
            # a text only node is simply represented by the string
            obj = text or ''
        self.current, self.text_parts = self.stack.pop()
        self.current.add_xml_attr(_name_mangle(name), obj)
    def characters(self, content):
        self.text_parts.append(content)


def xml2obj(src):
    """
    A simple function to converts XML data into native Python object.
    """

    builder = TreeBuilder()
    if isinstance(src, basestring):
        xml.sax.parseString(src, builder)
    else:
        xml.sax.parse(src, builder)
    return builder.root.attrs.values()[0]
