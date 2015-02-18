"""
Masks
=====

Masks are related to filters. Filters can block the processing of particular parts of the xml
hierarchy but they can only work on node level. If the part of the xml hierarchy that you want to
filter out is read in as an instance of one of the classes in parser/doxygen/*.py then you can use
the filters. However, if you want to filter out an attribute from one of the nodes (and some of the
xml child nodes are read in as attributes on their parents) then you can't use a filter.

We introduce the Mask's to fulfil this need. The masks are designed to be applied to a particular
node type and to limit the access to particular attributes on the node. For example, then
NoParameterNamesMask wraps a node a returns all its standard attributes but returns None for the
'declname' and 'defname' attributes.

Currently the Mask functionality is only used for the text signature rendering for doing function
matching.

"""

class NoParameterNamesMask(object):

    def __init__(self, data_object):
        self.data_object = data_object

    def __getattr__(self, attr):

        if attr in ['declname', 'defname', 'defval']:
            return None

        return getattr(self.data_object, attr)

class MaskFactory(object):

    def __init__(self, lookup):
        self.lookup = lookup

    def mask(self, data_object):

        try:
            node_type = data_object.node_type
        except AttributeError as e:

            # Horrible hack to silence errors on filtering unicode objects
            # until we fix the parsing
            if type(data_object) == unicode:
                node_type = "unicode"
            else:
                raise e

        if node_type in self.lookup:
            Mask = self.lookup[node_type]
            return Mask(data_object)

        return data_object


class NullMaskFactory(object):

    def mask(self, data_object):
        return data_object

